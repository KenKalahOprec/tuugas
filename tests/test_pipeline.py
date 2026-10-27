"""
Test Pipeline Pengolahan Citra Digital: Scan Garis Tangan ke Tarot Major Arcana
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import numpy as np
from src.preprocessor import PalmPreprocessor
from src.line_extractor import PalmLineExtractor
from src.tarot_mapper import map_lines_to_tarot, TAROT_CARDS
from src.utils import generate_synthetic_palm


def test_full_pipeline():
    print("=== Memulai Pengujian Pipeline PCD ===")
    preprocessor = PalmPreprocessor(target_roi_size=(400, 400))
    extractor = PalmLineExtractor(roi_size=(400, 400))

    profiles = ["thin", "balanced", "thick"]
    results = []

    for profile in profiles:
        print(f"\n--- Testing Profil: {profile} ---")
        img = generate_synthetic_palm(profile)
        assert img is not None and img.shape == (600, 500, 3), "Gagal membuat sampel citra"

        # 1. Preprocessing
        prep = preprocessor.preprocess(img)
        assert prep["roi_clahe"] is not None, "Gagal tahap CLAHE"
        assert prep["roi_clahe"].shape == (400, 400), f"Dimensi ROI salah: {prep['roi_clahe'].shape}"
        print(f"  [OK] Preprocessing berhasil (Metode: {prep['method']})")

        # 2. Line Extraction
        analysis = extractor.analyze(prep["roi_clahe"])
        features = analysis["features"]

        h_thick = features["heart"]["thickness_val"]
        hd_thick = features["head"]["thickness_val"]
        l_thick = features["life"]["thickness_val"]
        f_thick = features["fate"]["thickness_val"]
        print(f"  [OK] Ketebalan Hati: {h_thick} px ({features['heart']['category']}) [Conf: {features['heart']['confidence']}]")
        print(f"  [OK] Ketebalan Kepala: {hd_thick} px ({features['head']['category']}) [Conf: {features['head']['confidence']}]")
        print(f"  [OK] Ketebalan Hidup: {l_thick} px ({features['life']['category']}) [Conf: {features['life']['confidence']}]")
        print(f"  [OK] Ketebalan Nasib (Fate): {f_thick} px ({features['fate']['category']}) [Conf: {features['fate']['confidence']}]")

        # 3. Tarot Mapping
        tarot = map_lines_to_tarot(features)
        assert 0 <= tarot["id"] <= 21, f"ID kartu di luar jangkauan: {tarot['id']}"
        assert tarot["id"] in TAROT_CARDS, f"Kartu tidak ada di kamus: {tarot['id']}"
        assert os.path.exists(tarot["img_path"]), f"Gambar kartu tidak ditemukan: {tarot['img_path']}"
        print(f"  [OK] Kartu Tarot: #{tarot['id']} - {tarot['name']} ({tarot['name_id']})")
        print(f"  [OK] Gambar Kartu: {tarot['img']} (Exists: True)")
        print(f"  [OK] Kata Kunci: {', '.join(tarot['keywords'])}")
        print(f"  [OK] Makna Pribadi: {tarot['makna_pribadi'][:60]}...")

        results.append(tarot["id"])

    # 4. Verifikasi seluruh 22 kartu tarot di kamus
    assert len(TAROT_CARDS) == 22, f"Jumlah kartu bukan 22, melainkan {len(TAROT_CARDS)}"
    print("\n=== Seluruh Pengujian Pipeline PCD BERHASIL (PASSED) ===")


if __name__ == "__main__":
    test_full_pipeline()
