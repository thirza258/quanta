"""Original course: Financial Literacy for MSMEs (Literasi Keuangan UMKM).

Practical financial foundations, cash flow forecasting, break-even analysis,
working capital management, loan evaluation, and Indonesian UMKM tax treatment.
Bilingual Indonesian and English content.
"""

from foundations import question


def build_msme_financial_literacy():
    modules = [
        {
            "id": "23.1",
            "part": "1",
            "title": "Mengapa UMKM Gagal Karena Arus Kas, Bukan Profit",
            "subtitle": "Mengapa UMKM Gagal Karena Arus Kas, Bukan Karena Profit di Catatan",
            "minutes": 18,
            "objective": "Membedakan laba akuntansi dan arus kas riil, serta mengenali bagaimana warung yang tampak untung bisa kehabisan uang kas.",
            "kind": "fundamentals",
            "formula": r"\text{Kas Bersih} = \text{Kas Awal} + \text{Penerimaan Kas Riil} - \text{Pengeluaran Kas Riil}",
            "code": (
                "# Menghitung selisih laba akuntansi vs kas riil\n"
                "omzet_tercatat = 30_000_000  # Termasuk piutang pelanggan\n"
                "piutang_belum_bayar = 12_000_000\n"
                "kas_masuk_riil = omzet_tercatat - piutang_belum_bayar\n"
                "biaya_operasional_tunai = 22_000_000\n"
                "laba_tercatat = omzet_tercatat - biaya_operasional_tunai\n"
                "kas_bersih = kas_masuk_riil - biaya_operasional_tunai\n"
                "print(f'Laba tercatat: Rp {laba_tercatat:,.0f}')\n"
                "print(f'Arus kas riil: Rp {kas_bersih:,.0f}')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Banyak pemilik usaha mikro, kecil, dan menengah (UMKM) bingung ketika buku catatan menunjukkan laba bersih puluhan juta rupiah, namun saldo rekening bank kosong dan mereka tidak mampu membayar tagihan listrik atau gaji karyawan esok hari. Fenomena ini disebut **insolvensi kas** (*cash flow insolvency*).\n\n"
                "Laba akuntansi (*accounting profit*) dihitung saat transaksi terjadi, meskipun pembeli belum membayar sepeser pun (penjualan kredit atau piutang). Sebaliknya, kas riil (*cash flow*) hanya bertambah saat uang tunai atau transfer benar-benar masuk ke rekening usaha Anda. Jika pengeluaran tunai untuk bahan baku, sewa, dan upah terjadi lebih cepat daripada pembayaran dari pelanggan, bisnis Anda bisa bangkrut meski produk sangat laris.\n\n"
                "$$\n"
                r"\text{Kas Bersih Akhir} = \text{Kas Awal} + \text{Penerimaan Kas Riil} - \text{Pengeluaran Kas Riil}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Warung Ibu Siti mencatat pesanan katering sebesar Rp30.000.000 bulan ini. Dari jumlah itu, Rp12.000.000 berupa piutang yang baru akan dibayar kantor pelanggan 45 hari lagi. Biaya bahan baku dan upah asisten dapur sebesar Rp22.000.000 harus dibayar tunai minggu ini.\n\n"
                "Di atas kertas, Ibu Siti mencatat laba Rp8.000.000 (Rp30.000.000 − Rp22.000.000). Namun secara kas riil, uang tunai yang masuk hanya Rp18.000.000 sementara kas keluar Rp22.000.000, menghasilkan defisit kas negatif Rp4.000.000. Tanpa cadangan kas awal, usaha akan terhenti.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Pisahkan tanggal pencatatan invoice dengan tanggal estimasi uang masuk ke rekening.\n"
                "2. Hitung hari ketahanan kas (*days of cash buffer*): bagi total kas likuid yang tersedia dengan rata-rata pengeluaran operasional harian. Pastikan kas tunai minimal menutup pengeluaran rutin 30 hari ke depan.\n"
                "3. Jangan gunakan laba di atas kertas sebagai acuan berbelanja modal sebelum uangnya diterima di bank.\n\n"
                "### In the sandbox\n\n"
                "Gunakan script simulasi Python untuk memasukkan omzet warung Anda dan lihat bagaimana penundaan piutang mengubah kas bersih menjadi negatif."
            ),
            "exercise": question(
                "Mengapa sebuah UMKM bisa mengalami krisis kas meskipun laporan bulanan menunjukkan laba bersih positif?",
                [
                    "Karena seluruh keuntungan disimpan dalam bentuk emas batangan fisik di brankas kantor pusat",
                    "Karena sebagian besar omzet masih berupa piutang yang belum cair sementara tagihan harus dibayar tunai",
                    "Karena tarif pemotongan pajak penghasilan UMKM dipungut di muka sebesar lima puluh persen per transaksi",
                ],
                1,
                "Laba dihitung saat penjualan terjadi, namun kas hanya bertambah saat uang fisik/transfer diterima. Jika kas keluar mendahului penagihan piutang, terjadi defisit kas operasional.",
            ),
            "exercises": [
                question(
                    "Mengapa sebuah UMKM bisa mengalami krisis kas meskipun laporan bulanan menunjukkan laba bersih positif?",
                    [
                        "Karena seluruh keuntungan disimpan dalam bentuk emas batangan fisik di brankas kantor pusat",
                        "Karena sebagian besar omzet masih berupa piutang yang belum cair sementara tagihan harus dibayar tunai",
                        "Karena tarif pemotongan pajak penghasilan UMKM dipungut di muka sebesar lima puluh persen per transaksi",
                    ],
                    1,
                    "Laba dihitung saat penjualan terjadi, namun kas hanya bertambah saat uang fisik/transfer diterima.",
                ),
                question(
                    "Manakah tindakan preventif terbaik untuk mencegah krisis kas akibat piutang tertunda?",
                    [
                        "Membeli persediaan inventaris tambahan dalam jumlah besar menggunakan pinjaman kredit berbunga tinggi",
                        "Menerapkan uang muka (DP) minimal 50% dan menetapkan batas waktu pelunasan yang ketat",
                        "Menghentikan seluruh pencatatan pengeluaran harian dan menutup rekening bank operasional",
                    ],
                    1,
                    "Menetapkan uang muka dan batas termin pembayaran memastikan kas operasional selalu tersedia untuk membeli bahan baku.",
                ),
            ],
            "terms": [
                {"term": "Arus Kas (Cash Flow)", "definition": "Aliran uang tunai riil yang masuk dan keluar dari rekening atau kas fisik usaha."},
                {"term": "Laba Akuntansi (Accounting Profit)", "definition": "Selisih antara pendapatan tercatat dan beban tercatat pada suatu periode, tidak bergantung pada waktu penerimaan uang."},
                {"term": "Piutang Usaha (Accounts Receivable)", "definition": "Hak klaim pembayaran uang atas barang atau jasa yang sudah diserahkan kepada pelanggan namun belum dibayar."},
            ],
            "references": [
                {"title": "Kementerian UMKM · Pedoman Pembukuan Sederhana Usaha Mikro", "url": "https://kemenkopukm.go.id"},
                {"title": "Bank Indonesia · Modul Pelatihan Pengelolaan Keuangan UMKM", "url": "https://www.bi.go.id/id/umkm/default.aspx"},
            ],
        },
        {
            "id": "23.2",
            "part": "1",
            "title": "Memisahkan Uang Pribadi & Rekening Usaha",
            "subtitle": "Memisahkan Uang Pribadi dan Rekening Usaha untuk Akuntabilitas",
            "minutes": 15,
            "objective": "Menerapkan pemisahan mutlak antara pengeluaran rumah tangga dan keuangan bisnis, serta menentukan gaji pemilik (prive disiplin).",
            "kind": "fundamentals",
            "formula": r"\text{Saldo Rekening Usaha} = \text{Kas Operasional} - \text{Gaji Resmi Pemilik (Prive Tetap)}",
            "code": (
                "# Menentukan gaji tetap pemilik vs laba ditahan usaha\n"
                "arus_kas_operasional_rata2 = 18_000_000\n"
                "gaji_layak_pemilik = 6_000_000  # Ditransfer ke rekening pribadi bulanan\n"
                "cadangan_kas_darurat = 4_000_000\n"
                "laba_ditahan_ekspansi = arus_kas_operasional_rata2 - gaji_layak_pemilik - cadangan_kas_darurat\n"
                "print(f'Gaji Pemilik Bulanan: Rp {gaji_layak_pemilik:,.0f}')\n"
                "print(f'Sisa Kas untuk Cadangan & Reinvestasi Usaha: Rp {laba_ditahan_ekspansi:,.0f}')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Kesalahan nomor satu yang membunuh UMKM pada tahun pertama adalah mencampuradukkan dompet pribadi dan laci kas usaha. Ketika pendapatan toko langsung dipakai belanja dapur keluarga atau bayar sekolah anak, pemilik kehilangan visibilitas apakah usahanya sebenarnya menguntungkan atau sedang menggerogoti modal awal (*capital erosion*).\n\n"
                "Langkah perbaikan paling fundamental adalah membuka **dua rekening terpisah**: satu rekening atas nama usaha untuk seluruh operasional, dan satu rekening pribadi untuk kebutuhan keluarga. Pemilik usaha tidak boleh mengambil uang kasir sembarangan; tetapkan **gaji bulanan tetap** bagi diri sendiri yang ditransfer pada tanggal tertentu.\n\n"
                "$$\n"
                r"\text{Sisa Kas Usaha} = \text{Kas Operasional Masuk} - \text{Biaya Usaha} - \text{Gaji Resmi Pemilik}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Budi memiliki toko online pakaian dengan arus kas masuk Rp25.000.000 per bulan. Belanja kulakan dan biaya sewa operasional adalah Rp15.000.000, menghasilkan kas operasional bersih Rp10.000.000.\n\n"
                "Sebelumnya, Budi mengambil kas sesuka hati hingga modal kulakan habis. Setelah mengikuti pelatihan, Budi membuka rekening baru khusus toko dan menetapkan gaji tetap sebesar Rp6.000.000 per bulan. Sisa kas operasional sebesar Rp4.000.000 disimpan di rekening usaha sebagai cadangan kas darurat dan modal kulakan partai besar berikutnya.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Buka rekening terpisah khusus operasional bisnis tanpa fasilitas kartu debit konsumtif.\n"
                "2. Hitung kebutuhan hidup keluarga minimal dan tetapkan sebagai gaji pemilik tetap.\n"
                "3. Jangan pernah membayar pengeluaran pribadi dengan uang kasir warung tanpa mencatatnya sebagai prive resmi.\n\n"
                "### In the sandbox\n\n"
                "Jalankan kode untuk mensimulasikan alokasi kas usaha antara gaji pemilik, cadangan likuiditas, dan modal ekspansi."
            ),
            "exercise": question(
                "Apa konsekuensi utama jika kas pribadi dan kas usaha bercampur dalam satu rekening?",
                [
                    "Biaya administrasi transfer kliring perbankan komersial menjadi berlipat ganda setiap transaksi bulanan",
                    "Pemilik tidak bisa melihat apakah bisnis menghasilkan keuntungan atau mengikis modal awal",
                    "Lembaga perbankan umum akan langsung membekukan rekening giro operasional secara permanen",
                ],
                1,
                "Pencampuran kas menyamarkan biaya riil hidup pemilik dan mengaburkan kinerja operasional bisnis yang sesungguhnya.",
            ),
            "exercises": [
                question(
                    "Apa konsekuensi utama jika kas pribadi dan kas usaha bercampur dalam satu rekening?",
                    [
                        "Biaya administrasi transfer kliring perbankan komersial menjadi berlipat ganda setiap transaksi bulanan",
                        "Pemilik tidak bisa melihat apakah bisnis menghasilkan keuntungan atau mengikis modal awal",
                        "Lembaga perbankan umum akan langsung membekukan rekening giro operasional secara permanen",
                    ],
                    1,
                    "Pencampuran kas menyamarkan biaya hidup pemilik dan mengaburkan kinerja operasional bisnis.",
                ),
            ],
            "terms": [
                {"term": "Entitas Terpisah (Separate Entity Concept)", "definition": "Prinsip akuntansi yang memperlakukan keuangan bisnis terpisah dari urusan pribadi pemiliknya."},
                {"term": "Prive (Drawings)", "definition": "Penarikan sejumlah dana dari kas usaha oleh pemilik untuk keperluan pribadi."},
                {"term": "Laba Ditahan (Retained Earnings)", "definition": "Bagian keuntungan bersih yang tidak dibagikan kepada pemilik melainkan ditahan untuk memperkuat modal usaha."},
            ],
            "references": [
                {"title": "OJK · Buku Saku Cerdas Mengelola Keuangan UMKM", "url": "https://sikapiuangmu.ojk.go.id"},
            ],
        },
        {
            "id": "23.3",
            "part": "1",
            "title": "Pencatatan Keuangan Praktis Saat Usaha Sibuk",
            "subtitle": "Pencatatan Keuangan Praktis yang Bertahan di Tengah Kesibukan Usaha",
            "minutes": 18,
            "objective": "Menerapkan buku log transaksi harian 1 halaman dan rutinitas rekonsiliasi kas harian dalam waktu kurang dari 10 menit.",
            "kind": "fundamentals",
            "formula": r"\text{Saldo Kas Akhir} = \text{Saldo Awal} + \sum \text{Pemasukan Harian} - \sum \text{Pengeluaran Harian}",
            "code": (
                "# Rekonsiliasi kas harian sederhana\n"
                "saldo_awal_pagi = 1_500_000  # Modal kembalian kasir (opening float)\n"
                "transaksi_masuk = [250_000, 480_000, 120_000, 650_000]  # Total masuk: 1.500.000\n"
                "transaksi_keluar = [180_000, 320_000]  # Total keluar: 500.000 (belanja bumbu dan gas)\n"
                "saldo_hitung = saldo_awal_pagi + sum(transaksi_masuk) - sum(transaksi_keluar)\n"
                "uang_fisik_di_laci = 2_500_000\n"
                "selisih = uang_fisik_di_laci - saldo_hitung\n"
                "print(f'Saldo Teoretis Catatan: Rp {saldo_hitung:,.0f}')\n"
                "print(f'Uang Fisik Aktual di Kasir: Rp {uang_fisik_di_laci:,.0f}')\n"
                "print(f'Selisih Kas: Rp {selisih:,.0f}')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Banyak pemilik usaha memulai pembukuan dengan software rumit atau jurnal berpuluh kolom, lalu menyerah setelah tiga hari karena kelelahan melayani pembeli. Pembukuan terbaik untuk UMKM bukanlah yang paling canggih, melainkan **yang dapat dilakukan secara konsisten setiap hari**.\n\n"
                "Gunakan metode log 1 halaman: catat hanya 6 kolom sederhana: Tanggal, Keterangan Transaksi, Kategori, Kas Masuk, Kas Keluar, dan Saldo. Di akhir hari (atau sebelum tutup toko), lakukan **rekonsiliasi kas**: hitung uang fisik di laci dan cocokkan dengan catatan. Latihan 5 menit ini mencegah kebocoran kas, pencurian, atau nota hilang.\n\n"
                "$$\n"
                r"\text{Saldo Kas Akhir} = \text{Saldo Awal} + \sum \text{Kas Masuk} - \sum \text{Kas Keluar}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Pak Joko mengelola warung kopi. Di pagi hari saldo laci Rp1.500.000 sebagai modal kembalian kasir (*opening float*). Selama hari itu ia mencatat 4 pemasukan total Rp1.500.000 dan 2 pengeluaran belanja bumbu Rp500.000. Saldo di catatan harusnya Rp2.500.000.\n\n"
                "Saat menghitung uang fisik di laci malam hari, jumlahnya tepat Rp2.500.000 (selisih nol). Jika uang fisik hanya Rp2.400.000, Pak Joko langsung tahu ada transaksi Rp100.000 yang lupa dicatat atau kembalian yang keliru, dan bisa segera dicari saat ingatannya masih segar.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Unduh template log transaksi 1-halaman (`transaction_log_template.csv`).\n"
                "2. Catat pengeluaran seketika saat uang diserahkan, jangan menunda hingga malam hari.\n"
                "3. Tutup buku harian dengan menghitung fisik kas laci kasir setiap pergantian shift atau tutup toko.\n\n"
                "### In the sandbox\n\n"
                "Jalankan script untuk menguji rekonsiliasi kas harian antara catatan jurnal dan uang kasir riil."
            ),
            "exercise": question(
                "Apa tujuan utama melakukan rekonsiliasi kas harian sebelum menutup toko?",
                [
                    "Memastikan tidak ada selisih antara uang fisik di laci dengan transaksi yang tercatat hari itu",
                    "Menghitung proyeksi laju inflasi makroekonomi nasional untuk perencanaan anggaran lima tahun mendatang",
                    "Menyusun berkas pelaporan surat pemberitahuan pajak tahunan badan usaha sesuai standar perundang-undangan",
                ],
                0,
                "Rekonsiliasi harian memastikan seluruh kas fisik cocok dengan catatan transaksi, mendeteksi kesalahan kembalian atau nota lupa catat seketika.",
            ),
            "exercises": [
                question(
                    "Apa tujuan utama melakukan rekonsiliasi kas harian sebelum menutup toko?",
                    [
                        "Memastikan tidak ada selisih antara uang fisik di laci dengan transaksi yang tercatat hari itu",
                        "Menghitung proyeksi laju inflasi makroekonomi nasional untuk perencanaan anggaran lima tahun mendatang",
                        "Menyusun berkas pelaporan surat pemberitahuan pajak tahunan badan usaha sesuai standar perundang-undangan",
                    ],
                    0,
                    "Rekonsiliasi harian mendeteksi selisih fisik kas saat ingatan masih segar.",
                ),
            ],
            "terms": [
                {"term": "Buku Kas Harian (Daily Cash Log)", "definition": "Catatan kronologis penerimaan dan pengeluaran uang tunai hari demi hari."},
                {"term": "Rekonsiliasi Kas (Cash Reconciliation)", "definition": "Proses pencocokan antara saldo uang fisik yang ada di brankas/laci dengan saldo di catatan buku kas."},
            ],
            "references": [
                {"title": "Kementerian UMKM · Modul Pencatatan Keuangan Sederhana", "url": "https://kemenkopukm.go.id"},
            ],
        },
        {
            "id": "23.4",
            "part": "2",
            "title": "Membaca Angka Sendiri: Arus Kas Masuk vs Kas Keluar",
            "subtitle": "Membaca Pola Arus Kas Masuk dan Keluar untuk Antisipasi Krisis",
            "minutes": 18,
            "objective": "Mengelompokkan arus kas ke dalam pos operasional, investasi, dan pendanaan, serta mengantisipasi pola musiman.",
            "kind": "fundamentals",
            "formula": r"\text{Arus Kas Operasional} = \text{Kas Penjualan} - \text{Kas Beban Pokok} - \text{Kas Beban Operasional}",
            "code": (
                "# Memilah 3 kategori arus kas: Operasional, Investasi, Pendanaan\n"
                "kas_operasional = -3_000_000  # Penjualan lesu dan belanja bahan baku tinggi\n"
                "kas_investasi = -2_000_000    # Pembelian mixer dan oven baru\n"
                "kas_pendanaan = 25_000_000    # Pencairan pinjaman KUR Rp25 juta\n"
                "perubahan_kas_total = kas_operasional + kas_investasi + kas_pendanaan\n"
                "print(f'Arus Kas Operasional: Rp {kas_operasional:,.0f}')\n"
                "print(f'Arus Kas Investasi:   Rp {kas_investasi:,.0f}')\n"
                "print(f'Arus Kas Pendanaan:   Rp {kas_pendanaan:,.0f}')\n"
                "print(f'Kenaikan Kas Bersih:  Rp {perubahan_kas_total:,.0f}')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Tidak semua uang yang masuk ke rekening usaha adalah hasil keringat penjualan produk. Uang masuk bisa berasal dari tiga sumber yang sangat berbeda:\n"
                "1. **Arus Kas Operasional**: Kas dari penjualan barang/jasa dikurangi pengeluaran operasional sehari-hari. Ini adalah mesin utama denyut nadi bisnis Anda.\n"
                "2. **Arus Kas Investasi**: Kas yang keluar untuk membeli peralatan produksi (mesin jahit, oven, etalase) atau kas masuk dari penjualan aset lama.\n"
                "3. **Arus Kas Pendanaan**: Kas masuk dari pencairan utang bank (KUR) atau setoran modal pemilik, serta kas keluar untuk membayar cicilan pokok pinjaman.\n\n"
                "Bisnis yang sehat adalah bisnis yang arus kas operasionalnya positif secara berkelanjutan. Jika kas Anda naik hanya karena menambah pinjaman baru, Anda sebenarnya sedang menumpuk kewajiban di masa depan.\n\n"
                "$$\n"
                r"\Delta \text{Kas} = \text{Kas Operasional} + \text{Kas Investasi} + \text{Kas Pendanaan}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Sebuah toko roti mencatat kenaikan saldo bank Rp20.000.000 bulan ini. Pemilik merasa tokonya sangat untung. Namun setelah diurai:\n"
                "- Kas operasional ternyata minus Rp3.000.000 (penjualan sepi, bahan baku naik).\n"
                "- Kas investasi minus Rp2.000.000 (beli mixer baru).\n"
                "- Kas pendanaan plus Rp25.000.000 (pencairan pinjaman KUR).\n\n"
                "Kenaikan saldo bank semata-mata ditopang oleh utang baru, bukan oleh kinerja operasional warung roti. Dengan memilah angka ini, pemilik segera tersadar untuk memperbaiki efisiensi produksi sebelum dana pinjaman habis tergerus.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Pisahkan pemasukan operasional dari pinjaman atau setoran modal pribadi.\n"
                "2. Pantau tren kas operasional 6 bulan berturut-turut.\n"
                "3. Jika kas operasional negatif 3 bulan berturut-turut, lakukan pemangkasan biaya segera.\n\n"
                "### In the sandbox\n\n"
                "Eksperimen dengan script Python untuk memilah arus kas toko roti Anda ke dalam tiga pos utama."
            ),
            "exercise": question(
                "Jika saldo rekening kas UMKM Anda bertambah Rp50 juta bulan ini karena pinjaman KUR cair, apakah bisnis Anda dapat dikatakan untung?",
                [
                    "Ya, karena saldo kas di rekening bank komersial bertambah secara signifikan dalam waktu singkat",
                    "Belum tentu, karena pencairan pinjaman adalah arus kas pendanaan yang harus dicicil kembali, bukan laba operasional",
                    "Pasti menghasilkan laba bersih jika seluruh dana pinjaman langsung dibelanjakan untuk aset konsumtif",
                ],
                1,
                "Pinjaman bank adalah kewajiban (liabilitas) pendanaan yang wajib dibayar kembali beserta bunganya, bukan pendapatan hasil penjualan.",
            ),
            "exercises": [
                question(
                    "Jika saldo rekening kas UMKM bertambah karena pinjaman KUR cair, apakah bisnis otomatis untung?",
                    [
                        "Ya, karena saldo kas di rekening bank komersial bertambah secara signifikan dalam waktu singkat",
                        "Belum tentu, pinjaman adalah arus kas pendanaan yang harus dicicil kembali, bukan laba penjualan",
                        "Pasti menghasilkan laba bersih jika seluruh dana pinjaman langsung dibelanjakan untuk aset konsumtif",
                    ],
                    1,
                    "Pinjaman bank adalah liabilitas pendanaan yang wajib dicicil kembali, bukan pendapatan operasional.",
                ),
            ],
            "terms": [
                {"term": "Arus Kas Operasional (Operating Cash Flow)", "definition": "Kas yang dihasilkan langsung dari kegiatan utama bisnis, seperti penjualan barang dan pembayaran bahan baku."},
                {"term": "Arus Kas Pendanaan (Financing Cash Flow)", "definition": "Aliran kas yang terkait dengan pendanaan bisnis, seperti pinjaman bank, angsuran kredit, atau setoran modal."},
            ],
            "references": [
                {"title": "Bank Indonesia · Pengenalan Laporan Arus Kas UMKM", "url": "https://www.bi.go.id/id/umkm/default.aspx"},
            ],
        },
        {
            "id": "23.5",
            "part": "2",
            "title": "Menyusun Proyeksi Arus Kas 12 Bulan",
            "subtitle": "Membuat Proyeksi Arus Kas 12 Bulan (Capstone Project UMKM)",
            "minutes": 25,
            "objective": "Menyusun proyeksi kas bergulir 12 bulan menggunakan template standar dan memvalidasi kontinuitas saldo awal dan akhir.",
            "kind": "fundamentals",
            "formula": r"\text{Saldo Akhir Bulan } t = \text{Saldo Awal Bulan } t + \text{Inflow}_t - \text{Outflow}_t",
            "code": (
                "# Proyeksi arus kas 12 bulan sederhana dengan verifikasi kontinuitas\n"
                "kas_awal = 50_000_000\n"
                "inflows = [35, 38, 42, 40, 45, 48, 50, 47, 46, 52, 55, 60]  # dalam juta rupiah\n"
                "outflows = [28, 30, 33, 32, 35, 38, 40, 39, 38, 41, 44, 48]  # dalam juta rupiah\n"
                "\n"
                "saldo_berjalan = kas_awal\n"
                "print('Bulan | Kas Awal | Kas Masuk | Kas Keluar | Kas Akhir')\n"
                "for m in range(12):\n"
                "    masuk = inflows[m] * 1_000_000\n"
                "    keluar = outflows[m] * 1_000_000\n"
                "    saldo_akhir = saldo_berjalan + masuk - keluar\n"
                "    print(f'{m+1:5d} | {saldo_berjalan/1e6:8.1f}M | {masuk/1e6:9.1f}M | {keluar/1e6:10.1f}M | {saldo_akhir/1e6:9.1f}M')\n"
                "    saldo_berjalan = saldo_akhir\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Melihat kaca spion (pencatatan masa lalu) itu baik, namun pengemudi yang selamat adalah yang melihat kaca depan. **Proyeksi arus kas 12 bulan** (*12-month cash forecast*) memetakan estimasi kas masuk dan kas keluar Anda untuk satu tahun ke depan.\n\n"
                "Tujuan utama proyeksi bukanlah memprediksi angka rupiah secara tepat hingga ke desimal terakhir, melainkan **melihat celah kas (*cash gap*) sebelum itu terjadi**. Misalnya, jika Anda tahu bahwa pada bulan ke-4 ada pembayaran sewa kios tahunan yang membuat kas minus, Anda punya waktu 90 hari untuk menabung atau menegosiasikan termin cicilan sewa sebelum krisis tiba.\n\n"
                "$$\n"
                r"\text{Closing Balance}_t = \text{Opening Balance}_t + \text{Inflow}_t - \text{Outflow}_t \quad (\text{di mana } \text{Opening}_{t+1} = \text{Closing}_t)"
                "\n$$\n\n"
                "## A worked example & Capstone Deliverable / Contoh Kasus Nyata\n\n"
                "Dalam modul capstone ini, Anda wajib melengkapi dan memverifikasi template proyeksi arus kas 12 bulan (`cash_flow_forecast_template.csv`):\n"
                "1. Tepat 12 baris bulan (bulan 1 s.d. 12).\n"
                "2. Kolom angka: `opening_balance`, `cash_inflows`, `cash_outflows`, `closing_balance`.\n"
                "3. Kontinuitas saldo: Saldo akhir bulan berjalan wajib sama persis dengan saldo awal bulan berikutnya.\n"
                "4. Tidak ada saldo kas akhir yang bernilai negatif.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Unduh template CSV (`cash_flow_forecast_template.csv`) dari bagian sumber daya kursus.\n"
                "2. Masukkan angka estimasi berdasarkan rata-rata realisasi 3 bulan terakhir bisnis Anda.\n"
                "3. Masukkan pos pengeluaran musiman (THR karyawan di bulan Idul Fitri, perpanjangan sewa tahunan, atau penumpukan stok barang dagang).\n"
                "4. Lakukan self-check mandiri: pastikan kontinuitas saldo terpenuhi di setiap baris dan saldo akhir tidak pernah negatif.\n\n"
                "### In the sandbox\n\n"
                "Jalankan kode proyeksi untuk melihat bagaimana saldo awal bulan berikutnya mengalir otomatis dari saldo akhir bulan sebelumnya."
            ),
            "exercise": question(
                "Dalam pembuatan proyeksi arus kas 12 bulan yang benar, darimana angka saldo awal bulan Maret berasal?",
                [
                    "Dihitung secara acak berdasarkan target omzet penjualan kotor yang diinginkan pemilik usaha",
                    "Sama persis dengan saldo kas akhir bulan Februari",
                    "Rata-rata penjualan bersih pada kuartal pertama tahun buku sebelumnya",
                ],
                1,
                "Secara prinsip kontinuitas kas, uang yang ada di rekening pada 1 Maret pagi hari adalah sisa uang fisik yang ada pada penutupan 28/29 Februari malam hari.",
            ),
            "exercises": [
                question(
                    "Dalam proyeksi kas 12 bulan, dari mana saldo awal bulan Maret berasal?",
                    [
                        "Dihitung secara acak berdasarkan target omzet penjualan kotor yang diinginkan pemilik usaha",
                        "Sama persis dengan saldo kas akhir bulan Februari",
                        "Rata-rata penjualan bersih pada kuartal pertama tahun buku sebelumnya",
                    ],
                    1,
                    "Saldo awal bulan berikutnya selalu sama persis dengan saldo akhir bulan sebelumnya.",
                ),
            ],
            "terms": [
                {"term": "Proyeksi Arus Kas (Cash Flow Forecast)", "definition": "Perkiraan jumlah uang tunai yang diharapkan masuk dan keluar dari usaha selama periode waktu tertentu di masa depan."},
                {"term": "Kontinuitas Saldo (Balance Continuity)", "definition": "Kaidah matematis di mana saldo akhir periode saat ini menjadi saldo pembuka periode berikutnya."},
            ],
            "references": [
                {"title": "Bank Indonesia · Panduan Praktis Perencanaan Kas dan Keuangan Usaha", "url": "https://www.bi.go.id/id/umkm/default.aspx"},
            ],
        },
        {
            "id": "23.6",
            "part": "3",
            "title": "Analisis Titik Impas (BEP) Satu Produk",
            "subtitle": "Menghitung Titik Impas (Break-Even Point) untuk Menentukan Target Penjualan",
            "minutes": 18,
            "objective": "Menghitung biaya tetap, biaya variabel, margin kontribusi, dan unit titik impas (BEP) untuk satu produk unggulan.",
            "kind": "fundamentals",
            "formula": r"\text{BEP (Unit)} = \frac{\text{Biaya Tetap}}{\text{Harga Jual/Unit} - \text{Biaya Variabel/Unit}} = \frac{\text{Biaya Tetap}}{\text{Margin Kontribusi/Unit}}",
            "code": (
                "# Menghitung Break-Even Point (BEP) satu produk\n"
                "harga_jual_per_porsi = 25_000\n"
                "biaya_variabel_per_porsi = 13_000  # Beras, ayam, bumbu, kemasan box\n"
                "margin_kontribusi = harga_jual_per_porsi - biaya_variabel_per_porsi\n"
                "biaya_tetap_bulanan = 6_000_000   # Sewa tempat, gaji asisten, wifi\n"
                "\n"
                "bep_unit = biaya_tetap_bulanan / margin_kontribusi\n"
                "bep_rupiah = bep_unit * harga_jual_per_porsi\n"
                "bep_harian = bep_unit / 25  # Asumsi konsisten 25 hari kerja sebulan\n"
                "\n"
                "print(f'Margin Kontribusi per Porsi: Rp {margin_kontribusi:,.0f}')\n"
                "print(f'BEP Bulanan: {bep_unit:.0f} porsi (Rp {bep_rupiah:,.0f})')\n"
                "print(f'Target Minimal Harian: {bep_harian:.1f} porsi/hari')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Berapa porsi nasi ayam atau berapa cangkir kopi yang harus Anda jual setiap hari hanya agar usaha tidak merugi? Jawaban dari pertanyaan ini adalah **Titik Impas** (*Break-Even Point* atau BEP).\n\n"
                "Untuk menghitung BEP, Anda harus memisahkan biaya menjadi dua jenis:\n"
                "1. **Biaya Tetap (*Fixed Cost*)**: Biaya yang jumlahnya tetap harus dibayar berapa pun produk yang terjual (sewa tempat, gaji karyawan tetap, internet, penyusutan etalase).\n"
                "2. **Biaya Variabel (*Variable Cost*)**: Biaya yang naik seiring banyaknya produk yang diproduksi (beras, ayam, minyak goreng, kemasan takeaway).\n\n"
                "Setiap kali satu produk terjual, selisih antara harga jual dan biaya variabel disebut **Margin Kontribusi**. Margin inilah yang bertugas 'mencicil' pembayaran biaya tetap bulanan hingga lunas. Setelah biaya tetap tertutup, penjualan berikutnya menghasilkan keuntungan murni sebesar nilai margin kontribusi (misal Rp12.000 per porsi).\n\n"
                "$$\n"
                r"\text{BEP (Unit)} = \frac{\text{Total Biaya Tetap}}{\text{Harga Jual per Unit} - \text{Biaya Variabel per Unit}}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Warung Nasi Kotak memiliki biaya tetap sewa dan gaji asisten sebesar Rp6.000.000 per bulan. Harga jual per kotak Rp25.000, sedangkan belanja bahan baku dan kotak per porsi Rp13.000.\n\n"
                "Margin kontribusi per porsi adalah Rp25.000 − Rp13.000 = Rp12.000. Maka BEP unit adalah:\n"
                "$$\\text{BEP} = \\frac{6.000.000}{12.000} = 500 \\text{ kotak per bulan}$$\n"
                "Jika warung buka konsisten 25 hari sebulan, Ibu Siti harus menjual minimal **20 kotak per hari** hanya untuk balik modal operasional. Kotak ke-21 yang terjual barulah menghasilkan laba bersih riil sebesar Rp12.000 per kotak bagi keluarga.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Buat daftar seluruh pengeluaran bulanan dan beri label [Tetap] atau [Variabel].\n"
                "2. Hitung biaya variabel per porsi/unit produk unggulan Anda.\n"
                "3. Bagi total biaya tetap dengan margin kontribusi untuk mendapatkan target unit minimal harian (berdasarkan 25 hari kerja).\n\n"
                "### In the sandbox\n\n"
                "Ubah harga jual atau biaya bahan di script Python dan amati bagaimana target BEP harian Anda berubah seketika."
            ),
            "exercise": question(
                "Jika biaya tetap warung Anda Rp6 juta/bulan dan margin kontribusi per porsi Rp12.000, berapa porsi yang harus terjual dalam sebulan agar tidak rugi?",
                [
                    "250 porsi makanan siap saji per bulan",
                    "500 porsi",
                    "1.000 porsi paket katering per bulan",
                ],
                1,
                "BEP = Biaya Tetap / Margin Kontribusi = Rp6.000.000 / Rp12.000 = 500 porsi per bulan.",
            ),
            "exercises": [
                question(
                    "Jika biaya tetap Rp6 juta/bulan dan margin kontribusi Rp12.000/porsi, berapa porsi target BEP sebulan?",
                    [
                        "250 porsi makanan siap saji per bulan",
                        "500 porsi",
                        "1.000 porsi paket katering per bulan",
                    ],
                    1,
                    "BEP = Rp6.000.000 / Rp12.000 = 500 porsi.",
                ),
            ],
            "terms": [
                {"term": "Titik Impas (Break-Even Point)", "definition": "Tingkat volume penjualan di mana total pendapatan persis sama dengan total biaya, sehingga laba bersih bernilai nol."},
                {"term": "Margin Kontribusi (Contribution Margin)", "definition": "Harga jual per unit dikurangi biaya variabel per unit; jumlah rupiah yang tersedia untuk menutup biaya tetap."},
            ],
            "references": [
                {"title": "Kementerian UMKM · Analisis Biaya dan Titik Impas UMKM", "url": "https://kemenkopukm.go.id"},
            ],
        },
        {
            "id": "23.7",
            "part": "3",
            "title": "Modal Kerja dan Celah Kas (Cash Gap)",
            "subtitle": "Mengelola Modal Kerja dan Menutup Celah Kas (Cash Gap)",
            "minutes": 18,
            "objective": "Memetakan hari persediaan, hari piutang, dan hari utang ke dalam siklus konversi kas untuk mencegah krisis likuiditas modal kerja.",
            "kind": "fundamentals",
            "formula": r"\text{Siklus Konversi Kas (Hari)} = \text{DIO} + \text{DSO} - \text{DPO}",
            "code": (
                "# Menghitung Siklus Konversi Kas (Cash Conversion Cycle)\n"
                "dio = 20  # Days Inventory Outstanding: barang mengendap di gudang\n"
                "dso = 30  # Days Sales Outstanding: waktu tunggu piutang pelanggan\n"
                "dpo = 15  # Days Payable Outstanding: tempo pembayaran supplier bahan\n"
                "\n"
                "siklus_kas_hari = dio + dso - dpo\n"
                "kebutuhan_kas_harian = 1_200_000\n"
                "modal_kerja_terkunci = siklus_kas_hari * kebutuhan_kas_harian\n"
                "\n"
                "print(f'Celah Kas (Cash Gap / CCC): {siklus_kas_hari} hari')\n"
                "print(f'Modal Kerja yang Harus Disediakan Sendiri: Rp {modal_kerja_terkunci:,.0f}')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Banyak usaha bangkrut justru ketika pesanan membludak (*growing broke*). Ketika pesanan naik 3 kali lipat, Anda harus membeli kain atau bahan baku 3 kali lebih banyak hari ini, membayar penjahit minggu ini, sementara pembeli baru membayar bulan depan. Periode waktu di mana Anda sudah keluar uang namun belum menerima kas disebut **Celah Kas (*Cash Gap*)** atau Siklus Konversi Kas (*Cash Conversion Cycle* / CCC).\n\n"
                "Siklus Konversi Kas terdiri dari tiga variabel waktu:\n"
                "1. **DIO (*Days Inventory Outstanding*)**: Berapa lama bahan baku mengendap di gudang sebelum terjual.\n"
                "2. **DSO (*Days Sales Outstanding*)**: Berapa lama pelanggan menahan pembayaran piutang sebelum melunasi.\n"
                "3. **DPO (*Days Payable Outstanding*)**: Berapa lama pemasok bahan memberi Anda tempo pembayaran sebelum jatuh tempo.\n\n"
                "$$\n"
                r"\text{Cash Conversion Cycle (Hari)} = \text{DIO} + \text{DSO} - \text{DPO}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Konveksi Kaos membeli bahan kain dengan tempo 15 hari dari supplier (DPO = 15). Proses jahit memakan waktu 20 hari sebelum dikirim (DIO = 20). Klien perusahaan meminta tempo pembayaran 30 hari setelah barang diterima (DSO = 30).\n\n"
                "Siklus konversi kas adalah:\n"
                "$$\\text{Cash Gap} = 20 + 30 - 15 = 35 \\text{ hari}$$\n"
                "Selama 35 hari penuh, pemilik konveksi harus menalangi biaya operasional sendiri sebesar Rp1.200.000 per hari, membutuhkan modal kerja mengendap sebesar **Rp42.000.000**. Jika pemilik tidak memiliki dana cadangan ini, produksi terhenti dan pesanan batal.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Negosiasikan termin pembayaran yang lebih panjang dengan pemasok terpercaya (meningkatkan DPO dari 15 hari menjadi 30 hari).\n"
                "2. Minta uang muka (DP) minimal 30%–50% dari pelanggan untuk memangkas hari piutang (DSO).\n"
                "3. Percepat perputaran persediaan (memangkas DIO) dengan tidak menimbun bahan baku yang perputarannya lambat.\n\n"
                "### In the sandbox\n\n"
                "Jalankan kode untuk menguji bagaimana mempercepat hari piutang dari 30 hari menjadi 10 hari memangkas kebutuhan modal kerja usaha Anda."
            ),
            "exercise": question(
                "Jika hari persediaan (DIO) 20 hari, hari piutang (DSO) 30 hari, dan supplier memberi tempo (DPO) 15 hari, berapa hari kas Anda mengalami gap (kekosongan modal)?",
                [
                    "15 hari kalender",
                    "35 hari",
                    "65 hari kerja",
                ],
                1,
                "Cash Gap = 20 + 30 − 15 = 35 hari. Usaha harus mendanai sendiri kebutuhan operasional selama 35 hari.",
            ),
            "exercises": [
                question(
                    "Jika hari persediaan 20 hari, piutang 30 hari, dan tempo supplier 15 hari, berapa hari cash gap usaha?",
                    [
                        "15 hari kalender",
                        "35 hari",
                        "65 hari kerja",
                    ],
                    1,
                    "Cash Gap = 20 + 30 − 15 = 35 hari.",
                ),
            ],
            "terms": [
                {"term": "Siklus Konversi Kas (Cash Conversion Cycle)", "definition": "Jangka waktu antara pembayaran uang tunai untuk membeli bahan baku hingga diterimanya kembali uang tunai dari hasil penjualan produk (DIO + DSO - DPO)."},
                {"term": "Modal Kerja Bersih (Net Working Capital)", "definition": "Selisih antara aset lancar (kas, piutang, persediaan) dengan kewajiban lancar (utang usaha yang jatuh tempo segera)."},
            ],
            "references": [
                {"title": "Bank Indonesia · Manajemen Modal Kerja dan Likuiditas", "url": "https://www.bi.go.id/id/umkm/default.aspx"},
            ],
        },
        {
            "id": "23.8",
            "part": "4",
            "title": "Strategi Harga: Markup vs Gross Margin",
            "subtitle": "Strategi Penetapan Harga Jual: Jebakan Markup vs Margin Riil",
            "minutes": 18,
            "objective": "Menghitung harga jual yang tepat menggunakan rumus margin berbasis biaya pokok (HPP) dan memperhitungkan potongan komisi platform.",
            "kind": "fundamentals",
            "formula": r"\text{Harga Jual (Termasuk Fee)} = \frac{\text{HPP}}{1 - \text{Target Margin \%} - \text{Fee Platform \%}}",
            "code": (
                "# Membandingkan Markup 30% vs Margin 30% dan Fee Marketplace\n"
                "hpp = 70_000  # Biaya produksi / HPP per unit\n"
                "\n"
                "# Rumus 1: Markup 30% dari HPP\n"
                "harga_markup = hpp * (1 + 0.30)\n"
                "profit_markup = harga_markup - hpp\n"
                "\n"
                "# Rumus 2: Target Margin 30% dari Harga Jual\n"
                "harga_margin = hpp / (1 - 0.30)\n"
                "profit_margin = harga_margin - hpp\n"
                "\n"
                "# Rumus 3: Harga termasuk Margin 20% + Fee Marketplace 15%\n"
                "harga_all_in = hpp / (1 - 0.20 - 0.15)\n"
                "\n"
                "print(f'Harga Metode Markup 30%: Rp {harga_markup:,.0f} (Profit: Rp {profit_markup:,.0f})')\n"
                "print(f'Harga Metode Margin 30%: Rp {harga_margin:,.0f} (Profit: Rp {profit_margin:,.0f})')\n"
                "print(f'Harga All-In (Margin 20% + Fee 15%): Rp {harga_all_in:,.0f}')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Banyak pemilik usaha berpikir bahwa menambahkan markup 30% pada Harga Pokok Penjualan (HPP) sama artinya dengan mendapatkan margin keuntungan 30%. Ini adalah **salah kaprah matematika yang fatal**.\n\n"
                "Perbedaannya terletak pada angka pembagi:\n"
                "- **Markup (Cost-Plus)**: Keuntungan dihitung sebagai persentase dari **biaya produksi (HPP)**.\n"
                "- **Gross Margin**: Keuntungan dihitung sebagai persentase dari **harga jual akhir kepada konsumen**.\n\n"
                "Jika HPP Anda Rp70.000 dan Anda menambah markup 30%, harga jualnya Rp91.000 dengan keuntungan Rp21.000. Namun saat Anda menjual di marketplace yang memotong komisi 15% dari harga jual, potongan komisi Rp13.650 memakan hingga 65% dari laba kotor Anda! Untuk menjaga profitabilitas, gunakan rumus penetapan harga yang memasukkan fee platform secara eksplisit:\n\n"
                "$$\n"
                r"\text{Harga Jual} = \frac{\text{HPP}}{1 - \text{Target Margin} - \text{Fee Platform}}"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Toko Kue memproduksi kue kering dengan HPP Rp70.000 per toples. Pemilik menginginkan margin bersih 30% dari harga jual untuk menutup sewa toko:\n"
                "$$\\text{Harga} = \\frac{70.000}{1 - 0.30} = \\frac{70.000}{0.70} = \\text{Rp100.000}$$\n"
                "Keuntungan per toples adalah Rp30.000, tepat 30% dari harga jual Rp100.000. Jika sebelumnya pemilik hanya menggunakan markup Rp70.000 × 1.3 = Rp91.000, keuntungannya hanya Rp21.000 (margin riil hanya 23%), dan bisnis kekurangan kas untuk membayar sewa toko.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Hitung seluruh komponen HPP: bahan baku, kemasan, dan upah tenaga kerja langsung.\n"
                "2. Tentukan target gross margin minimal yang mampu menyerap diskon promosi atau potongan fee marketplace.\n"
                "3. Gunakan rumus pembagi `(1 - Margin - Fee)` bukan pengali markup.\n\n"
                "### In the sandbox\n\n"
                "Jalankan kode Python untuk membandingkan perbedaan harga jual dan keuntungan riil antara metode markup dan metode margin."
            ),
            "exercise": question(
                "Jika HPP produk Anda Rp70.000 dan Anda menginginkan margin keuntungan sebesar 30% dari harga jual, berapakah harga jual yang tepat?",
                [
                    "Rp91.000 per unit kemasan",
                    "Rp100.000",
                    "Rp120.000 per unit kemasan",
                ],
                1,
                "Harga = HPP / (1 − 0.30) = Rp70.000 / 0.70 = Rp100.000.",
            ),
            "exercises": [
                question(
                    "Jika HPP produk Rp70.000 dan target margin 30% dari harga jual, berapa harga jualnya?",
                    [
                        "Rp91.000 per unit kemasan",
                        "Rp100.000",
                        "Rp120.000 per unit kemasan",
                    ],
                    1,
                    "Harga = 70.000 / (1 − 0.30) = Rp100.000.",
                ),
            ],
            "terms": [
                {"term": "Harga Pokok Penjualan (HPP / COGS)", "definition": "Seluruh biaya langsung yang dikeluarkan untuk menghasilkan barang atau jasa yang siap dijual."},
                {"term": "Gross Margin", "definition": "Persentase laba kotor terhadap total harga jual, menunjukkan efisiensi produksi sebelum biaya operasional umum."},
            ],
            "references": [
                {"title": "Kementerian UMKM · Penentuan Harga Jual Produk UMKM", "url": "https://kemenkopukm.go.id"},
            ],
        },
        {
            "id": "23.9",
            "part": "4",
            "title": "Kapan Waktunya Mengambil Pinjaman Usaha?",
            "subtitle": "Kapan Waktunya Mengambil Pinjaman Usaha dan Evaluasi Utang",
            "minutes": 20,
            "objective": "Mengevaluasi kapasitas utang menggunakan Debt Service Coverage Ratio (DSCR) dan membedakan modal produktif dari lubang likuiditas konsumtif.",
            "kind": "fundamentals",
            "formula": r"\text{DSCR} = \frac{\text{Arus Kas Operasional Bersih}}{\text{Angsuran Pokok} + \text{Bunga Pinjaman}} \ge 1.3\times",
            "code": (
                "# Evaluasi kelayakan mengambil pinjaman usaha (DSCR)\n"
                "kas_operasional_bersih_bulanan = 6_500_000\n"
                "tawaran_cicilan_kur_bulanan = 3_200_000  # Angsuran pokok + bunga\n"
                "\n"
                "dscr = kas_operasional_bersih_bulanan / tawaran_cicilan_kur_bulanan\n"
                "print(f'Rasio Kemampuan Bayar (DSCR): {dscr:.2f}x')\n"
                "if dscr >= 1.3:\n"
                "    print('Status: Layak mengambil pinjaman (Memiliki buffer pengaman ~23%)')\n"
                "else:\n"
                "    print('Status: Terlalu berisiko! Arus kas tidak cukup kuat menahan penurunan penjualan')\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Pinjaman modal usaha adalah seperti pedang bermata dua: ia mempercepat pertumbuhan jika digunakan untuk membeli aset produktif yang menghasilkan arus kas baru, namun menjadi racun mematikan jika digunakan untuk menambal kerugian operasional sehari-hari.\n\n"
                "Dua aturan emas sebelum menandatangani perjanjian kredit:\n"
                "1. **Jangan pernah meminjam uang untuk menutup kerugian operasional yang sedang berjalan**. Jika model bisnis Anda rugi Rp5 juta per bulan, menyuntikkan utang Rp50 juta hanya memperpanjang napas 10 bulan sebelum bangkrut dengan beban utang yang menumpuk.\n"
                "2. **Uji kemampuan bayar dengan rasio penutup utang (DSCR)**: Arus kas operasional bersih bulanan Anda wajib minimal **1,3× lebih besar** dari total cicilan pokok dan bunga bulanan. Rasio 1,3× ini memberikan bantalan pengaman sekitar 23% ($1 - 1/1{,}3$) ketika penjualan mengalami penurunan sementara.\n\n"
                "$$\n"
                r"\text{DSCR} = \frac{\text{Arus Kas Operasional Bersih Bulanan}}{\text{Total Angsuran Pokok + Bunga Bulanan}} \ge 1{,}3\times"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Bengkel Motor mencatat arus kas operasional bersih stabil Rp6.500.000 per bulan. Pemilik ingin mengambil pinjaman KUR untuk membeli mesin bubut presisi yang akan menambah pendapatan bengkel. Cicilan bank Rp3.200.000 per bulan selama 2 tahun.\n\n"
                "$$\\text{DSCR} = \\frac{6.500.000}{3.200.000} = 2{,}03\\times$$\n"
                "Angka 2,03× berada jauh di atas ambang batas minimal 1,3×. Bahkan jika pendapatan bengkel turun 30% karena cuaca buruk, bengkel masih mampu membayar cicilan tepat waktu tanpa harus menunggak. Keputusan mengambil pinjaman ini rasional dan aman.\n\n"
                "## Research protocol / Panduan Praktik\n\n"
                "1. Hitung arus kas operasional bersih rata-rata 6 bulan terakhir tanpa memperhitungkan proyeksi yang terlalu muluk.\n"
                "2. Pastikan pinjaman disalurkan ke aset yang menghasilkan pendapatan langsung (mesin produksi, kendaraan angkut).\n"
                "3. Tolak tawaran pinjaman online ilegal atau pinjaman berbunga harian yang tidak terdaftar di OJK.\n\n"
                "### In the sandbox\n\n"
                "Uji kelayakan pinjaman modal Anda di script Python dengan memasukkan nominal cicilan bank dan arus kas riil Anda."
            ),
            "exercise": question(
                "Berapa batas rasio minimal Debt Service Coverage Ratio (DSCR) yang disarankan agar UMKM aman dari risiko gagal bayar kredit?",
                [
                    "0,8× dari total angsuran kredit bulanan",
                    "1,0× dari total angsuran kredit bulanan",
                    "1,3× (memiliki buffer aman sekitar 23%)",
                ],
                2,
                "DSCR minimal 1,3× memastikan arus kas operasional memiliki cadangan keamanan sekitar 23% di atas cicilan jika penjualan mengalami penurunan.",
            ),
            "exercises": [
                question(
                    "Berapa batas rasio minimal DSCR yang disarankan agar UMKM aman dari risiko gagal bayar?",
                    [
                        "0,8× dari total angsuran kredit bulanan",
                        "1,0× dari total angsuran kredit bulanan",
                        "1,3× (memiliki buffer aman sekitar 23%)",
                    ],
                    2,
                    "DSCR minimal 1,3× memastikan ada bantalan pengaman sekitar 23% di atas nilai angsuran cicilan.",
                ),
            ],
            "terms": [
                {"term": "Debt Service Coverage Ratio (DSCR)", "definition": "Rasio perbandingan antara arus kas operasional yang tersedia dengan total kewajiban pembayaran angsuran pokok dan bunga utang."},
                {"term": "Kredit Usaha Rakyat (KUR)", "definition": "Program pembiayaan bersubsidi bunga dari pemerintah untuk membantu permodalan pelaku UMKM produktif."},
            ],
            "references": [
                {"title": "OJK · Ketentuan Kredit Perbankan dan Perlindungan Konsumen UMKM", "url": "https://www.ojk.go.id"},
            ],
        },
        {
            "id": "23.10",
            "part": "4",
            "title": "Dasar Kepatuhan Pajak & Legalitas UMKM Indonesia",
            "subtitle": "Kewajiban Pajak dan Legalitas UMKM Indonesia: PP 55/2022 & Batas Bebas Pajak",
            "minutes": 22,
            "objective": "Memahami ketentuan PPh Final 0,5% sesuai PP 55/2022 s.t.d.d. PP 20/2026, batas omzet bebas pajak Rp500 juta, dan ambang PKP Rp4,8 miliar.",
            "kind": "fundamentals",
            "formula": r"\text{PPh Final Terutang} = \max(0, \text{Omzet Kumulatif} - 500.000.000) \times 0{,}5\% \quad (\text{Khusus Wajib Pajak Orang Pribadi})",
            "code": (
                "# Simulasi PPh Final UMKM 0.5% sesuai UU HPP & PP 55/2022 s.t.d.d. PP 20/2026\n"
                "omzet_bulanan = 40000000\n"
                "omzet_tahunan = omzet_bulanan * 12\n"
                "ambang_bebas_pajak = 500000000\n"
                "\n"
                "print('Omzet Tahunan: Rp', omzet_tahunan)\n"
                "print('Batas Bebas Pajak: Rp', ambang_bebas_pajak)\n"
                "if omzet_tahunan <= ambang_bebas_pajak:\n"
                "    print('Status: Bebas Pajak (PPh Rp 0)')\n"
                "else:\n"
                "    pajak = (omzet_tahunan - ambang_bebas_pajak) * 0.005\n"
                "    print('PPh Final 0.5%: Rp', pajak)\n"
            ),
            "content": (
                "## The idea / Konsep Utama\n\n"
                "Sebagai pemilik usaha mikro dan kecil di Indonesia, memahami kewajiban perpajakan tidak harus rumit dan menakutkan. Pemerintah Indonesia melalui **UU Harmonisasi Peraturan Perpajakan (UU HPP)** dan **PP 55/2022 sebagaimana telah diubah dengan PP 20/2026** memberikan fasilitas keringanan perpajakan bagi pelaku UMKM:\n\n"
                "1. **Skema Tarif 0,5%**: Pelaku usaha dengan peredaran bruto (omzet) tidak melebihi **Rp4,8 miliar per tahun** berhak menggunakan tarif PPh Final 0,5%.\n"
                "2. **Tanpa Batas Waktu untuk Orang Pribadi**: Bagi Wajib Pajak Orang Pribadi, skema PPh Final 0,5% berlaku tanpa batas waktu (permanen), dengan fasilitas omzet kumulatif sampai dengan **Rp500 juta dalam satu tahun pajak dibebaskan dari pajak (pajak Rp0)**!\n"
                "3. **Wajib Pajak Badan**: Entitas badan seperti Perseroan Perorangan (PT Perorangan 1 pendiri) dan Koperasi juga berhak atas fasilitas tarif ini. Badan usaha CV, Firma, dan PT yang sudah berjalan dapat memanfaatkan tarif 0,5% sampai jangka waktu PP 55 berakhir (4 tahun untuk CV/Koperasi, 3 tahun untuk PT).\n"
                "4. **Pengecualian Pekerjaan Bebas**: Penghasilan dari profesi pekerjaan bebas (dokter, pengacara, akuntan, notaris, konsultan) tidak dapat menggunakan tarif 0,5%, namun omzetnya tetap diperhitungkan dalam akumulasi batas Rp4,8 miliar.\n"
                "5. **Ambang Pengusaha Kena Pajak (PKP)**: Pelaku usaha wajib dikukuhkan sebagai PKP dan memungut PPN hanya jika omzet tahunan melampaui **Rp4,8 miliar**.\n"
                "6. **Pemotongan Marketplace**: Berdasarkan PMK 37/2025, platform marketplace memungut PPh Pasal 22 atas transaksi penjualan tertentu pedagang online.\n\n"
                "$$\n"
                r"\text{PPh Final OP} = \max(0, \text{Omzet Kumulatif Tahunan} - 500.000.000) \times 0{,}5\%"
                "\n$$\n\n"
                "## A worked example / Contoh Kasus Nyata\n\n"
                "Ibu Aminah adalah pengusaha warung makan perseorangan (Wajib Pajak Orang Pribadi) dengan omzet rata-rata Rp50.000.000 per bulan (total setahun Rp600.000.000):\n"
                "- Bulan 1 s.d. Bulan 10: Total omzet kumulatif mencapai Rp500.000.000. PPh Final terutang adalah **Rp0 (bebas pajak)**.\n"
                "- Bulan 11: Omzet Rp50.000.000 (kumulatif Rp550 juta). PPh Final 0,5% hanya dikenakan atas Rp50 juta = Rp250.000.\n"
                "- Bulan 12: Omzet Rp50.000.000 (kumulatif Rp600 juta). PPh Final 0,5% atas Rp50 juta = Rp250.000.\n\n"
                "Dari total peredaran usaha Rp600 juta dalam setahun, total pajak yang dibayarkan Ibu Aminah hanya **Rp500.000**. Legalitas dan kepatuhan perpajakan ini membuka pintu kemudahan mengajukan izin usaha resmi (NIB) dan fasilitas pembiayaan bank resmi.\n\n"
                "## Research protocol & Disclaimer / Tinjauan Legalitas\n\n"
                "> [!IMPORTANT]\n"
                "> **Catatan Kepatuhan:** Materi ini disajikan untuk edukasi literasi keuangan konseptual berdasarkan regulasi perpajakan Republik Indonesia (Direktorat Jenderal Pajak, UU HPP, PP 55/2022 s.t.d.d. PP 20/2026, PMK 37/2025) dan tidak menggantikan konsultasi hukum atau perpajakan resmi.\n\n"
                "### In the sandbox\n\n"
                "Jalankan kode simulasi untuk menghitung kapan tepatnya omzet usaha perseorangan Anda menyentuh batas Rp500 juta dan mulai membayar PPh Final 0,5%."
            ),
            "exercise": question(
                "Berdasarkan PP 55/2022 dan UU HPP, berapa batas peredaran bruto (omzet) yang tidak dikenai pajak (0%) bagi Wajib Pajak Orang Pribadi UMKM dalam satu tahun pajak?",
                [
                    "Rp50 juta per tahun pajak",
                    "Rp500 juta per tahun",
                    "Rp4,8 miliar per tahun pajak",
                ],
                1,
                "Sesuai UU HPP dan PP 55/2022, peredaran bruto kumulatif sampai dengan Rp500 juta dalam satu tahun pajak untuk Wajib Pajak Orang Pribadi UMKM dibebaskan dari PPh Final (0%).",
            ),
            "exercises": [
                question(
                    "Berapa batas omzet bebas pajak (0%) bagi Wajib Pajak Orang Pribadi UMKM per tahun sesuai PP 55/2022?",
                    [
                        "Rp50 juta per tahun pajak",
                        "Rp500 juta per tahun",
                        "Rp4,8 miliar per tahun pajak",
                    ],
                    1,
                    "Omzet kumulatif sampai dengan Rp500 juta dalam satu tahun pajak tidak dikenai PPh Final bagi Wajib Pajak Orang Pribadi.",
                ),
            ],
            "terms": [
                {"term": "PPh Final 0,5% UMKM", "definition": "Skema tarif pajak penghasilan final 0,5% atas peredaran bruto tertentu bagi pelaku usaha dengan omzet tidak lebih dari Rp4,8 miliar setahun."},
                {"term": "Nomor Induk Berusaha (NIB)", "definition": "Identitas resmi pelaku usaha yang diterbitkan oleh Lembaga OSS untuk perizinan operasional bisnis di Indonesia."},
                {"term": "Likuiditas Bisnis (Business Liquidity)", "definition": "Kemampuan kas dan aset lancar warung/usaha untuk memenuhi kewajiban operasional rutin harian tanpa ketergantungan utang."},
            ],
            "references": [
                {"title": "Direktorat Jenderal Pajak · Penyesuaian Pengaturan Pajak Penghasilan PP 55/2022", "url": "https://pajak.go.id"},
                {"title": "Kementerian Keuangan RI · Siaran Pers UU Harmonisasi Peraturan Perpajakan", "url": "https://kemenkeu.go.id"},
            ],
        },
    ]

    parts = [
        {
            "id": "1",
            "title": "Dasar Arus Kas & Pemisahan Dompet",
            "description": "Pahami mengapa usaha gagal karena kas, pisahkan rekening pribadi dan usaha, serta terapkan pencatatan harian yang bertahan di tengah kesibukan.",
        },
        {
            "id": "2",
            "title": "Membaca Angka & Proyeksi 12 Bulan",
            "description": "Pilahkan pos kas operasional, investasi, dan pendanaan, lalu susun proyeksi kas 12 bulan untuk melihat celah likuiditas.",
        },
        {
            "id": "3",
            "title": "Titik Impas & Manajemen Modal Kerja",
            "description": "Kalkulasi titik impas (BEP) satu produk, kelola siklus konversi kas, dan tutup cash gap sebelum kehabisan uang.",
        },
        {
            "id": "4",
            "title": "Strategi Harga, Pinjaman & Pajak UMKM",
            "description": "Terapkan penetapan harga berbasis margin, uji kelayakan pinjaman dengan DSCR, dan patuhi pajak UMKM sesuai regulasi terbaru.",
        },
    ]

    STRATEGY_FOOTER = (
        "\n\n# The price sandbox stays in cash; its equity curve is not evidence for the strategy's performance.\n"
        "def strategy(data):\n"
        '    return data["close"] < 0\n'
    )
    for m in modules:
        if "def strategy(data)" not in m.get("code", ""):
            m["code"] = (m.get("code", "") + STRATEGY_FOOTER).strip()

    exams = [
        {
            "id": "msme-financial-literacy-final",
            "title": "Financial Literacy for MSMEs Final Assessment",
            "kind": "final",
            "passingScore": 70,
            "minutes": 30,
            "version": 3,
            "description": "Evaluasi komprehensif literasi keuangan UMKM: arus kas, BEP, modal kerja, keputusan pinjaman, dan perpajakan Indonesia. Alokasi waktu pengerjaan 30 menit.",
            "moduleIds": [m["id"] for m in modules],
            "questions": [
                {
                    "id": "msme-final-q1",
                    "lessonId": "23.1",
                    "question": "Dalam evaluasi solvabilitas warung, apa risiko utama jika omzet kredit (piutang) meningkat jauh lebih cepat daripada kas tunai masuk?",
                    "options": [
                        "Tarif pajak penghasilan final secara otomatis berkurang setengahnya",
                        "Usaha mengalami defisit kas operasional untuk membayar pemasok dan upah harian",
                        "Pelanggan setia akan berhenti memesan barang dagangan selama tiga bulan ke depan",
                    ],
                    "answer": 1,
                    "explanation": "Omzet tercatat pada piutang belum berwujud uang kas riil; jika kewajiban tunai datang lebih awal, warung mengalami insolvensi kas meski di atas kertas laba.",
                },
                {
                    "id": "msme-final-q2",
                    "lessonId": "23.2",
                    "question": "Praktik 'prive disiplin' (gaji tetap pemilik) dalam pengelolaan keuangan UMKM bertujuan untuk:",
                    "options": [
                        "Memastikan pemilik menarik seluruh saldo kas harian tanpa batas pertanggungjawaban setiap malam",
                        "Mencegah pencampuran pengeluaran konsumtif rumah tangga dengan dana modal kerja usaha",
                        "Menghapuskan kewajiban pembukuan bukti pembayaran nota belanja barang dagangan toko",
                    ],
                    "answer": 1,
                    "explanation": "Dengan menetapkan gaji tetap untuk pemilik, dana operasional usaha terlindungi dari penarikan pribadi tak terkontrol yang menggerus modal kerja.",
                },
                {
                    "id": "msme-final-q3",
                    "lessonId": "23.3",
                    "question": "Format catatan transaksi harian paling ringkas yang tetap andal untuk warung sibuk harus minimal mencatat kolom:",
                    "options": [
                        "Warna kemasan produk, nama kurir ekspedisi pengantar, dan kondisi cuaca harian",
                        "Tanggal, deskripsi pos kas, nominal kas masuk/keluar, dan saldo kas berjalan",
                        "Estimasi fluktuasi harga saham kompetitor internasional di bursa berjangka luar negeri",
                    ],
                    "answer": 1,
                    "explanation": "Pencatatan tanggal, pos transaksi, arus kas masuk/keluar, dan saldo akhir berjalan memberikan kepastian rekonsiliasi kas harian yang akurat.",
                },
                {
                    "id": "msme-final-q4",
                    "lessonId": "23.4",
                    "question": "Dalam memilah arus kas (operasional, investasi, pendanaan), pencairan dana pinjaman bank atau KUR dikelompokkan sebagai:",
                    "options": [
                        "Arus kas operasional murni hasil penjualan barang dan jasa harian toko kepada pelanggan setia",
                        "Arus kas pendanaan yang menambah liabilitas kas tetapi wajib dicicil kembali, bukan laba usaha",
                        "Arus kas investasi belanja modal peralatan mesin dan etalase toko jangka panjang perusahaan",
                    ],
                    "answer": 1,
                    "explanation": "Pencairan pinjaman bank atau KUR adalah arus kas pendanaan yang wajib dicicil kembali; ini bukan keuntungan atau arus kas operasional dari penjualan.",
                },
                {
                    "id": "msme-final-q5",
                    "lessonId": "23.5",
                    "question": "Dalam tabel proyeksi arus kas 12 bulan (capstone), aturan kontinuitas saldo menyatakan bahwa:",
                    "options": [
                        "Saldo kas awal bulan t harus persis sama dengan saldo kas akhir bulan t-1",
                        "Saldo kas awal selalu ditetapkan bernilai nol setiap tanggal satu awal bulan kalender",
                        "Saldo kas akhir tidak dipengaruhi sama sekali oleh pengeluaran modal belanja aset fisik",
                    ],
                    "answer": 0,
                    "explanation": "Secara matematis, saldo kas akhir bulan sebelumnya menjadi saldo kas awal bulan berjalan, memastikan rantai kontinuitas likuiditas 12 bulan.",
                },
                {
                    "id": "msme-final-q6",
                    "lessonId": "23.6",
                    "question": "Jika harga jual per porsi mie ayam Rp15.000, biaya bahan baku Rp9.000/porsi, dan sewa tempat Rp3.000.000/bulan, berapa porsi minimal harus terjual per bulan untuk mencapai titik impas?",
                    "options": [
                        "200 porsi per bulan operasional",
                        "500 porsi per bulan",
                        "1.000 porsi per bulan operasional",
                    ],
                    "answer": 1,
                    "explanation": "Margin kontribusi per porsi = Rp15.000 − Rp9.000 = Rp6.000. BEP porsi = Rp3.000.000 / Rp6.000 = 500 porsi per bulan.",
                },
                {
                    "id": "msme-final-q7",
                    "lessonId": "23.7",
                    "question": "Bagaimana cara menutup cash gap (kesenjangan siklus kas) tanpa harus menambah utang bank berbunga mahal?",
                    "options": [
                        "Mempercepat penagihan piutang pelanggan (DSO) dan menegosiasikan termin pembayaran bahan baku lebih panjang (DPO)",
                        "Menjual seluruh peralatan mesin dan etalase operasional di bawah harga pasar wajar demi likuiditas jangka pendek",
                        "Menghentikan pembayaran kompensasi gaji karyawan secara sepihak selama tiga bulan berturut-turut tanpa pemberitahuan",
                    ],
                    "answer": 0,
                    "explanation": "Memperpendek Days Sales Outstanding (DSO) dan memperpanjang Days Payable Outstanding (DPO) secara efektif memangkas siklus konversi kas tanpa biaya bunga.",
                },
                {
                    "id": "msme-final-q8",
                    "lessonId": "23.8",
                    "question": "Jika pemilik warung ingin margin keuntungan kotor 25% dari sebuah paket katering dengan biaya pokok Rp75.000, berapa harga jual yang harus dipatok?",
                    "options": [
                        "Rp93.750 (hasil mark-up 25% dari HPP)",
                        "Rp100.000",
                        "Rp110.000 (hasil penambahan biaya tak terduga)",
                    ],
                    "answer": 1,
                    "explanation": "Harga jual = HPP / (1 − Target Margin) = Rp75.000 / (1 − 0.25) = Rp75.000 / 0.75 = Rp100.000. (Jika dijual Rp93.750, itu adalah mark-up 25% dengan margin riil 20%).",
                },
                {
                    "id": "msme-final-q9",
                    "lessonId": "23.9",
                    "question": "Berapa batas rasio cakupan pelunasan utang (Debt Service Coverage Ratio - DSCR) minimal yang aman sebelum UMKM mengambil pinjaman baru?",
                    "options": [
                        "Minimal 1.25x hingga 1.30x dari arus kas operasional bersih",
                        "Tepat 0.50x dari total omzet kotor penjualan bulanan tanpa memotong beban",
                        "Tidak ada batasan minimal, semakin besar nilai pinjaman bank semakin baik",
                    ],
                    "answer": 0,
                    "explanation": "DSCR di atas 1.25x memastikan kas operasional yang dihasilkan memiliki bantalan pengaman 20% di atas jumlah angsuran pokok dan bunga yang wajib dibayar.",
                },
                {
                    "id": "msme-final-q10",
                    "lessonId": "23.10",
                    "question": "Sesuai regulasi perpajakan Indonesia (PP 55/2022 s.t.d.d. PP 20/2026), batas omzet tahunan maksimal untuk dapat memanfaatkan tarif PPh Final UMKM 0,5% adalah:",
                    "options": [
                        "Rp500 juta dalam satu tahun pajak",
                        "Rp4,8 miliar per tahun",
                        "Rp10 miliar dalam satu tahun pajak",
                    ],
                    "answer": 1,
                    "explanation": "Fasilitas tarif PPh Final 0,5% berlaku untuk wajib pajak dengan peredaran bruto (omzet) tidak melebihi Rp4,8 miliar dalam satu tahun pajak.",
                },
            ],
        }
    ]

    return {
        "id": "msme-financial-literacy",
        "number": 23,
        "title": "Literasi Keuangan UMKM",
        "description": (
            "Dasar pengelolaan keuangan praktis bagi pemilik usaha mikro, kecil, dan menengah (UMKM). "
            "Kuasai pemisahan rekening pribadi vs usaha, pembukuan harian bebas ribet, pembuatan proyeksi "
            "arus kas 12 bulan (capstone), analisis titik impas (BEP), manajemen modal kerja, evaluasi utang "
            "usaha, dan kepatuhan pajak UMKM sesuai PP 55/2022 dan UU HPP."
        ),
        "source": "Original practical framework · Bank Indonesia & Kemenkop UKM guidance",
        "level": "Beginner",
        "icon": "book",
        "studyType": "applied",
        "modules": modules,
        "parts": parts,
        "prerequisites": "None. Dirancang untuk pemilik warung, jasa, toko online, dan pemula tanpa latar belakang akuntansi formal.",
        "outcomes": [
            "Memisahkan keuangan pribadi dan usaha dengan struktur akun yang disiplin",
            "Menyusun proyeksi arus kas 12 bulan untuk mendeteksi celah kas sebelum krisis",
            "Menghitung titik impas (BEP) satu produk dan target penjualan minimal harian",
            "Mengelola siklus konversi modal kerja dan mengevaluasi pinjaman usaha dengan DSCR",
            "Menerapkan ketentuan PPh Final UMKM 0,5% dan fasilitas omzet bebas pajak Rp500 juta secara tepat",
        ],
        "readingGuide": (
            "Materi disajikan dalam Bahasa Indonesia dengan istilah teknis keuangan global yang dijelaskan "
            "secara sederhana melalui contoh warung dan toko nyata. Selesaikan setiap modul, coba simulator "
            "perhitungan di setiap pelajaran, dan lengkapi tugas Capstone Proyeksi Kas 12 Bulan untuk menyelesaikan kursus."
        ),
        "resources": [
            {
                "title": "Template Proyeksi Kas 12 Bulan (CSV)",
                "url": "/templates/cash_flow_forecast_template.csv",
            },
            {
                "title": "Template Buku Log Transaksi Harian (CSV)",
                "url": "/templates/transaction_log_template.csv",
            },
        ],
        "references": [
            {"title": "Bank Indonesia · Modul Keuangan UMKM", "url": "https://www.bi.go.id/id/umkm/default.aspx"},
            {"title": "Direktorat Jenderal Pajak · Panduan Pajak UMKM PP 55/2022", "url": "https://pajak.go.id"},
            {"title": "Kemenkop UKM · Pusat Layanan Usaha Terpadu", "url": "https://kemenkopukm.go.id"},
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "msme-financial-literacy",
        "subtitle": "Literasi Keuangan Praktis untuk Pelaku UMKM",
        "audience_tags": ["msme", "beginner", "entrepreneur", "indonesia"],
        "estimated_minutes": sum(m["minutes"] for m in modules),
        "lesson_count": len(modules),
        "assessment_count": len(exams),
        "completion_criteria": {"lessons_pct": 100, "assessment_pass_pct": 70},
        "certificate": {"enabled": True, "template_id": "msme-literacy", "verification_required": False},
        "funnel_cta": {
            "label": "Lanjutkan ke The Intelligent & Careful Investor",
            "target_course_id": "intelligent-investor",
            "secondary_label": "Pelajari Data Hygiene untuk Investor & Pembukuan",
            "secondary_target_course_id": "data-hygiene",
        },
        "language": ["id", "en"],
    }
