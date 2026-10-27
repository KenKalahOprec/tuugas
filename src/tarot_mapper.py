"""
PCD Palm Line Scanner to Major Arcana Tarot
Dataset 22 Major Arcana dari lsind18/tarot-json dengan Makna Bahasa Indonesia Lengkap
dan Interpretasi Personal Berdasarkan Karakter 4 Garis Tangan (Heart, Head, Life, Fate Line).
"""
import os

TAROT_CARDS = {
    0: {
        "id": 0,
        "name": "The Fool",
        "name_id": "Si Pengembara Bebas (The Fool)",
        "img": "m00.jpg",
        "keywords": ["Awal Baru", "Spontanitas", "Keberanian Murni", "Kebebasan"],
        "makna_kartu": "The Fool melambangkan awal mula perjalanan kosmik, langkah pertama ke dalam hal yang belum diketahui dengan hati yang murni, optimisme tanpa prasangka, dan keyakinan mutlak pada semesta.",
        "makna_pribadi": (
            "Garis tanganmu yang luwes menandakan jiwa bebas yang tidak terikat oleh rasa takut akan kegagalan. "
            "Kamu memiliki aura pemula yang segar, siap mencoba peluang baru tanpa beban masa lalu."
        ),
        "analisis_garis": {
            "hati": "Emosimu mengalir tulus, mudah memaafkan, dan jarang memendam kepahitan lama.",
            "kepala": "Pola pikirmu sangat terbuka, menyukai eksplorasi ide unik yang tidak konvensional.",
            "kehidupan": "Energi hidupmu dinamis dan lentur, mudah bangkit dan beradaptasi di lingkungan baru.",
            "nasib": "Garis nasib samar atau mengalir bebas, menandakan jalan kariermu bukan tipe satu jalur kaku, melainkan petualangan dinamis yang kamu ciptakan sendiri."
        },
        "nasihat": "Percayalah pada insting dan lompatan pertamamu, namun tetap perhatikan batu sandungan di tepi jalan."
    },
    1: {
        "id": 1,
        "name": "The Magician",
        "name_id": "Sang Alkemis / Penyihir (The Magician)",
        "img": "m01.jpg",
        "keywords": ["Manifestasi", "Kecerdasan Praktis", "Daya Cipta", "Kehendak Kuat"],
        "makna_kartu": "The Magician adalah lambang penguasaan atas empat elemen kehidupan. Kartu ini menunjukkan kemampuan mengubah ide murni menjadi kenyataan fisik melalui keahlian, fokus, dan tekad nyata.",
        "makna_pribadi": (
            "Garis kepalamu yang tajam dan dominan mencerminkan kecerdasan tajam dan daya cipta luar biasa. "
            "Kamu memiliki bakat alami dalam meyakinkan orang lain serta mengeksekusi rencana rumit menjadi berhasil."
        ),
        "analisis_garis": {
            "hati": "Emosi terarah dan terkontrol dengan baik, kamu jarang membiarkan perasaan merusak fokus kerja.",
            "kepala": "Sangat analitis, inovatif, dan mampu melihat solusi di saat orang lain buntu.",
            "kehidupan": "Daya hidup dipicu oleh ambisi dan karya nyata yang sedang kamu bangun.",
            "nasib": "Garis nasib tegas mengarah ke bukit Saturnus, menandakan ambisi karier yang kuat dan kemampuan menentukan takdir sukses melalui keahlian tanganmu sendiri."
        },
        "nasihat": "Semua sumber daya dan keahlian yang kamu butuhkan sudah ada di tanganmu. Mulailah bertindak nyata sekarang."
    },
    2: {
        "id": 2,
        "name": "The High Priestess",
        "name_id": "Sang Pendeta Wanita Agung (The High Priestess)",
        "img": "m02.jpg",
        "keywords": ["Intuisi Batin", "Misteri", "Pengetahuan Rahasia", "Kedamaian"],
        "makna_kartu": "Penjaga gerbang alam bawah sadar. Kartu ini mengingatkan bahwa jawaban terdalam atas masalahmu tidak selalu datang dari logika duniawi, melainkan bisikan hati nurani yang hening.",
        "makna_pribadi": (
            "Kombinasi garis tanganmu mencerminkan kepekaan intuitif yang sangat kuat. Firasat atau gut feelings-mu "
            "sering kali terbukti benar bahkan sebelum kejadian itu nyata terlihat."
        ),
        "analisis_garis": {
            "hati": "Sangat peka, mampu merasakan suasana hati dan energi orang di sekitarmu dengan akurat.",
            "kepala": "Pola pikir reflektif, menyukai filosofi, simbolisme, dan observasi diam-diam.",
            "kehidupan": "Vitalitas tenang dan stabil, membutuhkan waktu hening menyendiri untuk mengisi ulang energi batin.",
            "nasib": "Garis nasib halus dan intuitif, kariermu berkembang paling subur di bidang yang memerlukan wawasan mendalam, penelitian, atau bimbingan spiritual."
        },
        "nasihat": "Dengarkan suara hatimu saat mengambil keputusan besar; jangan biarkan hiruk-pikuk luar menenggelamkan intuisimu."
    },
    3: {
        "id": 3,
        "name": "The Empress",
        "name_id": "Sang Permaisuri (The Empress)",
        "img": "m03.jpg",
        "keywords": ["Kelimpahan", "Kasih Sayang", "Kreativitas Subur", "Kehangatan"],
        "makna_kartu": "The Empress adalah personifikasi Dewi Ibu: pemeliharaan, keindahan alam, kelimpahan rezeki, dan kesuburan ide maupun materi yang siap dipanen.",
        "makna_pribadi": (
            "Garis tangan yang tebal dan melengkung hangat mencerminkan sifat penyayang, suportif, dan aura penyejuk. "
            "Orang-orang merasa nyaman berada di dekatmu karena kamu memancarkan penerimaan tulus."
        ),
        "analisis_garis": {
            "hati": "Kapasitas cinta yang melimpah, penuh empati, dan suka merawat orang-orang terkasih.",
            "kepala": "Kreatif, imajinatif, dan selalu memikirkan kesejahteraan bersama.",
            "kehidupan": "Vitalitas fisik yang subur dan kuat, memiliki daya pulih alami yang cepat.",
            "nasib": "Garis nasib subur dan bercabang ke atas, menandakan karier yang menghasilkan kelimpahan, kreativitas, dan hubungan harmonis dengan rekan kerja."
        },
        "nasihat": "Buka dirimu untuk menerima kelimpahan dan rawatlah dirimu sendiri sebaik kamu merawat orang lain."
    },
    4: {
        "id": 4,
        "name": "The Emperor",
        "name_id": "Sang Kaisar (The Emperor)",
        "img": "m04.jpg",
        "keywords": ["Kepemimpinan", "Struktur", "Otoritas", "Disiplin Kokoh"],
        "makna_kartu": "Fondasi keteraturan, perlindungan, dan stabilitas kekuasaan rasional. Melambangkan figur pelindung yang membangun peradaban di atas aturan yang kokoh dan keadilan tertib.",
        "makna_pribadi": (
            "Garis tangan yang tegas dan lurus memperlihatkan karakter pemimpin berpendirian keras, terorganisir, "
            "dan dapat diandalkan saat terjadi krisis. Kamu tidak mudah goyah oleh omongan orang lain."
        ),
        "analisis_garis": {
            "hati": "Menunjukkan kasih melalui tindakan nyata, proteksi, dan tanggung jawab daripada sekadar kata-kata.",
            "kepala": "Sangat logis, terstruktur, disiplin, dan menghargai rencana yang terukur.",
            "kehidupan": "Daya tahan tubuh kokoh, memiliki disiplin fisik yang konsisten.",
            "nasib": "Garis nasib lurus dan kokoh seperti tiang pancang, menunjukkan figur pemimpin atau profesional mapan yang membangun otoritas kokoh dan disiplin tinggi."
        },
        "nasihat": "Kekuatan kepemimpinan sejati terletak pada kebijaksanaan melayani, bukan sekadar ketegasan memerintah."
    },
    5: {
        "id": 5,
        "name": "The Hierophant",
        "name_id": "Sang Penjaga Kebijaksanaan (The Hierophant)",
        "img": "m05.jpg",
        "keywords": ["Tradisi", "Bimbingan Spiritual", "Nilai Moral", "Pendidikan"],
        "makna_kartu": "Simbol jembatan antara dunia fana dan prinsip moral abadi. Mewakili pembelajaran dari guru bijak, penghormatan terhadap akar tradisi, dan pencarian makna hidup sejati.",
        "makna_pribadi": (
            "Garis tangan yang proporsional dan tenang menandakan orang yang dihormati karena integritas, "
            "sering menjadi tempat bertanya atau pemberi nasihat bagi keluarga dan teman."
        ),
        "analisis_garis": {
            "hati": "Menghargai kesetiaan, nilai keluarga, dan komitmen jangka panjang.",
            "kepala": "Tertata, menghargai metodologi yang sudah teruji, tekun menuntut ilmu.",
            "kehidupan": "Garis hidup stabil, mencerminkan ritme kehidupan yang teratur dan tenang.",
            "nasib": "Garis nasib stabil berakar dari pangkal telapak, menandakan karier yang sukses di bidang pendidikan, organisasi besar, atau lembaga berintegritas tinggi."
        },
        "nasihat": "Pegang teguh prinsip etikamu; integritas adalah mahkota yang paling berharga dalam perjalananmu."
    },
    6: {
        "id": 6,
        "name": "The Lovers",
        "name_id": "Sang Dua Sejoli (The Lovers)",
        "img": "m06.jpg",
        "keywords": ["Harmoni Hati", "Pilihan Moral", "Kemitraan Sejati", "Dua Jiwa"],
        "makna_kartu": "The Lovers bukan hanya tentang romantisme, tetapi tentang penyelarasan nilai batin dan keberanian mengambil pilihan moral yang sejalan dengan kata hati nurani.",
        "makna_pribadi": (
            "Garis hati dan garis kepalamu yang berjalan beriringan menandakan keseimbangan antara perasaan dan logika. "
            "Hubungan antarpribadi dan koneksi jiwa yang mendalam menjadi fondasi kebahagiaanmu."
        ),
        "analisis_garis": {
            "hati": "Sangat mendalam dalam berkomitmen, mencari keintiman emosional yang tulus dan bermakna.",
            "kepala": "Mampu menimbang sudut pandang orang lain sebelum membuat keputusan.",
            "kehidupan": "Energi positifmu terpancar kuat ketika kamu berada di lingkungan yang saling mendukung.",
            "nasib": "Garis nasib bersinergi dengan garis hati, menandakan kemajuan karier yang sangat dipengaruhi oleh kemitraan yang cocok dan keselarasan minat."
        },
        "nasihat": "Pilihlah jalan hidup yang selaras dengan nilai batinmu yang paling murni, tanpa mengorbankan dirimu."
    },
    7: {
        "id": 7,
        "name": "The Chariot",
        "name_id": "Kereta Tempur Kemenangan (The Chariot)",
        "img": "m07.jpg",
        "keywords": ["Tekad Baja", "Fokus Ambisi", "Menembus Rintangan", "Kendali Diri"],
        "makna_kartu": "Dua sphinx hitam dan putih yang ditarik ke satu arah melambangkan penaklukan konflik batin melalui tekad bulat dan fokus pantang menyerah hingga garis akhir kemenangan.",
        "makna_pribadi": (
            "Struktur garis tanganmu yang tegas menusuk menandakan ambisi yang membara. Ketika kamu sudah menetapkan "
            "satu target, hampir tidak ada rintangan yang mampu menghentikan langkahmu."
        ),
        "analisis_garis": {
            "hati": "Hasrat berkompetisi dan membuktikan diri sangat tinggi.",
            "kepala": "Fokus laser, tidak mudah teralihkan oleh keraguan diri atau omongan pesimistis.",
            "kehidupan": "Vitalitas tinggi, memiliki stamina kuat untuk bekerja keras melampaui batas.",
            "nasib": "Garis nasib menusuk kuat melintasi garis kepala, melambangkan perjalanan karier yang penuh perjuangan menaklukkan rintangan hingga mencapai posisi puncak."
        },
        "nasihat": "Kendalikan kecepatan dan emosimu; kemenangan terbesar diraih ketika tekad baja diimbangi kehati-hatian."
    },
    8: {
        "id": 8,
        "name": "Strength",
        "name_id": "Kekuatan Sejati (Strength)",
        "img": "m08.jpg",
        "keywords": ["Kelembutan Menaklukkan Amarah", "Ketabahan", "Keberanian Batin", "Kesabaran"],
        "makna_kartu": "Seorang wanita yang menjinakkan singa dengan belaian lembut. Kekuatan sejati bukanlah kekerasan fisik, melainkan kesabaran batin, kebaikan hati, dan penguasaan atas hawa nafsu.",
        "makna_pribadi": (
            "Garis kehidupanmu yang melingkar dalam menunjukkan ketabahan luar biasa. Kamu telah melewati berbagai "
            "ujian hidup yang berat tanpa kehilangan kehangatan dan kelembutan jiwamu."
        ),
        "analisis_garis": {
            "hati": "Penuh kasih yang tak tergoyahkan, mampu meredakan kemarahan orang lain dengan ketenangan.",
            "kepala": "Pikiran dewasa, mampu menahan diri dari reaksi spontan yang merugikan.",
            "kehidupan": "Daya hidup sangat tangguh, memiliki sistem pertahanan imun dan batin yang kokoh.",
            "nasib": "Garis nasib stabil dan ulet, menunjukkan karier yang dibangun melalui ketahanan batin, kesabaran menghadapi krisis, dan kepemimpinan berwibawa."
        },
        "nasihat": "Tetaplah lembut dalam menghadapi kekerasan dunia; kelembutanmu adalah senjata terkuatmu."
    },
    9: {
        "id": 9,
        "name": "The Hermit",
        "name_id": "Sang Petapa Bijak (The Hermit)",
        "img": "m09.jpg",
        "keywords": ["Kontemplasi", "Pencarian Jati Diri", "Lentera Kebenaran", "Kesendirian Bermakna"],
        "makna_kartu": "Orang tua yang berdiri di puncak salju dengan lentera bintang berujung enam. Mengajak kita mundur sejenak dari kebisingan dunia luar untuk mencari kebenaran hakiki di dalam diri.",
        "makna_pribadi": (
            "Garis kepalamu yang dalam dan melandai menandakan kamu seorang pemikir mendalam (deep thinker). "
            "Kamu memerlukan waktu hening sendiri untuk merenung, membaca, dan menemukan kembali kompas hidupmu."
        ),
        "analisis_garis": {
            "hati": "Selektif dalam pertemanan, lebih menyukai sedikit sahabat yang mendalam daripada keramaian semu.",
            "kepala": "Kapasitas intelektual dan filosofis sangat tinggi, selalu mencari alasan fundamental dari setiap fenomena.",
            "kehidupan": "Ritme hidup tenang, tahan dalam kesederhanaan dan fokus pada hal-hal esensial.",
            "nasib": "Garis nasib mandiri dan soliter, menandakan keberhasilan karier di bidang keahlian khusus yang membutuhkan konsentrasi mandiri dan integritas batin."
        },
        "nasihat": "Jangan takut menyendiri untuk sementara; lentera batinmu sedang bersiap menerangi jalan hidupmu ke depan."
    },
    10: {
        "id": 10,
        "name": "Wheel of Fortune",
        "name_id": "Roda Takdir (Wheel of Fortune)",
        "img": "m10.jpg",
        "keywords": ["Perubahan Takdir", "Peluang Baru", "Siklus Kehidupan", "Keberuntungan"],
        "makna_kartu": "Roda nasib yang berputar tanpa henti: yang di bawah akan naik, yang di atas akan berganti. Mengingatkan bahwa hidup adalah siklus alami dan keberuntungan berpihak pada yang siap berubah.",
        "makna_pribadi": (
            "Garis tanganmu yang seimbang dan fleksibel menandakan kamu memiliki daya adaptasi tinggi terhadap perubahan nasib. "
            "Kamu pandai menangkap momentum dan melihat celah keberuntungan di tengah ketidakpastian."
        ),
        "analisis_garis": {
            "hati": "Fleksibel dan tidak mudah terpuruk saat situasi berubah drastis.",
            "kepala": "Cepat menangkap pola tren baru dan tidak kaku mempertahankan cara lama yang usang.",
            "kehidupan": "Energi hidup mengalir dinamis mengikuti fase dan babak kehidupan.",
            "nasib": "Garis nasib memiliki beberapa percabangan dinamis, menandakan perjalanan karier yang penuh momentum keberuntungan dan pergantian babak yang menguntungkan."
        },
        "nasihat": "Persiapkan dirimu; roda takdir sedang bersiap membawamu naik ke fase baru yang lebih makmur."
    },
    11: {
        "id": 11,
        "name": "Justice",
        "name_id": "Keadilan (Justice)",
        "img": "m11.jpg",
        "keywords": ["Kejujuran Mutlak", "Keseimbangan", "Hukum Sebab-Akibat", "Ketegasan"],
        "makna_kartu": "Pedang bermata dua dan timbangan yang seimbang. Menegaskan hukum karma: setiap keputusan dan tindakan akan membuahkan hasil yang setimpal tanpa pilih kasih.",
        "makna_pribadi": (
            "Garis tanganmu yang tegas dan simetris mencerminkan kepribadian adil, objektif, dan jujur. "
            "Kamu tidak menyukai kemunafikan dan selalu menimbang fakta sebelum menghakimi."
        ),
        "analisis_garis": {
            "hati": "Menjunjung tinggi etika dan kesetaraan dalam setiap hubungan emosional.",
            "kepala": "Logika tajam dan tidak memihak, mampu membedakan fakta objektif dari opini semata.",
            "kehidupan": "Pola hidup seimbang antara hak dan kewajiban, istirahat dan kerja.",
            "nasib": "Garis nasib simetris dan tegas, menandakan kesuksesan di bidang hukum, manajemen, audit, atau pekerjaan yang menuntut kejujuran dan ketepatan tinggi."
        },
        "nasihat": "Bersikaplah jujur pada dirimu sendiri; keputusan yang adil hari ini akan melindungimu di masa depan."
    },
    12: {
        "id": 12,
        "name": "The Hanged Man",
        "name_id": "Sang Pria Tergantung (The Hanged Man)",
        "img": "m12.jpg",
        "keywords": ["Sudut Pandang Baru", "Keikhlasan", "Jeda Bijak", "Pencerahan"],
        "makna_kartu": "Tergantung dengan tenang di pohon dunia dengan lingkaran cahaya di kepala. Melambangkan kerelaan melepaskan ego demi memperoleh pemahaman spiritual dan sudut pandang yang jauh lebih tinggi.",
        "makna_pribadi": (
            "Garis tanganmu menunjukkan kemampuan langka untuk melihat masalah dari perspektif terbalik yang tidak disadari orang lain. "
            "Kamu memiliki keikhlasan batin untuk mengalah demi kebaikan jangka panjang."
        ),
        "analisis_garis": {
            "hati": "Sangat sabar dan rela berkorban demi orang atau cita-cita yang kamu yakini.",
            "kepala": "Kreativitas lateral yang unik, mampu menemukan solusi yang melampaui pola pikir arus utama.",
            "kehidupan": "Kemampuan regenerasi tinggi saat sedang beristirahat atau mengambil jeda hidup.",
            "nasib": "Garis nasib mengambil jalur memutar atau unik, menunjukkan fase jeda strategis yang justru melahirkan terobosan karier tak terduga."
        },
        "nasihat": "Jika keadaan terasa macet, jangan memaksa maju; ubahlah sudut pandangmu, pencerahan akan segera hadir."
    },
    13: {
        "id": 13,
        "name": "Death",
        "name_id": "Transformasi Jiwa (Death)",
        "img": "m13.jpg",
        "keywords": ["Kelahiran Kembali", "Akhir Babak Lama", "Evolusi Diri", "Pembaruan"],
        "makna_kartu": "Kartu ini BUKAN kematian fisik, melainkan simbol mistis berakhirnya fase hidup lama secara total agar bunga kehidupan baru yang lebih indah dapat mekar merekah.",
        "makna_pribadi": (
            "Garis kehidupanmu yang kokoh menandakan ketahanan luar biasa untuk bangkit dari setiap titik terendah. "
            "Kamu adalah sosok yang mampu mendefinisikan ulang dirimu menjadi versi yang jauh lebih kuat."
        ),
        "analisis_garis": {
            "hati": "Mampu melepaskan keterikatan emosi masa lalu demi memulai lembaran baru.",
            "kepala": "Pikiran yang berani merombak kebiasaan buruk yang sudah tidak relevan.",
            "kehidupan": "Daya hidup dengan kemampuan pemulihan di atas rata-rata.",
            "nasib": "Garis nasib mengalami pembaruan titik arah, menandakan keberanian banting setir karier atau transformasi besar menuju profesi yang lebih bermakna."
        },
        "nasihat": "Lepaskan hal-hal yang sudah layu dalam hidupmu; ruang kosong yang kamu buat akan segera diisi keajaiban baru."
    },
    14: {
        "id": 14,
        "name": "Temperance",
        "name_id": "Penyelarasan Diri (Temperance)",
        "img": "m14.jpg",
        "keywords": ["Keseimbangan Jiwa", "Moderasi", "Penyembuhan", "Sinergi Harmonis"],
        "makna_kartu": "Malaikat yang menuangkan air di antara dua bejana emas tanpa setetes pun tumpah. Simbol perpaduan sempurna antara emosi dan logika, bumi dan langit, menciptakan kedamaian yang menyembuhkan.",
        "makna_pribadi": (
            "Aliran garis tanganmu yang harmonis menandakan pribadi yang menyejukkan. Kamu adalah penengah alami "
            "yang mampu menyatukan perbedaan dan menciptakan ketenangan di lingkungan sekitarmu."
        ),
        "analisis_garis": {
            "hati": "Ketenangan emosional yang stabil, tidak mudah terprovokasi drama sesaat.",
            "kepala": "Pendekatan diplomatis, bijak memadukan berbagai sudut pandang yang berbeda.",
            "kehidupan": "Kesehatan fisik dan psikis yang terjaga lewat pola hidup seimbang.",
            "nasib": "Garis nasib tenang dan mengalir seimbang, menunjukkan karier yang stabil, terhindar dari konflik besar, dan menjadi jembatan penghubung banyak pihak."
        },
        "nasihat": "Kunci keberhasilanmu ada pada jalan tengah dan kesabaran; jaga ritme hidupmu tetap harmonis."
    },
    15: {
        "id": 15,
        "name": "The Devil",
        "name_id": "Hasrat & Keterikatan (The Devil)",
        "img": "m15.jpg",
        "keywords": ["Ambisi Membara", "Hasrat Material", "Pelepasan Belenggu", "Kekuatan Tersembunyi"],
        "makna_kartu": "Dua manusia yang dirantai longgar di depan takhta Baphomet. Menggambarkan godaan hasrat duniawi, ambisi kekuasaan, dan ilusi keterikatan yang sebenarnya bisa dilepaskan kapan saja.",
        "makna_pribadi": (
            "Garis tanganmu yang tebal dan tajam menunjukkan energi ambisi yang luar biasa kuat. "
            "Kamu memiliki daya pikat magnetis dan dorongan besar untuk mencapai kemakmuran material."
        ),
        "analisis_garis": {
            "hati": "Gairah emosi yang sangat intens dan mendalam, kadang posesif terhadap apa yang dicintai.",
            "kepala": "Sangat cerdas dalam melihat peluang keuntungan materi dan strategi bisnis.",
            "kehidupan": "Daya hidup fisik yang penuh gelora dan tidak mudah lelah mengejar target.",
            "nasib": "Garis nasib tebal dan berenergi intens, menandakan dorongan ambisi finansial tinggi, insting bisnis tajam, dan daya saing yang agresif."
        },
        "nasihat": "Sadari batasanmu; jadikan ambisimu sebagai pelayan kebaikan, bukan tuan yang membelenggu jiwamu."
    },
    16: {
        "id": 16,
        "name": "The Tower",
        "name_id": "Runtuhnya Menara (The Tower)",
        "img": "m16.jpg",
        "keywords": ["Pembebasan Tiba-Tiba", "Pencerahan Kilat", "Runtuhnya Kepalsuan", "Rekonstruksi"],
        "makna_kartu": "Petir menyambar mahkota menara batu, menghancurkan fondasi ilusi. Menandakan guncangan tak terduga yang bertujuan meruntuhkan kepalsuan agar kamu dapat membangun masa depan di atas fondasi kebenaran mutlak.",
        "makna_pribadi": (
            "Garis tanganmu yang dinamis mencerminkan jiwa yang berani menghadapi kenyataan pahit tanpa menutup mata. "
            "Kamu memiliki kepekaan untuk segera keluar dari zona nyaman palsu demi pertumbuhan sejati."
        ),
        "analisis_garis": {
            "hati": "Kejujuran emosional yang berani, lebih memilih kebenaran yang menyakitkan daripada kebohongan manis.",
            "kepala": "Kemampuan berpikir cepat di saat krisis mendadak terjadi.",
            "kehidupan": "Daya adaptasi kilat dalam situasi yang serba tak menentu.",
            "nasib": "Garis nasib menunjukkan kemampuan bangkit dan membangun kembali karier dengan fondasi yang jauh lebih kokoh setelah peristiwa perombakan besar."
        },
        "nasihat": "Jangan takut jika ada rencana yang berantakan; semesta sedang merobohkan hal rapuh untuk memberi jalan pada yang sejati."
    },
    17: {
        "id": 17,
        "name": "The Star",
        "name_id": "Sang Bintang Harapan (The Star)",
        "img": "m17.jpg",
        "keywords": ["Harapan Terang", "Inspirasi Murni", "Pemulihan Batin", "Kedamaian"],
        "makna_kartu": "Gadis telanjang menuangkan air penyembuhan di bawah naungan delapan bintang gemerlap. Merupakan kartu harapan murni setelah badai berlalu, membawa kedamaian jiwa dan inspirasi artistik tak terbatas.",
        "makna_pribadi": (
            "Garis hatimu yang jernih dan melengkung ke atas menandakan optimisme sejati dan hati yang bersih. "
            "Kamu adalah pembawa harapan dan lentera terang bagi orang-orang yang sedang berada dalam kegelapan."
        ),
        "analisis_garis": {
            "hati": "Ketulusan cinta tanpa syarat, penuh harapan positif bagi masa depan.",
            "kepala": "Imajinasi artistik yang kaya dan visi masa depan yang cerah.",
            "kehidupan": "Energi pemulihan yang menyejukkan, memancarkan kedamaian alami.",
            "nasib": "Garis nasib terang dan bercabang ke arah bukit Apollo, menandakan panggilan karier yang membawa inspirasi, pengakuan publik, dan apresiasi karya."
        },
        "nasihat": "Pertahankan harapan dan keyakinanmu; impian yang kamu pupuk dengan tulus sedang bergerak mendekat."
    },
    18: {
        "id": 18,
        "name": "The Moon",
        "name_id": "Sang Rembulan Malam (The Moon)",
        "img": "m18.jpg",
        "keywords": ["Alam Bawah Sadar", "Imajinasi Liar", "Menguak Ilusi", "Misteri Jiwa"],
        "makna_kartu": "Anjing dan serigala melolong ke arah bulan purnama di jalan setapak berkelok. Melambangkan wilayah mimpi, ilusi ketakutan bawah sadar, dan perjalanan batin menembus kabut keraguan.",
        "makna_pribadi": (
            "Garis kepalamu yang melandai ke arah bukit bulan menandakan daya imajinasi liar dan kepekaan artistik luar biasa. "
            "Kamu mampu merasakan getaran hal-hal yang tak kasat mata di sekelilingmu."
        ),
        "analisis_garis": {
            "hati": "Dunia perasaan yang sangat luas dan berlapis, rentan terhadap suasana hati yang berganti.",
            "kepala": "Sangat intuitif, imajinatif, dan berbakat di bidang seni, sastra, atau psikologi.",
            "kehidupan": "Vitalitas dipengaruhi oleh ketenangan pikiran dan siklus istirahat batin.",
            "nasib": "Garis nasib berakar dari bukit Bulan (Luna), menandakan bakat sukses di industri kreatif, seni, imajinasi, atau pemahaman psikologi manusia."
        },
        "nasihat": "Jangan biarkan kecemasan imajiner menakutimu; tataplah kabut ketakutan itu, ia akan pudar diterpa fajar."
    },
    19: {
        "id": 19,
        "name": "The Sun",
        "name_id": "Sang Mentari Kejayaan (The Sun)",
        "img": "m19.jpg",
        "keywords": ["Vitalitas Murni", "Keberhasilan Bersinar", "Keceriaan Jiwa", "Kejelasan"],
        "makna_kartu": "Seorang anak kecil tersenyum di atas kuda putih di bawah pancaran matahari emas raksasa. Kartu paling positif dalam Tarot: melambangkan vitalitas penuh, kesuksesan gemilang, kebahagiaan sejati, dan optimisme.",
        "makna_pribadi": (
            "Garis-garis tanganmu tampak bertenaga dan tegas. Kamu memancarkan aura kehangatan, "
            "vitalitas tinggi, dan pesona alami yang mampu menghidupkan suasana di mana pun kamu berada."
        ),
        "analisis_garis": {
            "hati": "Gembira, terbuka, murah senyum, dan memancarkan energi kasih yang hangat.",
            "kepala": "Pikiran cerdas, optimis, jelas, dan selalu fokus pada solusi terbaik.",
            "kehidupan": "Stamina fisik luar biasa, vitalitas prima, dan daya tahan tubuh yang tangguh.",
            "nasib": "Garis nasib bersinar jelas dan bertenaga, melambangkan puncak pencapaian karier, rekognisi luas, dan kepuasan hidup yang membanggakan."
        },
        "nasihat": "Pancarkan sinarmu tanpa ragu; saatnya kamu melangkah maju dan menikmati hasil kerja kerasmu."
    },
    20: {
        "id": 20,
        "name": "Judgement",
        "name_id": "Panggilan Nurani / Kebangkitan (Judgement)",
        "img": "m20.jpg",
        "keywords": ["Kebangkitan Jiwa", "Panggilan Hidup", "Evaluasi Masa Lalu", "Kedewasaan Baru"],
        "makna_kartu": "Malaikat meniup terompet kebangkitan emas, membuka peti kubur manusia lama untuk menyambut kehidupan abadi. Simbol titik balik hidup di mana kamu dipanggil untuk mencapai tujuan hidup yang lebih mulia.",
        "makna_pribadi": (
            "Garis tanganmu mencerminkan momen transformasi kedewasaan. Kamu sedang atau akan segera mengalami "
            "panggilan nurani yang mengubah cara pandangmu terhadap arti hidup secara mendalam."
        ),
        "analisis_garis": {
            "hati": "Telah berdamai dengan masa lalu dan siap menerima takdir dengan rasa syukur.",
            "kepala": "Kesadaran diri yang sangat matang, mampu mengevaluasi kesalahan tanpa menyalahkan orang lain.",
            "kehidupan": "Energi hidup diperbarui, siap melangkah ke babak kehidupan yang lebih bermakna.",
            "nasib": "Garis nasib menandai titik kebangkitan profesional, panggilan hidup sejati yang menuntutmu menggunakan seluruh potensi terbaikmu."
        },
        "nasihat": "Jawablah panggilan nuranimu; jangan ragu meninggalkan versi dirimu yang lama demi masa depan yang lebih agung."
    },
    21: {
        "id": 21,
        "name": "The World",
        "name_id": "Kelengkapan Semesta (The World)",
        "img": "m21.jpg",
        "keywords": ["Pencapaian Paripurna", "Siklus Sempurna", "Kelengkapan Jiwa", "Perayaan"],
        "makna_kartu": "Sosok penari kosmik di dalam karangan bunga laurel hijau yang dijaga empat makhluk suci. Melambangkan pencapaian puncak perjalanan jiwa: integrasi total antara tubuh, pikiran, dan rasa di alam semesta.",
        "makna_pribadi": (
            "Garis tanganmu yang utuh, panjang, dan harmonis mencerminkan pencapaian kematangan pribadi yang menyeluruh. "
            "Kamu memiliki keseimbangan luar biasa antara dunia emosional, kecerdasan rasional, dan stamina fisik."
        ),
        "analisis_garis": {
            "hati": "Kedewasaan emosional yang stabil, penuh welas asih dan penerimaan utuh.",
            "kepala": "Wawasan luas, kebijaksanaan praktis, dan pemikiran komprehensif.",
            "kehidupan": "Vitalitas yang utuh dan selaras dengan ritme alam semesta.",
            "nasib": "Garis nasib lengkap dan menyatu harmonis dengan ketiga garis lainnya, mencerminkan pemenuhan tujuan hidup dan kepuasan karier paripurna."
        },
        "nasihat": "Rayakan setiap langkah yang telah kamu selesaikan; kamu sudah lengkap dan siap menyongsong horizon baru dunia."
    }
}


def map_lines_to_tarot(features: dict) -> dict:
    """
    Petakan fitur 4 garis (Heart, Head, Life, Fate) ke salah satu dari 22 Kartu Major Arcana.
    """
    h_cat = features.get('heart', {}).get('category', 'medium')
    hd_cat = features.get('head', {}).get('category', 'medium')
    l_cat = features.get('life', {}).get('category', 'medium')
    f_cat = features.get('fate', {}).get('category', 'faint')

    cat_weights = {'absent': 1, 'faint': 1, 'thin': 1, 'medium': 2, 'thick': 3}
    w_h = cat_weights.get(h_cat, 2)
    w_hd = cat_weights.get(hd_cat, 2)
    w_l = cat_weights.get(l_cat, 2)
    w_f = cat_weights.get(f_cat, 1)

    raw_index = (w_h - 1) * 9 + (w_hd - 1) * 3 + (w_l - 1)

    # Modulasi halus Fate Line (w_f) & kontinuitas garis
    continuity = features.get('continuity_ratio', 0.5)
    adjusted_index = int(round(raw_index * 21.0 / 26.0 + (w_f - 2) * 1.5 + (continuity - 0.5) * 2.0))
    tarot_id = max(0, min(21, adjusted_index))

    # Kasus batas terintegrasi
    if w_h == 3 and w_hd == 3 and w_l == 3:
        tarot_id = 21 if (w_f >= 2 or continuity > 0.60) else 19
    elif w_h == 1 and w_hd == 1 and w_l == 1:
        tarot_id = 0 if (w_f <= 1) else 16

    card_data = TAROT_CARDS[tarot_id].copy()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    card_data["img_path"] = os.path.join(base_dir, "assets", "cards", card_data["img"])

    f_thick = features.get('fate', {}).get('thickness_val', 0.0)
    card_data["feature_summary"] = {
        "heart_line": f"{h_cat.upper()} ({features['heart']['thickness_val']:.2f} px)",
        "head_line": f"{hd_cat.upper()} ({features['head']['thickness_val']:.2f} px)",
        "life_line": f"{l_cat.upper()} ({features['life']['thickness_val']:.2f} px)",
        "fate_line": f"{f_cat.upper()} ({f_thick:.2f} px)",
        "continuity": f"{continuity * 100:.1f}%"
    }
    return card_data
