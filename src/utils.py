"""
Helper Utilities for Palm Generation and Visualization
"""
import cv2
import numpy as np


def generate_synthetic_palm(thickness_profile="balanced") -> np.ndarray:
    """
    Membuat citra telapak tangan sintetis untuk pengujian atau demonstrasi.
    thickness_profile: 'thin' | 'balanced' | 'thick'
    """
    canvas = np.full((600, 500, 3), (200, 215, 235), dtype=np.uint8)  # Warna kulit dasar (BGR)

    # Shading telapak tangan (oval telapak tangan)
    cv2.ellipse(canvas, (250, 300), (180, 220), 0, 0, 360, (185, 200, 225), -1)

    th_map = {
        "thin": {"heart": 2, "head": 2, "life": 2, "fate": 2},
        "balanced": {"heart": 5, "head": 5, "life": 5, "fate": 4},
        "thick": {"heart": 8, "head": 8, "life": 8, "fate": 6}
    }
    t = th_map.get(thickness_profile, th_map["balanced"])

    # 1. Heart Line (Garis Hati - atas telapak)
    pts_heart = np.array([[120, 220], [200, 215], [300, 230], [380, 245]], np.int32)
    cv2.polylines(canvas, [pts_heart], isClosed=False, color=(110, 120, 145), thickness=t["heart"], lineType=cv2.LINE_AA)

    # 2. Head Line (Garis Kepala - tengah telapak)
    pts_head = np.array([[130, 275], [210, 280], [320, 310], [390, 350]], np.int32)
    cv2.polylines(canvas, [pts_head], isClosed=False, color=(100, 110, 140), thickness=t["head"], lineType=cv2.LINE_AA)

    # 3. Life Line (Garis Kehidupan - kurva melingkari jempol)
    pts_life = np.array([[130, 280], [170, 320], [190, 380], [180, 450], [150, 490]], np.int32)
    cv2.polylines(canvas, [pts_life], isClosed=False, color=(90, 100, 135), thickness=t["life"], lineType=cv2.LINE_AA)

    # 4. Fate Line (Garis Nasib - vertikal melintasi tengah telapak)
    pts_fate = np.array([[260, 470], [255, 380], [250, 290], [252, 230]], np.int32)
    cv2.polylines(canvas, [pts_fate], isClosed=False, color=(105, 115, 140), thickness=t["fate"], lineType=cv2.LINE_AA)

    # Sedikit Gaussian Noise untuk tekstur alami
    noise = np.random.normal(0, 3, canvas.shape).astype(np.int16)
    noisy = np.clip(canvas.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return noisy

