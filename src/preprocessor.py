"""
PCD Palm Line Scanner - Preprocessor Module
Mengekstrak Region of Interest (ROI) telapak tangan dengan
Auto-Orientation Alignment (PCD Central Moments) dan normalisasi kontras.
"""

import cv2
import numpy as np


class PalmPreprocessor:
    def __init__(self, target_roi_size=(400, 400)):
        self.target_roi_size = target_roi_size
        self.mp_hands = None
        self._init_mediapipe()

    def _init_mediapipe(self):
        """Inisialisasi MediaPipe jika tersedia di runtime."""
        try:
            import mediapipe as mp
            if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'hands'):
                self.mp_hands = mp.solutions.hands.Hands(
                    static_image_mode=True,
                    max_num_hands=1,
                    min_detection_confidence=0.5
                )
        except Exception:
            self.mp_hands = None

    def segment_skin_pcd(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Segmentasi warna kulit klasik PCD (YCrCb color space thresholding).
        """
        ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
        lower_skin = np.array([0, 133, 77], dtype=np.uint8)
        upper_skin = np.array([255, 173, 127], dtype=np.uint8)
        mask = cv2.inRange(ycrcb, lower_skin, upper_skin)

        # Operasi morfologi pembersihan noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

    def align_hand_orientation(self, image_bgr: np.ndarray, skin_mask: np.ndarray):
        """
        Rotasi otomatis telapak tangan agar selalu tegak lurus (0 derajat / Upright)
        menggunakan Central Image Moments (PCD Principal Axis Alignment).
        """
        h, w = image_bgr.shape[:2]
        contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return image_bgr, skin_mask, 0.0

        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) < (h * w * 0.02):
            return image_bgr, skin_mask, 0.0

        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return image_bgr, skin_mask, 0.0

        centroid_x = M["m10"] / M["m00"]
        centroid_y = M["m01"] / M["m00"]

        # Sudut sumbu utama tangan
        mu20, mu02, mu11 = M["mu20"], M["mu02"], M["mu11"]
        theta = 0.5 * np.arctan2(2 * mu11, mu20 - mu02)
        angle_deg = np.degrees(theta)

        # Hitung sudut rotasi agar tegak lurus vertikal (90 derajat)
        rot_angle = angle_deg - 90.0 if angle_deg > 0 else angle_deg + 90.0

        # Jika rotasi sangat kecil (< 4 derajat), tidak perlu diputar
        if abs(rot_angle) < 4.0:
            return image_bgr, skin_mask, 0.0

        rot_mat = cv2.getRotationMatrix2D((centroid_x, centroid_y), rot_angle, 1.0)
        rotated_bgr = cv2.warpAffine(image_bgr, rot_mat, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        rotated_mask = cv2.warpAffine(skin_mask, rot_mat, (w, h), flags=cv2.INTER_NEAREST)

        # Pastikan arah jari menghadap ke atas (y_fingers < y_palm_center)
        dist_map = cv2.distanceTransform(rotated_mask, cv2.DIST_L2, 5)
        _, _, _, maxLoc = cv2.minMaxLoc(dist_map)
        palm_center_y = maxLoc[1]

        cnts_rot, _ = cv2.findContours(rotated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cnts_rot:
            c_rot = max(cnts_rot, key=cv2.contourArea)
            M_rot = cv2.moments(c_rot)
            if M_rot["m00"] > 0:
                hand_centroid_y = M_rot["m01"] / M_rot["m00"]
                # Jika centroid tangan berada di bawah pusat telapak, putar 180 derajat
                if hand_centroid_y > (palm_center_y + 8):
                    rot_180 = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), 180.0, 1.0)
                    rotated_bgr = cv2.warpAffine(rotated_bgr, rot_180, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                    rotated_mask = cv2.warpAffine(rotated_mask, rot_180, (w, h), flags=cv2.INTER_NEAREST)
                    rot_angle += 180.0

        return rotated_bgr, rotated_mask, round(rot_angle, 1)

    def extract_palm_roi_classical(self, image_bgr: np.ndarray, skin_mask: np.ndarray = None):
        """
        Ekstraksi ROI telapak tangan menggunakan Maximum Inscribed Circle (Distance Transform)
        pada citra tangan yang sudah ditegakkan.
        """
        h, w = image_bgr.shape[:2]
        if skin_mask is None:
            skin_mask = self.segment_skin_pcd(image_bgr)

        contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            cy, cx = h // 2, w // 2
            half_box = min(h, w) // 3
            roi = image_bgr[max(0, cy - half_box):min(h, cy + half_box),
                            max(0, cx - half_box):min(w, cx + half_box)]
            roi_resized = cv2.resize(roi, self.target_roi_size)
            return roi_resized, skin_mask

        frame_cx, frame_cy = w / 2.0, h / 2.0
        diag = np.hypot(w, h)

        best_contour = None
        best_score = -1.0

        for c in contours:
            area = cv2.contourArea(c)
            if area < (h * w * 0.02):
                continue
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            dist_center = np.hypot(cx - frame_cx, cy - frame_cy)

            score = area * (1.0 - 0.5 * (dist_center / diag))
            if score > best_score:
                best_score = score
                best_contour = c

        if best_contour is None:
            best_contour = max(contours, key=cv2.contourArea)

        hand_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.drawContours(hand_mask, [best_contour], -1, 255, -1)

        # Maximum Inscribed Circle untuk mengunci pusat cekungan telapak tangan
        dist_map = cv2.distanceTransform(hand_mask, cv2.DIST_L2, 5)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(dist_map)
        cx, cy = maxLoc
        R = float(maxVal)

        if R < 20:
            x, y, bw, bh = cv2.boundingRect(best_contour)
            palm_crop = image_bgr[y:y+bh, x:x+bw]
        else:
            half_box = int(R * 1.35)
            x1 = max(0, cx - half_box)
            y1 = max(0, cy - half_box)
            x2 = min(w, cx + half_box)
            y2 = min(h, cy + half_box)
            palm_crop = image_bgr[y1:y2, x1:x2]

        if palm_crop.size == 0 or palm_crop.shape[0] < 30 or palm_crop.shape[1] < 30:
            x, y, bw, bh = cv2.boundingRect(best_contour)
            palm_crop = image_bgr[y:y+bh, x:x+bw]

        roi_resized = cv2.resize(palm_crop, self.target_roi_size)
        return roi_resized, skin_mask

    def preprocess(self, image_bgr: np.ndarray, auto_align: bool = True) -> dict:
        """
        Pipeline preprocessing PCD lengkap:
        1. Resize skala aman
        2. Segmentasi kulit (YCrCb)
        3. Auto-Orientation Alignment (Rotasi tegak 0 derajat via Image Moments)
        4. Ekstraksi ROI telapak tangan murni (Distance Transform)
        5. Normalisasi Iluminasi (Background Division)
        6. Peningkatan Kontras Adaptif (CLAHE)
        """
        h, w = image_bgr.shape[:2]
        max_dim = 1000
        if max(h, w) > max_dim:
            scale = max_dim / float(max(h, w))
            image_bgr = cv2.resize(image_bgr, (int(w * scale), int(h * scale)))

        # 1. Segmentasi kulit awal
        skin_mask = self.segment_skin_pcd(image_bgr)
        rot_angle = 0.0
        aligned_bgr = image_bgr
        aligned_mask = skin_mask

        # 2. Auto-Orientation Alignment
        if auto_align:
            aligned_bgr, aligned_mask, rot_angle = self.align_hand_orientation(image_bgr, skin_mask)

        # 3. Ekstraksi ROI pada tangan yang sudah tegak
        roi, _ = self.extract_palm_roi_classical(aligned_bgr, aligned_mask)

        # 4. Grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # 5. Normalisasi Iluminasi (Background Division)
        bg_blur = cv2.GaussianBlur(gray_roi, (51, 51), 0)
        norm_gray = cv2.divide(gray_roi, bg_blur, scale=128)

        # 6. CLAHE
        clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(8, 8))
        clahe_roi = clahe.apply(norm_gray)

        method_str = f"Classical Moments Alignment ({rot_angle}°)" if auto_align and rot_angle != 0 else "Classical Upright"

        return {
            "original_resized": image_bgr,
            "aligned_bgr": aligned_bgr,
            "rot_angle": rot_angle,
            "roi_color": roi,
            "roi_gray": gray_roi,
            "roi_clahe": clahe_roi,
            "skin_mask": skin_mask,
            "method": method_str
        }
