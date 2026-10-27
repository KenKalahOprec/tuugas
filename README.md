# 🔮 Palmistry to Major Arcana Tarot Scanner (PCD)

Aplikasi **Pengolahan Citra Digital (PCD)** untuk mendeteksi 4 garis utama telapak tangan (*Heart Line*, *Head Line*, *Life Line*, dan *Fate Line*), mengukur ketebalan garis secara kuantitatif (*Skeletonization* + *Euclidean Distance Transform*), dan memetakannya ke 22 kartu Tarot Major Arcana dari dataset **Rider-Waite (`lsind18/tarot-json`)** dengan pembacaan karakter berbahasa Indonesia.

---

## 🌟 Fitur Utama

- **Auto-Orientation Alignment (PCD Moments)**: Menegakkan tangan miring secara otomatis menggunakan *Central Image Moments* $(\mu_{11}, \mu_{20}, \mu_{02})$ sebelum pemrosesan.
- **Auto Palm Crop (Maximum Inscribed Circle)**: Mengunci cekungan telapak tangan menggunakan *Distance Transform*, memotong bersih tanpa mengenai ruas jari atas.
- **Deteksi 4 Garis (Gaya Detector Modern)**:
  - ❤️ **Heart Line (Merah)**: Emosi, empati, dan relasi asmara.
  - 🧠 **Head Line (Cyan/Biru)**: Pola pikir, logika, dan kecerdasan intelektual.
  - 🌱 **Life Line (Hijau)**: Vitalitas, stamina, dan daya tahan hidup.
  - 🔮 **Fate Line (Ungu)**: Karier, jalan takdir, dan kemandirian hidup.
  - Dilengkapi *Bounding Box* dan *Confidence Score* deteksi.
- **Dataset 22 Kartu Major Arcana**: Memuat scan gambar asli (`assets/cards/m00.jpg` s/d `m21.jpg`) dan pembacaan kepribadian lengkap dalam Bahasa Indonesia.
- **Laboratorium Tahapan PCD Interaktif**: Visualisasi step-by-step transformasi citra (*Original -> Auto-Aligned -> Inscribed ROI -> CLAHE -> Bottom-Hat -> Gabor Bank -> Otsu -> Skeleton/Thickness*).
- **Slider Kalibrasi Real-Time**: Penyesuaian batas zona secara visual di sidebar.

---

## 📂 Struktur Proyek

```
pcd/
├── assets/
│   └── cards/                   # 22 Gambar Asli Major Arcana (m00.jpg - m21.jpg)
├── src/
│   ├── __init__.py
│   ├── preprocessor.py          # Auto-Orientation Moments, YCrCb, Inscribed Circle, CLAHE
│   ├── line_extractor.py        # Bottom-Hat, Gabor Bank, 4-Line Segmentation, Thickness
│   ├── tarot_mapper.py          # Kamus 22 Major Arcana & Pembacaan Bahasa Indonesia
│   └── utils.py                 # Generator Citra Telapak Sintetis
├── tests/
│   └── test_pipeline.py         # Unit Test Otomatis
├── app.py                       # Aplikasi Web Streamlit
├── download_major_arcana.py     # Script Pengunduh Dataset Kartu
└── requirements.txt             # Dependensi Python
```

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Kloning Repositori
```bash
git clone https://github.com/KenKalahOprec/tuugas.git
cd tuugas
```

### 2. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Pengujian Otomatis
```bash
python tests/test_pipeline.py
```

### 4. Jalankan Aplikasi Web
```bash
python -m streamlit run app.py
```
Buka browser pada `http://localhost:8501`.

