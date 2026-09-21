# Perbandingan Manual 3 Skenario RAG - WaqfRAG Chatbot



Model LLM: `gemini-3.6-flash` (model_choice="gemini")  

Skenario: (I) LLM Saja | (II) RAG tanpa Rerank | (III) RAG + Rerank  

Catatan: hasil ini untuk dibaca & dinilai manual, bukan output evaluasi otomatis (Ragas).



---

## Pertanyaan: Apa itu wakaf produktif?

### Skenario I - LLM Saja
**Wakaf Produktif** adalah skema pengelolaan harta benda wakaf yang dikembangkan dan dikelola secara komersial/bisnis, di mana keuntungan atau surplus dari hasil pengelolaan tersebut digunakan untuk kemaslahatan umat (kegiatan sosial, keagamaan, dan pemberdayaan ekonomi).

Sederhananya, jika pada **wakaf tradisional (konsumtif)** aset langsung dipakai (seperti membangun masjid atau pemakaman), maka pada **wakaf produktif**, aset tersebut "diputar" terlebih dahulu agar menghasilkan uang/nilai tambah secara terus-menerus.

---

### Prinsip Utama Wakaf Produktif
1. **Pokok Aset Harus Dijaga:** Harta wakaf (seperti tanah, gedung, atau modal uang) tidak boleh berkurang, dijual, dihibahkan, atau diwariskan.
2. **Dikelola Secara Bisnis:** Aset diproduktifkan melalui unit usaha yang menguntungkan dan sesuai syariat Islam.
3. **Hasilnya untuk Manfaat Sosial:** Keuntungan (profit) dari usaha tersebut disalurkan kepada penerima manfaat (*mauquf 'alaih*), seperti fakir miskin, beasiswa pendidikan, atau operasional rumah sakit.

---

### Contoh Wakaf Produktif

1. **Sektor Properti Komersial:**
   Seseorang mewakafkan sebidang tanah strategis. Pengelola wakaf (*Nazhir*) membangun ruko atau hotel di atas tanah tersebut. Keuntungan dari sewa ruko/hotel tersebut digunakan untuk membiayai sekolah gratis bagi anak miskin.

2. **Sektor Pertanian/Perkebunan:**
   Tanah wakaf ditanami kelapa sawit atau kurma. Hasil panennya dijual, dan keuntungannya digunakan untuk santunan anak yatim dan pemberdayaan ekonomi warga setempat.

3. **Wakaf Uang (Cash Waqf):**
   Masyarakat mengumpulkan wakaf dalam bentuk uang tunai. Uang tersebut diinvestasikan ke dalam instrumen keuangan syariah (seperti Sukuk Negara/SBSN atau deposito syariah). Imbal hasil (bagi hasil) dari investasi tersebut disalurkan untuk program kemanusiaan.

---

### Contoh Populer dalam Sejarah
Contoh paling terkenal adalah **Sumur Raumah milik Sahabat Nabi, Utsman bin Affan RA**. 
Utsman membeli sumur tersebut lalu mewakafkannya untuk warga Madinah. Seiring berjalannya waktu, kebun di sekitar sumur tersebut terus berkembang, dikelola secara produktif hingga saat ini, dan menghasilkan aset berupa perkebunan kurma serta hotel bintang lima di Madinah atas nama Utsman bin Affan.

---

### Keunggulan Wakaf Produktif
* **Manfaat Berkelanjutan (Sustainable):** Bantuan sosial tidak langsung habis, melainkan terus mengalir selama bisnis wakaf berjalan.
* **Mendorong Perekonomian Umat:** Membuka lapangan kerja baru dan menggerakkan roda ekonomi masyarakat.
* **Pahala Jariah yang Mengalir:** Wakif (orang yang mewakafkan) akan terus mendapatkan pahala selama aset wakaf tersebut memberikan manfaat.

### Skenario II - RAG tanpa Rerank
Wakaf produktif adalah konsep wakaf (yang mencakup uang, surat berharga, hingga aset produktif lainnya) yang dikelola secara profesional sehingga mampu menghasilkan manfaat ekonomi yang berkelanjutan (Sumber: Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1). 

Dalam konteks tanah wakaf, wakaf produktif diartikan sebagai pengelolaan tanah-tanah wakaf sehingga menghasilkan produk yang mempunyai nilai ekonomi (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 7).
Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):
- [Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] mewakafkan uang, surat berharga, hingga aset produktif lainnya.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Pengertian Wakaf
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 7] vi Himpunan Peraturan Perundang-undangan Tentang Wakaf
demikian, realitasnya masih jauh dari yang diharapkan.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Pengertian Wakaf
1.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 274] untuk mauquf alaih.
- [Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Dalam praktik wakaf, perhatian sering kali lebih banyak tertuju pada aset yang diwakafkan atau pihak
pengelola (nazhir).
- [1.-Peraturan-BWI-Nomor-1-Tahun-2008-Tentang-Prosedur-Penyusunan-Rekomendasi-Terhadap-Permohonan-PenukaranPerubahan-Status-Harta-Benda-Wakaf.pdf, Hal. 3] peruntukannya.
- [Peraturan-BWI-No.-1-Tahun-2008-Ruislag.pdf, Hal. 2] tulisan kepada Nazhir untuk mewakafkan harta benda miliknya.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] kepemilikannya atas harta tersebut kepada yang lain dan wakif berkewajiban menyedekahkan
manfaatnya serta tidak boleh menarik kembali wakafnya.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] mempergunakan manfaatnya untuk kebajikan.

### Skenario III - RAG + Rerank
Wakaf produktif adalah wakaf yang dikelola secara profesional sehingga mampu menghasilkan manfaat ekonomi yang berkelanjutan (Sumber: Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1). Selain itu, wakaf produktif juga diartikan sebagai pengelolaan aset atau tanah-tanah wakaf sehingga menghasilkan produk yang mempunyai nilai ekonomi (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 7).
Dokumen yang dipakai (top-3, dengan skor rerank):
- [Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9993) mewakafkan uang, surat berharga, hingga aset produktif lainnya.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9962) Pengertian Wakaf
1.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 7] (Rerank Score: 0.9917) vi Himpunan Peraturan Perundang-undangan Tentang Wakaf
demikian, realitasnya masih jauh dari yang diharapkan.

---

## Pertanyaan: Apa dasar hukum dan cara kerja wakaf uang di Indonesia?

### Skenario I - LLM Saja
**Wakaf Uang** adalah salah satu bentuk wakaf produktif di mana harta yang diwakafkan berupa uang tunai, yang kemudian dikelola secara produktif dan hasilnya dimanfaatkan untuk kesejahteraan umat.

Berikut adalah penjelasan lengkap mengenai **dasar hukum** dan **cara kerja** wakaf uang di Indonesia.

---

### A. Dasar Hukum Wakaf Uang di Indonesia

Wakaf uang memiliki landasan hukum yang kuat di Indonesia, baik dari sudut pandang hukum Islam (fatwa) maupun hukum positif (perundang-undangan negara).

#### 1. Fatwa Majelis Ulama Indonesia (MUI)
*   **Fatwa MUI tanggal 11 Mei 2002:** Menegaskan bahwa Wakaf Uang (*Cash Waqf/Waqf al-Nuqud*) hukumnya **JAWAZ (Boleh)**. 
*   Syarat utamanya: Nilai pokok wakaf uang **harus dijamin kelestariannya** (tidak boleh dijual, dihibahkan, ditagih, atau diwariskan) dan hanya hasil pengelolaannya yang boleh disalurkan.

#### 2. Undang-Undang Republik Indonesia
*   **UU No. 41 Tahun 2004 tentang Wakaf:** Ini adalah payung hukum utama. Pasal 28 hingga Pasal 31 secara khusus mengatur tentang *Wakaf Benda Bergerak Berupa Uang*.
    *   *Pasal 28:* Wakif dapat mewakafkan benda bergerak berupa uang melalui Lembaga Keuangan Syariah (LKS) yang ditunjuk oleh Menteri.

#### 3. Peraturan Pemerintah & Turunannya
*   **PP No. 42 Tahun 2006** tentang Pelaksanaan UU No. 41 Tahun 2004 tentang Wakaf.
*   **Peraturan Menteri Agama (PMA) No. 4 Tahun 2009** tentang Administrasi Pendaftaran Wakaf Uang.
*   **Peraturan Badan Wakaf Indonesia (BWI)** terkait pengelolaan dan pengembangan harta benda wakaf.

---

### B. Cara Kerja Wakaf Uang

Proses dan cara kerja wakaf uang melibatkan 4 pihak utama:
1.  **Wakif:** Orang/lembaga yang memberikan wakaf.
2.  **LKS-PWU (Lembaga Keuangan Syariah Penerima Wakaf Uang):** Bank Syariah yang ditunjuk pemerintah untuk menerima dana wakaf.
3.  **Nazhir:** Pengelola dana wakaf (bisa berupa badan/organisasi seperti BWI, Dompet Dhuafa, Rumah Zakat, dll).
4.  **Mauquf 'Alaih:** Penerima manfaat wakaf (masyarakat umum, fakir miskin, program pendidikan, dll).

#### Skema dan Tahapan Cara Kerja:

```text
[Wakif] ➡️ (Setor Uang) ➡️ [LKS-PWU / Bank Syariah] ➡️ (Terbit Sertifikat Wakaf)
                                   |
                          (Dana Diteruskan)
                                   |
                                   ⬇️
                           [Nazhir Wakaf]
                                   |
                   (Investasi Produktif & Aman)
                                   |
                                   ⬇️
                       [Hasil / Keuntungan]
                                   |
                        (Disalurkan Ke Program)
                                   |
                                   ⬇️
                          [Mauquf 'Alaih]
```

1.  **Penyerahan Dana (Penyetoran):**
    *   Wakif datang ke Bank Syariah (LKS-PWU) atau menggunakan *platform digital* resmi.
    *   Wakif menyetorkan sejumlah uang dan mengucapkan pernyataan kehendak wakaf (*Ikrar Wakaf*).

2.  **Penerbitan Sertifikat (SWU):**
    *   LKS-PWU menerbitkan **Sertifikat Wakaf Uang (SWU)** sebagai bukti sah. SWU ini diserahkan kepada Wakif dan pembusannya dikirim ke Nazhir serta Badan Wakaf Indonesia (BWI).

3.  **Pengelolaan dan Investasi oleh Nazhir:**
    *   Dana wakaf uang dari Bank Syariah diserahkan kepada **Nazhir**.
    *   Nazhir wajib menginvestasikan dana pokok tersebut ke dalam instrument yang **aman dan produktif** berprinsip syariah. 
    *   *Contoh investasi:* Sukuk Negara (Cash Waqf Linked Sukuk/CWLS), Deposito Syariah, atau pembiayaan usaha sektor riil berrisiko rendah.
    *   **Prinsip Utama:** Nilai pokok uang wakaf **TIDAK BOLEH BERKURANG** sedikit pun.

4.  **Penyaluran Hasil Pengelolaan (Bagi Hasil):**
    *   Keuntungan/bagi hasil dari investasi tersebut disalurkan untuk program pemberdayaan dan sosial (Pendidikan, Kesehatan, Ekonomi Mikro, Pembangunan Masjid, dll) kepada *Mauquf 'Alaih*.
    *   Nazhir berhak mendapatkan bagian (*operasional*) maksimal **10% dari hasil keuntungan** (bukan dari dana pokok) sebagai imbalan atas pengelolaannya.

---

### Ringkasan Prinsip Utamanya:
*   **Pokok Dana:** Tetap dan abadi (Diinvestasikan terus-menerus).
*   **Hasil Investasi:** Disalurkan untuk kemaslahatan umat (Penerima Manfaat).
*   **Fleksibilitas:** Mengingat bentuknya uang, wakaf jenis ini bisa dilakukan oleh siapa saja tanpa harus menunggu menjadi kaya raya (bisa dimulai dari nominal kecil, misalnya Rp10.000).

### Skenario II - RAG tanpa Rerank
Berikut adalah dasar hukum dan cara kerja wakaf uang di Indonesia berdasarkan dokumen yang disediakan:

### 1. Dasar Hukum Wakaf Uang di Indonesia
Dasar hukum perwakafan dan wakaf uang di Indonesia diatur melalui beberapa regulasi dan fatwa, antara lain:
* **Undang-Undang Nomor 41 Tahun 2004 tentang Wakaf** (Sumber: Undang-undang-No.-41-2004-Tentang-Wakaf.pdf, Hal: 2).
* **Fatwa MUI tentang Wakaf Uang** yang ditetapkan pada 11 Mei 2002 / 28 Shafar 1423 H (serta Fatwa DSN MUI) yang memutuskan bahwa wakaf uang hukumnya *jawaz* (boleh) (Sumber: Perbedaan Wakaf Uang dan Wakaf Melalui Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
* **Peraturan Menteri Agama Republik Indonesia Nomor 4 Tahun 2009** tentang Administrasi Pendaftaran Wakaf Uang (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 100, 274).
* **Peraturan Badan Wakaf Indonesia (BWI) No. 1 Tahun 2009** tentang Pedoman Pengelolaan dan Pengembangan Wakaf Uang (Sumber: Peraturan-BWI-No.-1-tahun-2009-tentang-Pedoman-Pengelolaan-dan-Pengembangan-Wakaf-Uang.pdf, Hal: 2).
* **Peraturan BWI No. 2 Tahun 2010** tentang Tata Cara Pendaftaran Nazhir Wakaf Uang (Sumber: Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2).
* **Peraturan BWI Nomor 1 Tahun 2020** (Sumber: 20210709-Research-Expose-Wakaf-Seri-6-Jadzil-Baihaqi-Penguatan-Akuntabilitas-Wakaf.pdf, Hal: 7).

---

### 2. Cara Kerja / Mekanisme Wakaf Uang
Cara kerja wakaf uang di Indonesia meliputi tahap-tahap dan ketentuan sebagai berikut:
1. **Penyerahan Dana oleh Wakif:** Wakif menyerahkan uang tunai (atau dalam bentuk surat-surat berharga) berupa rupiah kepada Nazhir dengan jumlah minimal satu juta rupiah. Wakif menentukan jangka waktu pemanfaatan (selamanya atau jangka waktu tertentu minimal 1 tahun) serta peruntukannya (Sumber: 20210709-Research-Expose-Wakaf-Seri-6-Jadzil-Baihaqi-Penguatan-Akuntabilitas-Wakaf.pdf, Hal: 7; Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
2. **Pengelolaan Produktif oleh Nazhir:** Nazhir mengelola dan mengembangkan uang wakaf tersebut secara produktif (Sumber: Peraturan-BWI-No.-1-tahun-2009-tentang-Pedoman-Pengelolaan-dan-Pengembangan-Wakaf-Uang.pdf, Hal: 2; 20210709-Research-Expose-Wakaf-Seri-6-Jadzil-Baihaqi-Penguatan-Akuntabilitas-Wakaf.pdf, Hal: 7).
3. **Penyertaan Pokok Wakaf:** Nilai pokok dari wakaf uang wajib dijamin kelestariannya dan tidak boleh dijual, dihibahkan, maupun diwariskan (Sumber: Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 3).
4. **Penyaluran Hasil Pengelolaan:** Hasil/keuntungan dari pengelolaan produktif tersebut disalurkan kepada *mauquf alaih* untuk hal-hal yang dibolehkan secara syar'i, baik guna keperluan ibadah maupun kesejahteraan umum menurut syariah (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 274; Perbedaan Wakaf Uang dan Wakaf Melalui Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 274] Himpunan Peraturan Perundang-undangan Tentang Wakaf
3.
- [Peraturan-BWI-No.-1-tahun-2009-tentang-Pedoman-Pengelolaan-dan-Pengembangan-Wakaf-Uang.pdf, Hal. 2] BAB I 
KETENTUAN UMUM 
Pasal 1 
Dalam Peraturan Badan Wakaf Indonesia ini yang dimaksud dengan : 
1.
- [Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Badan Wakaf Indonesia – Wakaf Uang di Indonesia
 Wakaf uang di Indonesia mulai dikenal sejak dikeluarkannya fatwa wakaf uang
oleh DSN MUI pada 2012.
- [Perbedaan Wakaf Uang dan Wakaf Melalui Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Wakaf uang adalah perbuatan hukum wakif untuk memisahkan dan/atau
menyerahkan sebagian uang miliknya dalam jangka waktu tertentu atau selamanya untuk dikelola
secara produktif yang hasilnya dimanfaatk...
- [Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal. 2] BAB I 
KETENTUAN UMUM 
 
Pasal 1 
Dalam Peraturan ini yang dimaksud dengan : 
1.
- [20210709-Research-Expose-Wakaf-Seri-6-Jadzil-Baihaqi-Penguatan-Akuntabilitas-Wakaf.pdf, Hal. 7] Peraturan BWI Nomor 1 Tahun 2020 membedakan antara wakaf uang dan 
wakaf melalui uang.
- [Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 3] Wakaf Uang (Cash Wakaf/Wagf al-Nuqud) adalah wakaf yang dilakukan seseorang, kelompok orang,
lembaga atau badan hukum dalam bentuk uang tunai.
- [Undang-undang-No.-41-2004-Tentang-Wakaf.pdf, Hal. 2] PRESIDEN 
REPUBLIK INDONESIA 
- 2 - 
 
 
 
MEMUTUSKAN : 
Menetapkan : UNDANG-UNDANG TENTANG WAKAF.
- [4.-Peraturan-BWI-Nomor-3-Tahun-2012-Tentang-Perubahan-Peruntukan-Harta-Benda-Wakaf.pdf, Hal. 3] BAB I 
KETENTUAN UMUM 
Pasal 1 
Dalam Peraturan Badan Wakaf Indonesia ini yang dimaksud dengan: 
1.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 100] 90 Himpunan Peraturan Perundang-undangan Tentang Wakaf
Presiden Nomor 9 Tahun 2005 tentang 
Kedudukan, Tugas, Fungsi, Susunan 
Organisasi dan Tata Kerja Kementerian 
Negara Republik Indonesia.
 4.

### Skenario III - RAG + Rerank
Berikut adalah dasar hukum dan cara kerja wakaf uang di Indonesia berdasarkan dokumen yang disediakan:

**Dasar Hukum Wakaf Uang:**
1. **Fatwa DSN MUI Tahun 2012**, yang menetapkan bahwa hukum wakaf uang adalah *jawaz* (boleh) (Sumber: Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
2. **Pendapat Imam al-Zuhri (w. 124H)**, yang menyatakan bahwa mewakafkan dinar hukumnya boleh (Sumber: Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 3).
3. **Peraturan BWI No. 2 Tahun 2010** tentang Tata Cara Pendaftaran Nazhir Wakaf Uang (Sumber: Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2).

**Cara Kerja Wakaf Uang:**
1. **Penyerahan Harta:** Wakif (seseorang, kelompok orang, lembaga, atau badan hukum) memisahkan atau menyerahkan uang tunai rupiah atau surat-surat berharga (Sumber: Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2).
2. **Pengelolaan dan Pengembangan:** Uang wakaf diterima oleh Nazhir untuk dikelola dan dikembangkan secara produktif, contohnya dengan menjadikannya sebagai modal usaha (Sumber: Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 3; Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2).
3. **Penyaluran Manfaat/Hasil:** Keuntungan atau hasil dari pengelolaan produktif tersebut disalurkan kepada *mauquf 'alaih* untuk hal-hal yang dibolehkan secara syar'i, seperti keperluan ibadah dan/atau kesejahteraan umum (Sumber: Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 3; Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2).
4. **Jaminan Kelestarian Pokok:** Nilai pokok dari wakaf uang wajib dijamin kelestariannya dan tidak boleh dijual, dihibahkan, atau diwariskan (Sumber: Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
Dokumen yang dipakai (top-3, dengan skor rerank):
- [Wakaf Uang di Indonesia - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9996) Badan Wakaf Indonesia – Wakaf Uang di Indonesia
 Wakaf uang di Indonesia mulai dikenal sejak dikeluarkannya fatwa wakaf uang
oleh DSN MUI pada 2012.
- [Apa Itu Wakaf Uang_ - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 3] (Rerank Score: 0.9994) Wakaf Uang (Cash Wakaf/Wagf al-Nuqud) adalah wakaf yang dilakukan seseorang, kelompok orang,
lembaga atau badan hukum dalam bentuk uang tunai.
- [Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal. 2] (Rerank Score: 0.9987) BAB I 
KETENTUAN UMUM 
 
Pasal 1 
Dalam Peraturan ini yang dimaksud dengan : 
1.

---

## Pertanyaan: Bagaimana hukum zakat fitrah?

### Skenario I - LLM Saja
Hukum zakat fitrah adalah **wajib** (*fardhu 'ain*) bagi setiap individu Muslim, baik laki-laki maupun perempuan, dewasa maupun anak-anak, bahkan bayi yang baru lahir sebelum matahari terbenam pada hari terakhir bulan Ramadan.

Berikut adalah rincian lengkap mengenai hukum dan ketentuan zakat fitrah:

### 1. Dalil Landasan Hukum
Kewajiban ini didasarkan pada hadis Nabi Muhammad SAW yang diriwayatkan oleh Abdullah bin Umar RA:

> *"Rasulullah SAW mewajibkan zakat fitrah satu sha' kurma atau satu sha' gandum atas umat Muslim, baik hamba sahaya maupun orang merdeka, laki-laki maupun perempuan, kecil maupun besar. Beliau memerintahkannya untuk ditunaikan sebelum orang-orang keluar menuju salat (Idulfitri)."* (HR. Bukhari dan Muslim)

### 2. Syarat Wajib Zakat Fitrah
Seseorang diwajibkan membayar zakat fitrah apabila memenuhi 3 syarat berikut:
1. **Beragama Islam.**
2. **Menemui sebagian waktu Ramadan dan awal Syawal.** Artinya, orang yang meninggal sebelum matahari terbenam di hari terakhir Ramadan, atau bayi yang lahir setelah matahari terbenam di hari terakhir Ramadan, tidak wajib zakat fitrah.
3. **Memiliki kelebihan makanan/harta** untuk diri dan keluarganya pada malam Hari Raya dan siang harinya.

### 3. Besaran Zakat Fitrah
* **Bentuk:** Makanan pokok yang berlaku di daerah setempat (di Indonesia umumnya berupa **beras**).
* **Jumlah:** **1 sha'**, yang jika dikonversi ke standar Indonesia adalah sekitar **2,5 kg atau 3,5 liter** beras per jiwa. (Beberapa ulama dan BAZNAS menyarankan 2,7 kg hingga 3 kg untuk kehati-hatian).
* **Pembayaran dengan Uang:** Menurut mazhab Hanafi dan pendapat yang difatwakan oleh MUI/BAZNAS, zakat fitrah **boleh dibayarkan dalam bentuk uang** senilai dengan harga beras/makanan pokok kualitas terbaik yang dikonsumsi sehari-hari.

### 4. Waktu Pembayaran
* **Waktu Mubah (Boleh):** Sejak awal bulan Ramadan hingga hari terakhir Ramadan.
* **Waktu Wajib:** Sejak terbenamnya matahari di akhir bulan Ramadan (malam takbiran) hingga sebelum salat Idulfitri.
* **Waktu Afdal (Utama):** Setelah salat Subuh di hari Idulfitri sampai sebelum pelaksanaan salat Idulfitri.
* **Waktu Makruh:** Membayar zakat fitrah setelah salat Idulfitri tetapi sebelum matahari terbenam pada hari Idulfitri.
* **Waktu Haram:** Membayar zakat fitrah setelah hari Idulfitri berakhir (tanpa alasan yang dibenarkan). Pembayaran setelah waktu ini hanya bernilai **sedekah biasa**, bukan zakat fitrah, dan orang tersebut berdosa karena menunda-nunda.

### 5. Hikmah Zakat Fitrah
1. **Menyucikan orang yang berpuasa** dari kata-kata yang tidak berguna atau perbuatan dosa kecil selama bulan Ramadan.
2. **Memberi makan fakir miskin** agar mereka juga dapat merasakan kegembiraan pada hari Raya Idulfitri bersama umat Muslim lainnya.

### Skenario II - RAG tanpa Rerank
Maaf, informasi tidak ditemukan dalam dokumen wakaf produktif yang tersedia.
Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):
- [Perbedaan Wakaf, Zakat, Infak, dan Sedekah - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Pada dasarnya wakaf, zakat, infak, dan sedekah sama-sama merupakan suatu
pemberian (tabarru’) untuk mengharapkan pahala dan ridha Allah.
- [Perbedaan Wakaf, Zakat, Infak, dan Sedekah - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Hukum sunah wajib sunah sunah
Waktu fleksibel ditentukan fleksibel fleksibel
Penerima
manfaat fleksibel Ditentukan
8 golongan fleksibel fleksibel
Harta bendanya
dikelola dulu, baru
disalurkan
manfaatn...
- [PBWI-1-2020.pdf, Hal. 4] sesuai prinsip syariah, termasuk mengelola zakat, 
infaq/sedekah, dan wakaf.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 38] berikut :
1.
- [Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal. 2] HIMPUNAN FATWA MAJELIS ULAMA INDONESIA
0
Islam di Indonesia, Bukuk III, Bab I, Pasal 
215, (1) dan (4));
sehingga atas dasar pengertian tersebut, 
bagi mereka hukum wakaf uang ( waqf al-
nuqud, cash...
- [9.-Peraturan-Ketua-Badan-Pelaksana-BWI-Nomor-1Bp-Tahun-2021-Tentang-Kenazhiran-Badan-Wakaf-Indonesia.pdf, Hal. 3] BAB I 
KETENTUAN UMUM 
Pasal 1 
(1) Wakaf adalah perbuatan hukum wakif untuk memisahkan 
dan/atau menyerahkan sebagian harta benda miliknya untuk 
dimanfaatkan selamanya atau untuk jangka waktu terten...
- [3.-Peraturan-Nomor-25-Tahun-2018-Tentang-Wakaf.pdf, Hal. 3] tertentu sesuai dengan kepentingannya guna keperluan 
ibadah dan/atau kesejahteraan umum menurut Syariah.
- [Peraturan Pemerintah RI Nomor 42 Tahun 2006 Tentang Pelaksanaan Undang-Undang Nomor 41 Tahun 2004 Tentang Wakaf.pdf, Hal. 31] - 2 -
2.
- [1.-Peraturan-BWI-Nomor-1-Tahun-2008-Tentang-Prosedur-Penyusunan-Rekomendasi-Terhadap-Permohonan-PenukaranPerubahan-Status-Harta-Benda-Wakaf.pdf, Hal. 3] Dalam Peraturan Badan Wakaf Indo nesia ini yang dimaksud 
dengan: 
1.
- [Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal. 3] 0
“Orang yang menafkahkan hartanya 
di jalan Allah, kemudian mereka tidak 
mengiringi apa yang dinafkahkannya itu 
dengan menyebut-nyebut pemberiannya 
dan dengan tidak menyakiti (perasaan 
penerima...

### Skenario III - RAG + Rerank
Maaf, informasi tidak ditemukan dalam dokumen wakaf produktif yang tersedia.
Dokumen yang dipakai (top-3, dengan skor rerank):
- [Perbedaan Wakaf, Zakat, Infak, dan Sedekah - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9541) Pada dasarnya wakaf, zakat, infak, dan sedekah sama-sama merupakan suatu
pemberian (tabarru’) untuk mengharapkan pahala dan ridha Allah.
- [Perbedaan Wakaf, Zakat, Infak, dan Sedekah - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.8967) Hukum sunah wajib sunah sunah
Waktu fleksibel ditentukan fleksibel fleksibel
Penerima
manfaat fleksibel Ditentukan
8 golongan fleksibel fleksibel
Harta bendanya
dikelola dulu, baru
disalurkan
manfaatn...
- [9.-Peraturan-Ketua-Badan-Pelaksana-BWI-Nomor-1Bp-Tahun-2021-Tentang-Kenazhiran-Badan-Wakaf-Indonesia.pdf, Hal. 3] (Rerank Score: 0.8155) BAB I 
KETENTUAN UMUM 
Pasal 1 
(1) Wakaf adalah perbuatan hukum wakif untuk memisahkan 
dan/atau menyerahkan sebagian harta benda miliknya untuk 
dimanfaatkan selamanya atau untuk jangka waktu terten...

---

## Pertanyaan: Apa perbedaan wakaf produktif dengan wakaf konsumtif?

### Skenario I - LLM Saja
Perbedaan utama antara **wakaf produktif** dan **wakaf konsumtif** terletak pada **cara pengelolaan aset wakaf** dan **bagaimana manfaat (hasil) wakaf tersebut disalurkan** kepada penerima manfaat (*mauquf 'alaih*).

Berikut adalah penjelasan rincinya:

---

### 1. Wakaf Konsumtif (Wakaf Langsung)
Wakaf konsumtif adalah benda/aset wakaf yang **langsung dimanfaatkan secara langsung** oleh masyarakat untuk pelayanan ibadah, sosial, atau pendidikan, tanpa diputar terlebih dahulu untuk menghasilkan keuntungan finansial secara bisnis.

* **Cara Kerja:** Aset diberikan $\rightarrow$ Langsung digunakan/dikonsumsi manfaatnya oleh penerima.
* **Tujuan Utama:** Menyediakan fasilitas publik atau pelayanan sosial mendasar secara gratis.
* **Contoh:**
  * Tanah yang dibangun menjadi **masjid** atau mushola.
  * Bangunan yang dijadikan **sekolah/pesantren** gratis.
  * Lahan untuk **pemakaman umum** (TPU).
  * Mobil **ambulans** untuk mengantar orang sakit secara gratis.

---

### 2. Wakaf Produktif (Wakaf Investasi)
Wakaf produktif adalah benda/aset wakaf yang **dikelola secara komersial atau dikembangkan melalui kegiatan ekonomi** (seperti bisnis, investasi, atau persewaan). Keuntungan (*surplus*) dari hasil pengelolaan itulah yang kemudian disalurkan kepada penerima manfaat.

* **Cara Kerja:** Aset diberikan $\rightarrow$ Dikelola secara bisnis/diinvestasikan $\rightarrow$ Menghasilkan keuntungan $\rightarrow$ Keuntungan disalurkan untuk masyarakat.
* **Tujuan Utama:** Menjaga aset pokok tetap utuh (bahkan bertambah) sambil menghasilkan dana secara berkelanjutan untuk memberdayakan ekonomi umat.
* **Contoh:**
  * **Ruko atau Gedung:** Dikelola untuk disewakan, hasil uang sewanya digunakan untuk membiayai beasiswa anak yatim.
  * **Lahan Pertanian/Perkebunan:** Ditanami kelapa sawit atau padi secara profesional, hasil penjualannya digunakan untuk membiayai operasional rumah sakit gratis.
  * **Wakaf Uang:** Dana tunai diinvestasikan pada instrumen syariah (seperti Sukuk/SBSN), bagi hasilnya digunakan untuk pemberdayaan UMKM.

---

### Perbandingan Ringkas

| Aspek | Wakaf Konsumtif | Wakaf Produktif |
| :--- | :--- | :--- |
| **Bentuk Manfaat** | Langsung berupa fasilitas/pelayanan. | Berupa hasil usaha/keuntungan finansial. |
| **Pengelolaan** | Tidak berorientasi bisnis/keuntungan. | Berorientasi komersial & profesional (*profit-generating*). |
| **Sifat Nilai Aset** | Cenderung menyusut seiring waktu (karena dipakai). | Berpotensi terus berkembang dan bertambah. |
| **Dampak Ekonomi** | Membantu kebutuhan jangka pendek/fasilitas. | Menciptakan kemandirian ekonomi jangka panjang. |
| **Penerima Manfaat** | Pengguna fasilitas (misal: jemaah masjid, siswa). | Orang yang membutuhkan bantuan dana/program (misal: penerima beasiswa, penerima modal usaha). |

---

### Kesimpulan
Keduanya sama-sama memiliki pahala jariyah yang terus mengalir dan sangat dibutuhkan oleh umat. **Wakaf konsumtif** penting untuk memenuhi kebutuhan sarana ibadah dan sosial dasar, sedangkan **wakaf produktif** sangat penting untuk memperkuat perekonomian umat dan menjamin keberlanjutan pendanaan program-program sosial.

### Skenario II - RAG tanpa Rerank
Berdasarkan konteks dokumen yang disediakan, informasi mengenai **wakaf produktif** adalah sebagai berikut:

* **Wakaf Produktif** adalah wakaf yang dikelola secara profesional sehingga mampu menghasilkan manfaat ekonomi yang berkelanjutan (Sumber: Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1). 
* Konsep wakaf produktif juga mencakup pengelolaan aset-aset wakaf (seperti tanah wakaf) sehingga menghasilkan produk yang mempunyai nilai ekonomi (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 7).

Adapun istilah **wakaf konsumtif** beserta perbandingannya secara spesifik tidak ditemukan dalam dokumen yang tersedia.
Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Pengertian Wakaf
- [Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] mewakafkan uang, surat berharga, hingga aset produktif lainnya.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Pengertian Wakaf
1.
- [Jenis Harta Benda Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] Uang
Logam mulia
Surat berharga seperti saham dan sukuk 
Kendaraan 
Hak atas kekayaan intelektual 
Hak sewa
Benda bergerak lain sesuai ketentuan syariah
Jenis benda bergerak ini memberikan fleksibilit...
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] mempergunakan manfaatnya untuk kebajikan.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] kepemilikannya atas harta tersebut kepada yang lain dan wakif berkewajiban menyedekahkan
manfaatnya serta tidak boleh menarik kembali wakafnya.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 7] vi Himpunan Peraturan Perundang-undangan Tentang Wakaf
demikian, realitasnya masih jauh dari yang diharapkan.
- [Pengertian Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] memberikannya kepada mauquf’alaih.
- [20210709-Research-Expose-Wakaf-Seri-6-Jadzil-Baihaqi-Penguatan-Akuntabilitas-Wakaf.pdf, Hal. 7] Peraturan BWI Nomor 1 Tahun 2020 membedakan antara wakaf uang dan 
wakaf melalui uang.
- [3.-Peraturan-Nomor-25-Tahun-2018-Tentang-Wakaf.pdf, Hal. 3] tertentu sesuai dengan kepentingannya guna keperluan 
ibadah dan/atau kesejahteraan umum menurut Syariah.

### Skenario III - RAG + Rerank
Maaf, informasi tidak ditemukan dalam dokumen wakaf produktif yang tersedia.
Dokumen yang dipakai (top-3, dengan skor rerank):
- [20210709-Research-Expose-Wakaf-Seri-6-Jadzil-Baihaqi-Penguatan-Akuntabilitas-Wakaf.pdf, Hal. 7] (Rerank Score: 0.9947) Peraturan BWI Nomor 1 Tahun 2020 membedakan antara wakaf uang dan 
wakaf melalui uang.
- [Pengertian Wakif - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9905) mewakafkan uang, surat berharga, hingga aset produktif lainnya.
- [Jenis Harta Benda Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] (Rerank Score: 0.9861) Uang
Logam mulia
Surat berharga seperti saham dan sukuk 
Kendaraan 
Hak atas kekayaan intelektual 
Hak sewa
Benda bergerak lain sesuai ketentuan syariah
Jenis benda bergerak ini memberikan fleksibilit...

---

## Pertanyaan: Siapa saja sahabat Nabi yang mewakafkan hartanya?

### Skenario I - LLM Saja
Tradisi wakaf di dalam Islam sudah dimulai sejak zaman Rasulullah SAW dan dilanjutkan oleh para sahabatnya. Bahkan, Jabir bin Abdillah RA pernah berkata: 

> *"Tidak ada seorang pun dari sahabat Nabi SAW yang memiliki kemampuan (harta), melainkan mereka mewakafkan hartanya."*

Berikut adalah beberapa sahabat Nabi yang paling terkenal dengan kebiasaan mewakafkan hartanya beserta bentuk wakaf mereka:

### 1. Umar bin Khattab RA
Umar bin Khattab adalah sahabat yang pertama kali mencatatkan syariat wakaf secara rasmi dalam fikih Islam. 
* **Harta yang diwakafkan:** Tanah subur di **Khaibar** yang sangat dicintainya.
* **Kisah:** Umar bertanya kepada Rasulullah SAW cara terbaik memanfaatkan tanah tersebut. Rasulullah bersabda: *"Tahan pokoknya (jangan dijual, dihibahkan, atau diwariskan) dan sedekahkan hasilnya."* Hasil tanah tersebut diwakafkan untuk fakir miskin, karabat, pembebasan budak, tamu, dan orang yang sedang dalam perjalanan.

### 2. Uthman bin Affan RA
Uthman dikenal sebagai salah satu sahabat yang paling dermawan. Wakaf beliau bahkan manfaatnya masih terasa dan dikelola hingga hari ini di Arab Saudi.
* **Harta yang diwakafkan:** **Sumur Rauma (Sumur Ruma)**.
* **Kisah:** Saat umat Islam migrasi ke Madinah, mereka kesulitan air bersih. Sumur milik seorang warga Yahudi dijual dengan harga sangat mahal. Uthman membelinya dengan harga tinggi lalu mewakafkannya untuk seluruh penduduk Madinah, baik Muslim maupun non-Muslim, secara gratis. Selain itu, Uthman juga mewakafkan tanah untuk perluasan Masjid Nabawi.

### 3. Abu Talha al-Anshari RA
Abu Talha adalah salah satu sahabat Anshar yang paling kaya di Madinah.
* **Harta yang diwakafkan:** **Kebun Bairaha’**, sebuah kebun kurma paling indah dan paling dicintainya yang berada tepat di depan Masjid Nabawi.
* **Kisah:** Beliau mewakafkannya tepat setelah turun firman Allah SWT dalam Surah Ali 'Imran ayat 92: *"Kamu tidak akan memperoleh kebajikan (yang sempurna) sebelum kamu menginfakkan sebagian harta yang kamu cintai."*

### 4. Ali bin Abi Talib RA
* **Harta yang diwakafkan:** Tanah di kawasan **Yanbu** yang memiliki mata air jernih. Ali mengelola tanah tersebut dan mewakafkan hasilnya untuk kaum fakir dan miskin.

### 5. Abu Bakar as-Siddiq RA
* **Harta yang diwakafkan:** Abu Bakar mewakafkan rumahnya di Makkah untuk dipergunakan oleh keturunannya yang membutuhkan serta untuk kepentingan umat Islam.

### 6. Zubair bin al-Awwam RA
* **Harta yang diwakafkan:** Rumah-rumahnya yang ada di Madinah. Beliau mensyaratkan bahwa rumah tersebut boleh ditinggali oleh anak-anak perempuannya yang tercerai atau membutuhkan bantuan tanpa boleh dijual.

### 7. Sa'ad bin Abi Waqqas RA
* **Harta yang diwakafkan:** Rumah dan tanahnya di kawasan Istas (dekat Madinah) yang diperuntukkan bagi kesejahteraan masyarakat Islam.

### 8. Istri-Istri Nabi (Aisyah, Hafshah, Ummu Salamah, dll.)
* **Harta yang diwakafkan:**
  * **Aisyah RA** mewakafkan rumah yang dibelinya dari Muawiyah untuk kepentingan kemanusiaan.
  * **Hafshah binti Umar RA** mewakafkan tanah yang diperolehnya dari ayahnya (Umar bin Khattab) di Khaibar.

---

**Kesimpulan:**
Praktik wakaf dilakukan oleh hampir seluruh sahabat Nabi yang memiliki harta, baik laki-laki maupun perempuan, sahabat Muhajirin maupun Anshar. Bentuk wakaf mereka bervariasi, mulai dari tanah, sumur air, kebun kurma, hingga bangunan (rumah).

### Skenario II - RAG tanpa Rerank
Berdasarkan dokumen yang disediakan, berikut adalah sahabat-sahabat Nabi yang tercatat mewakafkan hartanya:

1. **Umar bin Khattab**: Mewakafkan sebidang tanah/kebun (seratus saham) di Khaibar (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal: 5).
2. **Abu Thalhah (Zaid bin Sahl)**: Mewakafkan kebun kesayangan dan terbaiknya, yaitu Kebun Bairaha / Bairuha' (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Kisah Inspirasi Abu Thalhah Wakaf Kebun Bairahu Abu - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
3. **Utsman**: Menyedekahkan/mewakafkan hartanya di Khaibar (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
4. **Ali bin Abi Thalib**: Mewakafkan tanahnya yang subur (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
5. **Mu’ad bin Jabal**: Mewakafkan rumahnya yang populer dengan sebutan “Dar Al-Anshar” (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
6. **Anas bin Malik** (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
7. **Abdullah bin Umar** (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
8. **Zubair bin Awwam** (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
9. **Aisyah (istri Rasulullah SAW)** (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
10. **Abu Bakar**: Mewakafkan sebidang tanahnya di Makkah yang diperuntukkan bagi anak keturunannya yang datang ke Makkah (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).

Selain itu, Jabir r.a. menyatakan bahwa tidak ada seorang sahabat Rasul pun yang memiliki kemampuan melainkan berwakaf (Sumber: Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal: 5).
Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):
- [Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal. 3] 0
“Orang yang menafkahkan hartanya 
di jalan Allah, kemudian mereka tidak 
mengiringi apa yang dinafkahkannya itu 
dengan menyebut-nyebut pemberiannya 
dan dengan tidak menyakiti (perasaan 
penerima...
- [Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] masjid nabawi.Dengan demikian, Rasulullah telah mewakafkan tanah untuk pembangunan masjid.
- [Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] Sahabat Utsman menyedekahkan hartanya di Khaibar.
- [Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] kebun kesayangannya, kebun Bairaha.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 100] memisahkan dan/atau menyerahkan sebagian uang miliknya 
untuk dimanfaatkan selamanya atau untuk jangka waktu 
tertentu sesuai dengan kepentingannya guna keperluan 
ibadah dan/atau kesejahteraan umum m...
- [Sejarah Awal Mula Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] kaum kerabat, hamba sahaya, sabilillah Ibnu sabil, dan tamu, dan tidak dilarang bagi yang mengelola
(nazhir) wakaf makan dari hasilnya dengan cara yang baik (sepantasnya) atau member makan orang
lain...
- [Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal. 5] 0
5.
- [Kisah Inspirasi Abu Thalhah Wakaf Kebun Bairahu Abu - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Dikisahkan, Abu Thalhah (Zaid bin Sahl) seorang sahabat dari kalangan Anshar yang memiliki kebun
bernama Bairuha’ yang terletak tidak jauh dari Masjid Madinah, sebagai harta paling dicintai dan
dibang...
- [Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal. 5] ﻭﺍﻟﺪﺭﺍﻫﻴﻢ

ﺍﺣﺒﺲﺃﺻﻠﻬﺎﻭﺳﺒﻞﲦﺮ 

ﺣﻳﺑﺃﹶﺻ ﺑﹺﻘﹶﻄﹾﻊﹺ 
ﺭﻣﻣﻣ.
1.
- [Sejarah Perkembangan Wakaf - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Umar, sedangkan orang-orang Ansor mengatakan adalah wakaf Rasulullah SAW.” (Asy-Syaukani: 129).

### Skenario III - RAG + Rerank
Berdasarkan konteks dokumen yang disediakan, berikut adalah para sahabat Nabi yang mewakafkan hartanya:

1. **Umar bin Khattab**: Mewakafkan sebidang tanah/kebun yang dimilikinya di Khaibar (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal: 5).
2. **Abu Thalhah**: Mewakafkan kebun kesayangan dan terbaik yang dimilikinya (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1).
3. **Sahabat Utsman**: Menyedekahkan hartanya di Khaibar (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
4. **Ali bin Abi Thalib**: Mewakafkan tanahnya yang subur (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
5. **Mu’ad bin Jabal**: Mewakafkan rumahnya yang populer dengan sebutan “Dar Al-Anshar” (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
6. **Anas bin Malik**: Melaksanakan/menyusul pelaksanaan wakaf (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
7. **Abdullah bin Umar**: Melaksanakan/menyusul pelaksanaan wakaf (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
8. **Zubair bin Awwam**: Melaksanakan/menyusul pelaksanaan wakaf (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
9. **Aisyah (Istri Rasulullah SAW)**: Melaksanakan/menyusul pelaksanaan wakaf (Sumber: Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
Dokumen yang dipakai (top-3, dengan skor rerank):
- [Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] (Rerank Score: 0.9977) Sahabat Utsman menyedekahkan hartanya di Khaibar.
- [Fatwa-MUI-tentang-Wakaf-Uang.pdf, Hal. 5] (Rerank Score: 0.9947) 0
5.
- [Wakaf Produktif Di Zaman Rasulullah SAW & Para Sahabat - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9945) masjid nabawi.Dengan demikian, Rasulullah telah mewakafkan tanah untuk pembangunan masjid.

---

## Pertanyaan: Apa syarat menjadi Nazhir wakaf uang?

### Skenario I - LLM Saja
Syarat menjadi **Nazhir Wakaf Uang** (pengelola wakaf uang) di Indonesia diatur dalam **Undang-Undang No. 41 Tahun 2004 tentang Wakaf**, **Peraturan Pemerintah (PP) No. 42 Tahun 2006**, serta **Peraturan Badan Wakaf Indonesia (BWI)**.

Mengingat pengelolaan wakaf uang membutuhkan keahlian manajemen keuangan yang baik agar nilainya tidak berkurang dan dapat diinvestasikan, syarat untuk Nazhir Wakaf Uang cukup ketat.

Nazhir dibedakan menjadi 3 kategori: **Perorangan**, **Organisasi**, dan **Badan Hukum**. Namun, untuk wakaf uang, umumnya BWI mendorong dan lebih banyak mengesahkan Nazhir berstatus **Badan Hukum** atau **Organisasi** demi profesionalitas.

Berikut adalah rincian syarat-syaratnya:

---

### 1. Syarat Umum Nazhir (Perorangan)
Jika berbentuk perorangan (minimal terdiri dari 3 orang), para pengurusnya harus memenuhi syarat:
1. **Warga Negara Indonesia (WNI)**.
2. **Beragama Islam**.
3. **Dewasa** (baligh).
4. **Sehat jasmani dan rohani**.
5. **Tidak terhalang melakukan perbuatan hukum** (tidak dalam pengampuan atau bangkrut/pailit).
6. **Amanah, adil, bertanggung jawab**, dan memiliki reputasi baik.
7. Memiliki **kemampuan dan pengetahuan** dalam mengelola harta benda wakaf (khususnya manajemen keuangan syariah untuk wakaf uang).

---

### 2. Syarat Nazhir Organisasi
Jika Nazhir berbentuk Organisasi, syaratnya adalah:
1. Pengurus organisasi harus memenuhi **syarat umum perorangan** di atas.
2. Organisasi bergerak di bidang **sosial, pendidikan, kemasyarakatan, dan/atau keagamaan Islam**.
3. Memiliki **struktur organisasi dan tata kerja** yang jelas.
4. Memiliki pengurus yang berdomisili di wilayah hukum Republik Indonesia.

---

### 3. Syarat Nazhir Badan Hukum (Paling Direkomendasikan untuk Wakaf Uang)
Nazhir berbentuk badan hukum (seperti Yayasan atau Koperasi Syariah) harus memenuhi syarat:
1. Pengurus badan hukum memenuhi **syarat umum perorangan**.
2. Merupakan **Badan Hukum Indonesia** yang dibentuk sesuai dengan peraturan perundang-undangan yang berlaku.
3. Badan hukum tersebut bergerak di bidang **sosial, pendidikan, kemasyarakatan, dan/atau keagamaan Islam**.
4. Memiliki **anggaran dasar (AD/ART)** yang memuat kegiatan pengelolaan wakaf.
5. Memiliki **kemampuan finansial dan manajemen** untuk mengelola investasi wakaf uang secara aman dan produktif.

---

### 4. Syarat Khusus Administrasi & Operasional Nazhir Wakaf Uang

Selain syarat kelembagaan di atas, untuk dapat mengelola **wakaf uang secara resmi**, Nazhir wajib memenuhi syarat operasional berikut:

1. **Terdaftar Resmi di BWI (Badan Wakaf Indonesia):**
   Nazhir wajib mengajukan permohonan pendaftaran dan mendapatkan Surat Tanda Bukti Pendaftaran Nazhir (STBPN) dari BWI Pusat.

2. **Bekerja Sama dengan LKS-PWU:**
   Nazhir wajib membuka rekening wakaf uang di **Lembaga Keuangan Syariah Penerima Wakaf Uang (LKS-PWU)** yang telah ditunjuk oleh Menteri Agama (seperti Bank Syariah).

3. **Memiliki Program Kerja yang Jelas:**
   Nazhir harus menyerahkan proposal rencana pengelolaan dan penyerapan dana wakaf (rencana investasi yang aman dan rencana penyaluran manfaat/nadzarah).

4. **Kapasitas Manajemen Risiko & Akuntabilitas:**
   Nazhir wakaf uang dituntut memiliki kemampuan pelaporan keuangan yang transparan, siap diaudit, dan menjamin bahwa **nilai pokok wakaf uang tidak boleh berkurang atau hilang**.

---

### Ringkasan Langkah Menjadi Nazhir Wakaf Uang:
1. Membentuk kelembagaan (disarankan berupa Yayasan/Badan Hukum yang sah).
2. Memyiapkan SDM pengurus yang kompeten di bidang keuangan syariah.
3. Mengajukan pendaftaran Nazhir Wakaf Uang ke **Badan Wakaf Indonesia (BWI)**.
4. Setelah disetujui BWI, membuka rekening operasional wakaf uang di **LKS-PWU** (Bank Syariah).
5. Mulai dapat menghimpun dan mengelola wakaf uang dari masyarakat.

### Skenario II - RAG tanpa Rerank
Berdasarkan dokumen-dokumen yang disediakan, syarat untuk menjadi Nazhir wakaf uang meliputi:

**1. Pendaftaran dan Ketentuan Umum**
* Calon Nazhir Wakaf Uang wajib mendaftarkan diri kepada Badan Wakaf Indonesia (BWI) dan memenuhi persyaratan Nazhir sesuai Undang-Undang Nomor 41 Tahun 2004 tentang Wakaf dan Peraturan Pemerintah Nomor 42 Tahun 2006 (Sumber: Persyaratan Pendaftaran Nazhir Wakaf Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 1; HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 275; Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2).

**2. Persyaratan Kualifikasi, Kompetensi, dan SDM**
* **Kompetensi Keuangan:** Memiliki kompetensi dalam pengelolaan keuangan yang meliputi pengetahuan di bidang keuangan syariah, kemampuan pengelolaan keuangan, dan pengalaman di bidang pengelolaan keuangan (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 275; Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal: 2; HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 359).
* **Komitmen & Pengalaman:** Memiliki kemampuan, pengalaman, dan komitmen tinggi dalam pemberdayaan ekonomi umat serta pengembangan Wakaf Uang yang sehat, transparan, dan akuntabel (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 359).
* **Sertifikasi Profesioanal:** Memiliki SDM yang bersertifikasi profesi Nazhir / Sertifikat Kompetensi Bidang Pengelola Wakaf minimal 2 orang (Sumber: Pendaftaran Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2; HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 359).
* **Kemitraan:** Memiliki dukungan kerja sama dengan manajer investasi sebagaimana diatur dalam Undang-Undang Nomor 8 Tahun 1995 tentang Pasar Modal (Sumber: HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal: 359).

**3. Persyaratan Berkas dan Finansial**
* Memiliki biaya operasional minimal Rp30.000.000 yang dibuktikan dengan melampirkan buku rekening (Sumber: Pendaftaran Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
* Melengkapi berkas pendaftaran: Akta Pendirian, Company Profile Yayasan/Organisasi, Dokumen NPWP, Pengesahan Kemenkumham, Dokumen Rekomendasi LKS-PWU, Surat Keterangan Domisili dari Kelurahan, Rekomendasi BWI perwakilan Provinsi/Kota/Kabupaten, dan Rencana kerja (Sumber: Pendaftaran Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).
* Melampirkan surat-surat pernyataan/permohonan meliputi: Surat Permohonan, Surat Kesediaan Setia kepada NKRI, Surat Pernyataan Bersedia Diaudit, Surat Pernyataan Laporan Wakaf Bulanan, dan Surat Pernyataan Laporan Pelaksanaan Wakaf per 6 bulan (Sumber: Pendaftaran Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal: 2).

**4. Persyaratan Dasar Nazhir (Perseorangan atau Organisasi)**
* **Jika Perseorangan:** Warga Negara Indonesia, beragama Islam, dewasa, amanah, mampu secara jasmani dan rohani, tidak terhalang melakukan perbuatan hukum, salah seorang Nazhir bertempat tinggal di kecamatan tempat benda wakaf berada, serta memiliki program kerja pengelolaan/pengembangan wakaf (Sumber: Peraturan-BWI-No.-3-Tahun-2008-Penggantian-Nazhir.pdf, Hal: 4).
* **Jika Organisasi:** Pengurus memenuhi syarat Nazhir perseorangan, organisasi bergerak di bidang sosial/pendidikan/kemasyarakatan/keagamaan Islam, salah satu pengurus berdomisili di kabupaten/kota letak benda wakaf, serta memiliki salinan akta notaris pendirian/AD-ART dan daftar susunan pengurus (Sumber: Peraturan-BWI-No.-3-Tahun-2008-Penggantian-Nazhir.pdf, Hal: 4).
Dokumen yang dipakai (tanpa skor rerank, tampilkan judul + 1 kalimat awal saja):
- [Persyaratan Pendaftaran Nazhir Wakaf Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Persyaratan Pendaftaran Nazhir Wakaf Uang Di Badan Wakaf Indonesia
 Berdasarkan Undang-Undang Nomor 41 Tahun 2004.
- [Syarat dan Ketentuan Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] Dalam perbincangan seputar wakaf, seringkali kita mendengar istilah Nazhir.
- [Persyaratan Pendaftaran Nazhir Wakaf Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] adalah wakaf berupa uang dalam bentuk rupiah yang dapat dikelola secara produktif, hasilnya
dimanfaatkan untuk penerima (Mauquf ‘Alaih).
- [Pendaftaran Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 2] sesuai dengan jenis wakaf dan bentuk nazhir, yaitu:
1.
- [Peraturan Pemerintah RI Nomor 42 Tahun 2006 Tentang Pelaksanaan Undang-Undang Nomor 41 Tahun 2004 Tentang Wakaf.pdf, Hal. 30] perwakafan, BWI, dan Lembaga Keuangan Syariah, sekaligus menghindari
berbagai kemungkinan perbedaan penafsiran terhadap ketentuan yang
berlaku.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 275] Himpunan Peraturan Perundang-undangan Tentang Wakaf
BAB II
PERSYARATAN PENDAFTARAN NAZHIR WAKAF UANG 
 Pasal 2 
(1) Calon Nazhir Wakaf Uang wajib mendaftarkan diri kepada 
BWI dan memenuhi persyaratan...
- [Peraturan-BWI-No.-2-Tahun-2010-Tentang-Tata-Cara-Pendaftaran-Nazhir-Wakaf-Uang.pdf, Hal. 2] pelaksanaan tugasnya untuk mengembangkan perwakafan di Indonesia.
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 300] uang sesuai dengan tujuan, fungsi dan peruntukannya.
- [Peraturan-BWI-No.-3-Tahun-2008-Penggantian-Nazhir.pdf, Hal. 4] 1) memenuhi persyaratan Nazhir perseorangan , yaitu: warga Negara Indonesia, 
beragama Islam, dewasa, amanah, mampu secara jasmani dan rohani, dan tidak 
terhalang melakukan perbuatan hukum; 
2) salah...
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 359] Himpunan Peraturan Perundang-undangan Tentang Wakaf
Nazhir sesuai ketentuan peraturan perundang-undangan 
yang berlaku; 
b.

### Skenario III - RAG + Rerank
Error dalam proses generasi jawaban oleh LLM (gemini): Error calling model 'gemini-3.6-flash' (RESOURCE_EXHAUSTED): 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.6-flash\nPlease retry in 31.621620667s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-3.6-flash'}, 'quotaValue': '20'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '31s'}]}}
Dokumen yang dipakai (top-3, dengan skor rerank):
- [HIMPUNAN - Peraturan-Perundangan-Wakaf-2022.pdf, Hal. 275] (Rerank Score: 0.9997) Himpunan Peraturan Perundang-undangan Tentang Wakaf
BAB II
PERSYARATAN PENDAFTARAN NAZHIR WAKAF UANG 
 Pasal 2 
(1) Calon Nazhir Wakaf Uang wajib mendaftarkan diri kepada 
BWI dan memenuhi persyaratan...
- [Syarat dan Ketentuan Nazhir - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9996) Dalam perbincangan seputar wakaf, seringkali kita mendengar istilah Nazhir.
- [Persyaratan Pendaftaran Nazhir Wakaf Uang - Badan Wakaf Indonesia _ BWI.go.id.pdf, Hal. 1] (Rerank Score: 0.9995) Persyaratan Pendaftaran Nazhir Wakaf Uang Di Badan Wakaf Indonesia
 Berdasarkan Undang-Undang Nomor 41 Tahun 2004.

---
