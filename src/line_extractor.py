"""
PCD Palm Line Scanner - Line Extractor Module
Menggabungkan pendekatan deteksi 4 garis utama (Heart, Head, Life, dan Fate Line)
seperti pada MuntahaShams/palm-line-detection dengan algoritma PCD klasik:
Bottom-Hat Morphology, Gabor Filter Bank, Skeletonization, dan Distance Transform.
"""

import cv2
import numpy as np
from skimage.morphology import skeletonize


class PalmLineExtractor:
    def __init__(self, roi_size=(400, 400)):
        self.h, self.w = roi_size
        self.gabor_kernels = self._build_gabor_bank()

    def _build_gabor_bank(self):
        """Membangun bank filter Gabor pada berbagai orientasi sudut."""
        kernels = []
        ksize = 15
        sigma = 2.5
        lamda = 8.0
        gamma = 0.5
        psi = 0
        for theta in np.arange(0, np.pi, np.pi / 8):
            kern = cv2.getGaborKernel(
                (ksize, ksize), sigma, theta, lamda, gamma, psi, ktype=cv2.CV_32F
            )
            kernels.append(kern)
        return kernels

    def enhance_lines(self, gray_clahe: np.ndarray) -> dict:
        """
        Peningkatan garis menggunakan Bottom-Hat Morphology & Bank Gabor Filter.
        """
        # 1. Bottom-Hat / Black-Hat (Closing - Original) untuk mendeteksi lembah gelap
        kernel_morph = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
        bottom_hat = cv2.morphologyEx(gray_clahe, cv2.MORPH_BLACKHAT, kernel_morph)

        # 2. Respon Maksimum Gabor Filter
        gabor_responses = []
        for kern in self.gabor_kernels:
            fimg = cv2.filter2D(bottom_hat, cv2.CV_32F, kern)
            gabor_responses.append(fimg)
        gabor_max = np.maximum.reduce(gabor_responses)
        gabor_norm = cv2.normalize(gabor_max, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # 3. Penggabungan berbobot
        combined = cv2.addWeighted(bottom_hat, 0.4, gabor_norm, 0.6, 0)

        # 4. Binarisasi adaptif / Otsu
        _, binary = cv2.threshold(combined, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 5. Membersihkan noise & gumpalan bayangan
        h, w = binary.shape
        cleaned_binary = np.zeros_like(binary)
        dist_map = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
        min_line_area = 50

        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area < min_line_area:
                continue

            comp_mask = (labels == i).astype(np.uint8)
            cnts, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not cnts:
                continue
            perimeter = cv2.arcLength(cnts[0], True)
            if perimeter == 0:
                continue

            elongation = (perimeter * perimeter) / float(area)
            max_thickness = np.max(dist_map[comp_mask > 0]) * 2.0

            if elongation >= 16.0 and max_thickness <= 18.0:
                cleaned_binary[labels == i] = 255

        # Hilangkan sisa noise di tepi bingkai
        cleaned_binary[:int(h * 0.10), :] = 0
        cleaned_binary[:, :10] = 0
        cleaned_binary[:, -10:] = 0
        cleaned_binary[-10:, :] = 0

        return {
            "bottom_hat": bottom_hat,
            "gabor": gabor_norm,
            "combined": combined,
            "binary": cleaned_binary
        }

    def _filter_dominant_line(self, zone_binary: np.ndarray, top_k: int = 1) -> np.ndarray:
        """
        Hanya mempertahankan garis terpanjang dan paling kontinyu di dalam zona.
        """
        if np.sum(zone_binary) == 0:
            return np.zeros_like(zone_binary)

        kernel_bridge = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        bridged = cv2.morphologyEx(zone_binary, cv2.MORPH_CLOSE, kernel_bridge)

        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(bridged, connectivity=8)
        if num_labels <= 1:
            return np.zeros_like(zone_binary)

        components = []
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            w_box = stats[i, cv2.CC_STAT_WIDTH]
            h_box = stats[i, cv2.CC_STAT_HEIGHT]
            diag = np.hypot(w_box, h_box)
            if area >= 40 and diag >= 25:
                components.append((i, area * diag))

        if not components:
            return np.zeros_like(zone_binary)

        components.sort(key=lambda x: x[1], reverse=True)
        top_indices = [c[0] for c in components[:top_k]]

        dominant_mask = np.zeros_like(zone_binary)
        for idx in top_indices:
            dominant_mask[labels == idx] = 255

        return dominant_mask

    def segment_major_lines(self, binary_lines: np.ndarray,
                            y_heart=(0.28, 0.48),
                            y_head=(0.45, 0.68),
                            y_life=(0.48, 0.92),
                            y_fate=(0.38, 0.88)) -> dict:
        """
        Memisahkan 4 garis telapak tangan (Heart, Head, Life, dan Fate Line)
        dengan zona anatomis terkalibrasi agar tidak menabrak ruas jari atas.
        """
        h, w = binary_lines.shape

        palm_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(palm_mask, (w // 2, h // 2), (int(w * 0.46), int(h * 0.46)), 0, 0, 360, 255, -1)
        palm_lines = cv2.bitwise_and(binary_lines, palm_mask)

        # Mask spasial 4 garis terkalibrasi
        heart_mask = np.zeros((h, w), dtype=np.uint8)
        head_mask = np.zeros((h, w), dtype=np.uint8)
        life_mask = np.zeros((h, w), dtype=np.uint8)
        fate_mask = np.zeros((h, w), dtype=np.uint8)

        # 1. Heart Line: Di bawah pangkal jari (y: 28% - 48%)
        y_h1, y_h2 = int(y_heart[0] * h), int(y_heart[1] * h)
        heart_mask[y_h1:y_h2, int(0.08 * w):int(0.92 * w)] = 255

        # 2. Head Line: Tengah melintang (y: 45% - 68%)
        y_hd1, y_hd2 = int(y_head[0] * h), int(y_head[1] * h)
        head_mask[y_hd1:y_hd2, int(0.08 * w):int(0.92 * w)] = 255

        # 3. Life Line: Kurva melingkari ibu jari (y: 48% - 92%)
        y_l1, y_l2 = int(y_life[0] * h), int(y_life[1] * h)
        life_mask[y_l1:y_l2, int(0.06 * w):int(0.75 * w)] = 255

        # 4. Fate Line (Garis Nasib): Koridor vertikal poros tengah (y: 38% - 88%)
        y_f1, y_f2 = int(y_fate[0] * h), int(y_fate[1] * h)
        fate_mask[y_f1:y_f2, int(0.38 * w):int(0.64 * w)] = 255

        raw_heart = cv2.bitwise_and(palm_lines, heart_mask)
        raw_head = cv2.bitwise_and(palm_lines, head_mask)
        raw_life = cv2.bitwise_and(palm_lines, life_mask)

        heart_line = self._filter_dominant_line(raw_heart, top_k=1)
        head_line = self._filter_dominant_line(raw_head, top_k=1)
        life_line = self._filter_dominant_line(raw_life, top_k=1)

        # Fate Line: Cari komponen garis yang dominan berorientasi vertikal (height >> width)
        raw_fate = cv2.bitwise_and(palm_lines, fate_mask)
        num_f, labels_f, stats_f, _ = cv2.connectedComponentsWithStats(raw_fate, connectivity=8)
        vertical_components = []
        for i in range(1, num_f):
            area = stats_f[i, cv2.CC_STAT_AREA]
            wb = stats_f[i, cv2.CC_STAT_WIDTH]
            hb = stats_f[i, cv2.CC_STAT_HEIGHT]
            v_ratio = hb / float(max(1, wb))
            # Garis nasib memiliki rasio vertikal tajam (tinggi jauh melebihi lebar)
            if v_ratio >= 1.5 and hb >= 30 and area >= 35:
                vertical_components.append((i, area * v_ratio))

        fate_line = np.zeros_like(raw_fate)
        if vertical_components:
            vertical_components.sort(key=lambda x: x[1], reverse=True)
            best_idx = vertical_components[0][0]
            fate_line[labels_f == best_idx] = 255

        return {
            "heart": heart_line,
            "head": head_line,
            "life": life_line,
            "fate": fate_line
        }

    def measure_thickness(self, line_binary: np.ndarray) -> dict:
        """
        Mengukur ketebalan, panjang, confidence score, dan bounding box garis.
        """
        if np.sum(line_binary) == 0:
            return {
                "mean_thickness": 0.0,
                "category": "absent",
                "pixel_count": 0,
                "length": 0,
                "confidence": 0.0,
                "bbox": None
            }

        bool_binary = line_binary > 0
        skel = skeletonize(bool_binary)
        dist_transform = cv2.distanceTransform(line_binary, cv2.DIST_L2, 5)

        centerline_radii = dist_transform[skel]
        if len(centerline_radii) == 0:
            mean_thick = 1.0
            length = 0
        else:
            mean_thick = float(np.mean(centerline_radii) * 2.0)
            length = int(np.sum(skel))

        # Kategori ketebalan
        if length < 20:
            cat = "faint"
        elif mean_thick < 3.2:
            cat = "thin"
        elif mean_thick <= 5.5:
            cat = "medium"
        else:
            cat = "thick"

        # Confidence score (0.70 - 0.98) seperti output YOLO/MuntahaShams
        conf = round(min(0.98, max(0.65, 0.70 + 0.28 * min(1.0, length / 160.0))), 2)

        # Bounding box
        cnts, _ = cv2.findContours(line_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bbox = None
        if cnts:
            all_pts = np.vstack(cnts)
            bx, by, bw, bh = cv2.boundingRect(all_pts)
            bbox = (int(bx), int(by), int(bw), int(bh))

        return {
            "mean_thickness": round(mean_thick, 2),
            "category": cat,
            "pixel_count": int(np.sum(bool_binary)),
            "length": length,
            "confidence": conf,
            "bbox": bbox,
            "skeleton": (skel.astype(np.uint8) * 255),
            "distance_map": dist_transform
        }

    def analyze(self, gray_clahe: np.ndarray,
                y_heart=(0.28, 0.48),
                y_head=(0.45, 0.68),
                y_life=(0.48, 0.92),
                y_fate=(0.38, 0.88)) -> dict:
        """
        Eksekusi penuh analisis 4 garis telapak tangan dengan parameter kalibrasi.
        """
        enhanced = self.enhance_lines(gray_clahe)
        lines = self.segment_major_lines(enhanced["binary"], y_heart, y_head, y_life, y_fate)

        heart_metrics = self.measure_thickness(lines["heart"])
        head_metrics = self.measure_thickness(lines["head"])
        life_metrics = self.measure_thickness(lines["life"])
        fate_metrics = self.measure_thickness(lines["fate"])

        total_skel_len = (
            heart_metrics["length"] +
            head_metrics["length"] +
            life_metrics["length"] +
            fate_metrics["length"]
        )
        continuity_ratio = min(1.0, max(0.1, total_skel_len / 480.0))

        features = {
            "heart": {
                "thickness_val": heart_metrics["mean_thickness"],
                "category": heart_metrics["category"],
                "length": heart_metrics["length"],
                "confidence": heart_metrics["confidence"],
                "bbox": heart_metrics["bbox"]
            },
            "head": {
                "thickness_val": head_metrics["mean_thickness"],
                "category": head_metrics["category"],
                "length": head_metrics["length"],
                "confidence": head_metrics["confidence"],
                "bbox": head_metrics["bbox"]
            },
            "life": {
                "thickness_val": life_metrics["mean_thickness"],
                "category": life_metrics["category"],
                "length": life_metrics["length"],
                "confidence": life_metrics["confidence"],
                "bbox": life_metrics["bbox"]
            },
            "fate": {
                "thickness_val": fate_metrics["mean_thickness"],
                "category": fate_metrics["category"],
                "length": fate_metrics["length"],
                "confidence": fate_metrics["confidence"],
                "bbox": fate_metrics["bbox"]
            },
            "continuity_ratio": continuity_ratio
        }

        return {
            "enhanced": enhanced,
            "lines": lines,
            "metrics": {
                "heart": heart_metrics,
                "head": head_metrics,
                "life": life_metrics,
                "fate": fate_metrics
            },
            "features": features
        }

    def generate_overlay(self, roi_color: np.ndarray, lines: dict, metrics: dict = None, *args, **kwargs) -> np.ndarray:
        """
        Visualisasi overlay 4 garis telapak tangan dengan label bounding box & confidence score
        (gaya detector MuntahaShams / YOLO):
        - Heart Line: Merah (Red)
        - Head Line: Cyan / Biru (Blue)
        - Life Line: Hijau (Green)
        - Fate Line: Ungu / Magenta (Purple)
        """
        overlay = roi_color.copy()
        color_mask = np.zeros_like(roi_color)

        color_mask[lines["heart"] > 0] = [0, 0, 255]      # Merah (Heart)
        color_mask[lines["head"] > 0] = [255, 130, 0]     # Cyan/Biru (Head)
        color_mask[lines["life"] > 0] = [0, 220, 0]       # Hijau (Life)
        color_mask[lines["fate"] > 0] = [220, 50, 200]    # Ungu / Magenta (Fate)

        mask_any = (
            (lines["heart"] > 0) |
            (lines["head"] > 0) |
            (lines["life"] > 0) |
            (lines["fate"] > 0)
        )
        overlay[mask_any] = cv2.addWeighted(roi_color, 0.35, color_mask, 0.65, 0)[mask_any]

        # Gambarkan bounding box deteksi + confidence score jika tersedia metrics
        if metrics is not None:
            labels_info = [
                ("heart", "Heart-Line", (0, 0, 255)),
                ("head", "Head-Line", (255, 130, 0)),
                ("life", "Life-Line", (0, 220, 0)),
                ("fate", "Fate-Line", (220, 50, 200))
            ]
            for key, name, color in labels_info:
                m = metrics.get(key, {})
                bbox = m.get("bbox")
                conf = m.get("confidence", 0.0)
                if bbox is not None and conf > 0.60:
                    bx, by, bw, bh = bbox
                    cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), color, 1, cv2.LINE_AA)
                    label_text = f"{name} {conf:.2f}"
                    # Label box background
                    cv2.rectangle(overlay, (bx, max(0, by - 16)), (bx + len(label_text) * 7 + 6, max(0, by)), color, -1)
                    cv2.putText(overlay, label_text, (bx + 3, max(12, by - 4)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

        return overlay
