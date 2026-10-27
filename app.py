"""
Aplikasi Web PCD: Palm Line Scanner to Major Arcana Tarot
Framework: Streamlit
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import importlib

import src.tarot_mapper
import src.preprocessor
import src.line_extractor
importlib.reload(src.tarot_mapper)
importlib.reload(src.preprocessor)
importlib.reload(src.line_extractor)

from src.preprocessor import PalmPreprocessor
from src.line_extractor import PalmLineExtractor
from src.tarot_mapper import map_lines_to_tarot, TAROT_CARDS
from src.utils import generate_synthetic_palm

st.set_page_config(
    page_title="Palm Tarot Scanner (PCD)",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #7928CA;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .tarot-card-box {
        background: linear-gradient(135deg, #1f1f2e 0%, #16161f 100%);
        border: 2px solid #9d4edd;
        border-radius: 16px;
        padding: 24px;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(157, 78, 221, 0.25);
        text-align: center;
    }
    .metric-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


preprocessor = PalmPreprocessor(target_roi_size=(400, 400))
extractor = PalmLineExtractor(roi_size=(400, 400))

# Sidebar
st.sidebar.title("⚙️ Pengaturan & Input")
input_mode = st.sidebar.radio(
    "Pilih Sumber Gambar:",
    ["Gunakan Sampel Bawaan", "Upload Gambar (JPG/PNG)", "Gunakan Kamera"],
    index=0
)

image_bgr = None

if input_mode == "Gunakan Sampel Bawaan":
    sample_type = st.sidebar.selectbox(
        "Pilih Profil Sampel Telapak:",
        ["balanced", "thick", "thin"],
        format_func=lambda x: f"Profil Garis {x.capitalize()}"
    )
    image_bgr = generate_synthetic_palm(sample_type)

elif input_mode == "Upload Gambar (JPG/PNG)":
    uploaded_file = st.sidebar.file_uploader("Unggah foto telapak tangan Anda:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

elif input_mode == "Gunakan Kamera":
    st.sidebar.caption("💡 **Tips Kamera:** Dekatkan telapak tangan ke tengah kamera agar telapak mendominasi layar dan wajah tidak ikut masuk.")
    cam_img = st.sidebar.camera_input("Ambil foto telapak tangan:")
    if cam_img is not None:
        file_bytes = np.asarray(bytearray(cam_img.read()), dtype=np.uint8)
        image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Orientasi & Format Tangan (PCD)")
auto_align = st.sidebar.checkbox("🔄 Auto-Rotate Alignment", value=True, help="Menegakkan tangan miring secara otomatis menggunakan Momen Inersia Citra (PCA)")
manual_rot = st.sidebar.selectbox("Putar Manual:", [0, 90, 180, 270], format_func=lambda x: f"{x}°")

hand_format = st.sidebar.radio(
    "Format Foto Tangan:",
    ["Hanya Telapak (Close-up / Sampel)", "Seluruh Tangan (Ada Jari-Jari)"],
    index=1 if input_mode != "Gunakan Sampel Bawaan" else 0,
    help="Gunakan 'Seluruh Tangan' jika foto Anda memuat jari tangan agar garis deteksi tidak meleset ke ruas jari."
)

if hand_format == "Seluruh Tangan (Ada Jari-Jari)":
    default_yh = (42, 58)
    default_yhd = (56, 72)
    default_yl = (60, 94)
    default_yf = (50, 92)
else:
    default_yh = (28, 48)
    default_yhd = (45, 68)
    default_yl = (48, 92)
    default_yf = (38, 88)

with st.sidebar.expander("🎛️ Penyesuaian Posisi 4 Garis (Kalibrasi)", expanded=False):
    st.caption("Ubah rentang jika foto tangan memiliki proporsi jari yang unik:")
    yh = st.slider("Zona Garis Hati (% tinggi):", 10, 80, default_yh)
    yhd = st.slider("Zona Garis Kepala (% tinggi):", 20, 85, default_yhd)
    yl = st.slider("Zona Garis Hidup (% tinggi):", 30, 98, default_yl)
    yf = st.slider("Zona Garis Nasib (% tinggi):", 20, 95, default_yf)

zone_params = {
    "y_heart": (yh[0] / 100.0, yh[1] / 100.0),
    "y_head": (yhd[0] / 100.0, yhd[1] / 100.0),
    "y_life": (yl[0] / 100.0, yl[1] / 100.0),
    "y_fate": (yf[0] / 100.0, yf[1] / 100.0),
}

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Metode PCD yang Diterapkan:**
- Central Image Moments (Auto-Rotate)
- Segmentasi Kulit YCrCb
- Maximum Inscribed Circle (Distance Transform)
- CLAHE (Contrast Enhancement)
- Bottom-Hat Filtering
- Gabor Filter Bank (8 Orientasi)
- Binarisasi Otsu
- Skeletonization (Centerline)
- Distance Transform (Ketebalan)
""")

# Header
st.markdown('<div class="main-header">🔮 Palmistry to Tarot Scanner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ekstraksi 4 Garis Utama Telapak Tangan & Pemetaan ke 22 Kartu Major Arcana</div>', unsafe_allow_html=True)

if image_bgr is None:
    st.info("👋 Silakan pilih atau unggah gambar telapak tangan dari panel sebelah kiri untuk memulai analisis.")
    st.stop()

# Manual Rotation jika dipilih pengguna
if manual_rot == 90:
    image_bgr = cv2.rotate(image_bgr, cv2.ROTATE_90_CLOCKWISE)
elif manual_rot == 180:
    image_bgr = cv2.rotate(image_bgr, cv2.ROTATE_180)
elif manual_rot == 270:
    image_bgr = cv2.rotate(image_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Processing Pipeline
with st.spinner("Memproses citra telapak tangan dengan algoritma PCD..."):
    prep_res = preprocessor.preprocess(image_bgr, auto_align=auto_align)
    analysis_res = extractor.analyze(prep_res["roi_clahe"], **zone_params)
    tarot_res = map_lines_to_tarot(analysis_res["features"])
    overlay_img = extractor.generate_overlay(prep_res["roi_color"], analysis_res["lines"], analysis_res["metrics"])

tab1, tab2, tab3 = st.tabs(["🎴 Hasil Kartu Tarot", "🔬 Tahapan Algoritma PCD", "📖 Ensiklopedia Major Arcana"])

# TAB 1: HASIL TAROT
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("📸 Deteksi & Overlay Garis Tangan")
        st.image(cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB), caption="Deteksi 4 Garis (Merah: Hati, Biru: Kepala, Hijau: Kehidupan, Ungu: Nasib)", use_container_width=True)

        st.markdown("#### 📏 Pengukuran Ketebalan & Akurasi Garis")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            h_conf = int(analysis_res['metrics']['heart']['confidence'] * 100)
            st.metric("❤️ Heart Line", f"{analysis_res['features']['heart']['thickness_val']} px", f"{analysis_res['features']['heart']['category'].upper()} ({h_conf}%)")
        with m_col2:
            hd_conf = int(analysis_res['metrics']['head']['confidence'] * 100)
            st.metric("🧠 Head Line", f"{analysis_res['features']['head']['thickness_val']} px", f"{analysis_res['features']['head']['category'].upper()} ({hd_conf}%)")
        with m_col3:
            l_conf = int(analysis_res['metrics']['life']['confidence'] * 100)
            st.metric("🌱 Life Line", f"{analysis_res['features']['life']['thickness_val']} px", f"{analysis_res['features']['life']['category'].upper()} ({l_conf}%)")
        with m_col4:
            f_conf = int(analysis_res['metrics']['fate']['confidence'] * 100)
            st.metric("🔮 Fate Line", f"{analysis_res['features']['fate']['thickness_val']} px", f"{analysis_res['features']['fate']['category'].upper()} ({f_conf}%)")

    with col_right:
        st.subheader("✨ Kartu Tarot Major Arcana Anda")

        # Gambar kartu aman dengan fallback path
        card_id = tarot_res.get("id", 0)
        img_name = tarot_res.get("img", f"m{card_id:02d}.jpg")
        base_cards_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cards")
        img_path = tarot_res.get("img_path") or os.path.join(base_cards_dir, img_name)

        c_img_col, c_text_col = st.columns([1.1, 2.0], gap="medium")
        with c_img_col:
            if os.path.exists(img_path):
                st.image(img_path, caption=f"Major Arcana #{card_id}", use_container_width=True)
            else:
                st.info("Gambar kartu tidak ditemukan.")

        with c_text_col:
            st.markdown(f"### {tarot_res.get('name', 'The Tarot')}")
            st.markdown(f"**_{tarot_res.get('name_id', '')}_**")

            # Keyword badges
            keywords = tarot_res.get("keywords", ["Major Arcana"])
            kw_html = " ".join([f"<span class='metric-badge' style='background:#7928CA; color:white;'>{k}</span>" for k in keywords])
            st.markdown(kw_html, unsafe_allow_html=True)

            st.markdown("#### 📜 Makna Filosofis Kartu")
            st.write(tarot_res.get("makna_kartu", tarot_res.get("description", "")))

        st.markdown("---")
        st.markdown("### 🔮 Pembacaan Personal Karakter & Nasib")
        st.info(tarot_res.get("makna_pribadi", tarot_res.get("description", "")))

        analisis = tarot_res.get("analisis_garis", {})
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.markdown("**❤️ Aspek Emosi**")
            st.caption(analisis.get("hati", "Emosi mengalir stabil dan tulus."))
        with col_b:
            st.markdown("**🧠 Pola Pikir**")
            st.caption(analisis.get("kepala", "Pikiran tajam, kreatif, dan analitis."))
        with col_c:
            st.markdown("**🌱 Vitalitas**")
            st.caption(analisis.get("kehidupan", "Daya tahan tubuh kokoh dan adaptif."))
        with col_d:
            st.markdown("**🔮 Karier & Nasib**")
            st.caption(analisis.get("nasib", "Karier berkembang seiring kemandirian."))

        st.success(f"💡 **Petuah / Nasihat Tarot:** {tarot_res.get('nasihat', 'Percayalah pada jalan hidupmu.')}")
        st.caption(f"Metode ROI: {prep_res['method']} | Kontinuitas Garis: {analysis_res['features']['continuity_ratio']*100:.1f}%")

# TAB 2: TAHAPAN PCD
with tab2:
    st.subheader("🔬 Visualisasi Lengkap Step-by-Step Pengolahan Citra Digital")
    st.write("Setiap tahap transformasi citra dari input asli hingga ekstraksi kuantitatif ketebalan:")

    r1_col1, r1_col2, r1_col3 = st.columns(3)
    with r1_col1:
        st.caption("1. Input Citra Asli")
        st.image(cv2.cvtColor(prep_res["original_resized"], cv2.COLOR_BGR2RGB), use_container_width=True)
    with r1_col2:
        angle_str = f"Rotasi: {prep_res['rot_angle']}°" if prep_res['rot_angle'] != 0 else "Sudah Tegak"
        st.caption(f"2. Auto-Aligned (PCA {angle_str})")
        st.image(cv2.cvtColor(prep_res["aligned_bgr"], cv2.COLOR_BGR2RGB), use_container_width=True)
    with r1_col3:
        st.caption("3. ROI Inscribed Circle (400x400)")
        st.image(cv2.cvtColor(prep_res["roi_color"], cv2.COLOR_BGR2RGB), use_container_width=True)

    r2_col1, r2_col2, r2_col3 = st.columns(3)
    with r2_col1:
        st.caption("4. CLAHE Contrast Enhancement")
        st.image(prep_res["roi_clahe"], clamp=True, use_container_width=True)
    with r2_col2:
        st.caption("5. Bottom-Hat Transform (Lembah Garis)")
        st.image(analysis_res["enhanced"]["bottom_hat"], clamp=True, use_container_width=True)
    with r2_col3:
        st.caption("6. Gabor Filter Bank Response")
        st.image(analysis_res["enhanced"]["gabor"], clamp=True, use_container_width=True)

    st.markdown("#### 📐 Isolasi Zona Garis & Skeletonization (Pengukuran Ketebalan)")
    r3_col1, r3_col2, r3_col3, r3_col4 = st.columns(4)
    with r3_col1:
        st.caption("❤️ Heart Line")
        if "skeleton" in analysis_res["metrics"]["heart"]:
            st.image(analysis_res["metrics"]["heart"]["skeleton"], clamp=True, use_container_width=True)
        else:
            st.image(analysis_res["lines"]["heart"], clamp=True, use_container_width=True)
    with r3_col2:
        st.caption("🧠 Head Line")
        if "skeleton" in analysis_res["metrics"]["head"]:
            st.image(analysis_res["metrics"]["head"]["skeleton"], clamp=True, use_container_width=True)
        else:
            st.image(analysis_res["lines"]["head"], clamp=True, use_container_width=True)
    with r3_col3:
        st.caption("🌱 Life Line")
        if "skeleton" in analysis_res["metrics"]["life"]:
            st.image(analysis_res["metrics"]["life"]["skeleton"], clamp=True, use_container_width=True)
        else:
            st.image(analysis_res["lines"]["life"], clamp=True, use_container_width=True)
    with r3_col4:
        st.caption("🔮 Fate Line")
        if "skeleton" in analysis_res["metrics"]["fate"]:
            st.image(analysis_res["metrics"]["fate"]["skeleton"], clamp=True, use_container_width=True)
        else:
            st.image(analysis_res["lines"]["fate"], clamp=True, use_container_width=True)
            st.image(analysis_res["lines"]["life"], clamp=True, use_container_width=True)

# TAB 3: ENSIKLOPEDIA MAJOR ARCANA
with tab3:
    st.subheader("📖 22 Kartu Major Arcana & Profil Karakter Garis Tangan")
    st.write("Daftar lengkap 22 Kartu Major Arcana (Rider-Waite Deck) beserta makna filosofis dan interpretasi kepribadiannya:")

    base_card_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cards")

    for cid in range(0, 22):
        cdata = TAROT_CARDS[cid]
        card_img_path = os.path.join(base_card_dir, cdata["img"])
        with st.expander(f"#{cdata['id']} - {cdata['name']} ({cdata['name_id']})"):
            c_img, c_detail = st.columns([1, 3], gap="medium")
            with c_img:
                if os.path.exists(card_img_path):
                    st.image(card_img_path, use_container_width=True)
            with c_detail:
                st.markdown(f"#### {cdata['name_id']}")
                kw_str = " • ".join(cdata.get("keywords", []))
                st.markdown(f"**Kata Kunci:** `{kw_str}`")
                st.markdown(f"**Makna Filosofis:** {cdata['makna_kartu']}")
                st.markdown(f"**Interpretasi Karakter:** {cdata['makna_pribadi']}")
                st.markdown(f"💡 **Petuah:** _{cdata['nasihat']}_")
