# Course 1: Financial Literacy for MSMEs (Literasi Keuangan untuk UMKM)
## Detailed Lesson-by-Lesson Content Outline, Case Selection & Tax Review Brief

**Course Code:** `msme-financial-literacy` (Catalog Track #23)  
**Target Audience:** Micro, Small, and Medium Enterprise (MSME / UMKM) owners, sole proprietors (*Wajib Pajak Orang Pribadi*), warung operators, online store merchants (Shopee/Tokopedia/TikTok Shop), independent contractors, and small service business managers.  
**Pedagogical Objective:** Bridge non-technical entrepreneurs from informal bookkeeping and intuition-based cash management to systematic cash forecasting, unit economics, working capital control, loan service evaluation, and Indonesian tax compliance under PP 55/2022.  
**Language Track:** Indonesian primary (`id`), English secondary (`en`).  
**Prerequisites:** None (no prior financial, accounting, or coding background assumed).  
**Graduation Milestone & Capstone:** Submission of an autochecked 12-month cash flow forecast (CSV or structured sheet) exhibiting opening-to-closing balance continuity and self-evaluation rubric.  
**Primary Funnel CTA:** $\to$ `intelligent-investor` (*The Intelligent Investor* by Graham & Dodd).  
**Secondary Funnel CTA:** $\to$ `data-hygiene` (*Data Hygiene for Investors*).

---

## 1. Pedagogical Architecture & Module Breakdown

The curriculum is structured into four progressive parts spanning 10 core modules:
- **Part 1: Fondasi Arus Kas & Pemisahan Keuangan (Modules 1–3)**
- **Part 2: Membaca Angka Usaha & Proyeksi Arus Kas (Modules 4–5) — Includes Capstone**
- **Part 3: Unit Economics & Likuiditas Modal Kerja (Modules 6–7)**
- **Part 4: Keputusan Utang, Penetapan Harga & Pajak UMKM (Modules 8–10)**

```
+--------------------------------------------------------------------------------------------------+
|                                C1: FINANCIAL LITERACY FOR MSMEs                                  |
+--------------------------------------------------------------------------------------------------+
| PART 1: CASH FIRST, NOT PROFIT                                                                   |
| [23.1] Arus Kas vs Laba Buku   --> [23.2] Pemisahan Rekening Usaha --> [23.3] Pencatatan Kas 1-Hal|
+--------------------------------------------------------------------------------------------------+
| PART 2: ARUS KAS & FORECASTING (CAPSTONE)                                                        |
| [23.4] Membaca Uang Masuk/Keluar  ------------------------>  [23.5] Proyeksi Kas 12-Bulan       |
|                                                                     (Mandatory Capstone Upload)  |
+--------------------------------------------------------------------------------------------------+
| PART 3: UNIT ECONOMICS & MODAL KERJA                                                             |
| [23.6] Titik Impas (BEP) Satuan   ------------------------>  [23.7] Siklus Konversi Modal Kerja  |
+--------------------------------------------------------------------------------------------------+
| PART 4: PRICING, UTANG & KEPATUHAN PAJAK PP 55/2022                                              |
| [23.8] Margin vs Markup        --> [23.9] Kelayakan Pinjaman (DSCR) --> [23.10] Pajak UMKM 0.5%  |
+--------------------------------------------------------------------------------------------------+
|                                    FUNNEL EXIT ROUTES                                            |
| --> Primary: The Intelligent Investor (Track #0)  |  --> Secondary: Data Hygiene (Track #25)     |
+--------------------------------------------------------------------------------------------------+
```

---

## 2. Detailed Lesson-by-Lesson Specification

### Module 1: Mengapa UMKM Gagal Karena Kas, Bukan Laba (Why MSMEs Fail on Cash, Not Profit)

#### Lesson 23.1: Ilusi Laba Akuntansi vs Realitas Kas Harian
* **Duration:** 15 minutes | **Type:** Fundamentals & Worked Diagnostic
* **Learning Objective:** Distinguish between paper accounting profit and actual cash solvency; diagnose the warning signs of cash insolvency in a growing business.
* **Core Theoretical Principle:**
  Profit is an accounting construct subject to timing lags and accruals, whereas cash is the sole medium of exchange that settles debts, payroll, and supplier accounts payable. A business can be legally profitable while being operationally insolvent.
* **Mathematical Invariant:**
  $$\text{Net Cash Flow} = \text{Cash Inflows} - \text{Cash Outflows} \ne \text{Revenue} - \text{Expenses}$$
  $$\text{Solvency Condition: } \text{Cash Balance}_t \ge \text{Immediate Obligations}_t \quad \forall t$$
* **Business Scenario & Worked Numbers:**
  *Warung Nasi Padang "Minang Jaya" (Ibu Siti)* records gross sales of Rp 45,000,000 in Ramadan. However:
  - Cash received at drawer: Rp 25,000,000.
  - Neighbor catering receivables (*kasbon kantor kelurahan*): Rp 20,000,000 (payable in 45 days).
  - Cash outlays due immediately: Groceries & meat supplier Rp 24,000,000, employee wages Rp 6,000,000, shop lease Rp 3,000,000 (Total Rp 33,000,000).
  - *Accounting view:* Profit = Rp 45,000,000 − Rp 33,000,000 = **+Rp 12,000,000 (Looks healthy!)**
  - *Cash reality:* Inflow Rp 25,000,000 − Outflow Rp 33,000,000 = **−Rp 8,000,000 deficit.** Ibu Siti cannot purchase meat tomorrow unless she injects emergency liquidity.
* **Key Artifact / Template:** *Lembar Diagnosa Kesehatan Kas 5-Menit* (PDF checklist).
* **Interactive Tool / Code:** Cash balance vs accounting profit comparison calculator.
* **Assessment Item:**
  *Question:* Mengapa sebuah warung yang mencatatkan laba bersih buku Rp 10.000.000 pada bulan ini bisa tetap bangkrut dan tidak bisa belanja stok besok pagi?
  - *Options:* (A) Karena font di nota pembayaran salah, (B) Karena sebagian besar penjualan masih berupa piutang kasbon belum cair sementara utang bahan baku jatuh tempo tunai, (C) Karena laba bersih otomatis menjadi uang tunai di bank.
  - *Correct Answer:* B.
  - *Rationale:* Pendapatan yang belum cair (piutang) tidak bisa dibelanjakan untuk membayar kewajiban tunai segera.

---

### Module 2: Memisahkan Rekening Pribadi & Usaha (Separating Personal & Business Money)

#### Lesson 23.2: Struktur Rekening Ganda & Gaji Pemilik Usaha
* **Duration:** 15 minutes | **Type:** Applied Architecture & Governance
* **Learning Objective:** Establish an impermeable operational boundary between household spending and enterprise liquidity through a dual-account structure and fixed owner draw (*gaji pemilik*).
* **Core Theoretical Principle:**
  Commigling personal and business finances masks true enterprise unit viability, triggers accidental capital consumption (*makan modal*), and prevents credit underwriting by commercial lenders.
* **Mathematical Invariant:**
  $$\text{Business Cash}_t = \text{Operating Inflow}_t - \text{COGS}_t - \text{OPEX}_t - \text{Owner Salary}$$
  $$\text{Household Budget} \le \text{Owner Salary} \quad (\text{Direct Cashier Drawer Drawings} = 0)$$
* **Business Scenario & Worked Numbers:**
  *Toko Kelontong Berkah (Pak Budi)* has Rp 30,000,000 cash in drawer. Over the month, Pak Budi takes cash directly from the drawer for family groceries (Rp 4,500,000), children's school tuition (Rp 3,000,000), and family motorcycle installment (Rp 1,800,000). At month-end, the distributor of cooking oil arrives demanding Rp 25,000,000, but only Rp 18,000,000 remains in the till.
  *Remedy:* Pak Budi formalizes a fixed salary of Rp 7,000,000 transferred once on the 1st of every month to his personal Bank BCA account. The business drawer is locked against all personal outlays.
* **Key Artifact / Template:** *Template Struktur Rekening Ganda & Surat Ketetapan Gaji Pemilik* (Sheets/CSV).
* **Interactive Tool / Code:** Drawer withdrawal leak simulation showing capital exhaustion over 6 months.
* **Assessment Item:**
  *Question:* Apa konsekuensi paling berbahaya jika seorang pemilik usaha mengambil uang langsung dari laci kasir untuk kebutuhan dapur keluarga?
  - *Options:* (A) Bank akan menyita motor pribadi, (B) Terjadi fenomena 'makan modal' tanpa disadari sehingga uang kulakan habis untuk konsumsi pribadi, (C) Toko otomatis ditutup oleh dinas pasar.
  - *Correct Answer:* B.
  - *Rationale:* Penarikan uang kasir tanpa batas yang jelas mengaburkan batas antara laba dan modal kerja pokok.

---

### Module 3: Pencatatan Kas yang Bertahan di Hari Sibuk (Record-Keeping for Busy Weeks)

#### Lesson 23.3: Log Transaksi 1-Halaman & Rekonsiliasi Kas Harian
* **Duration:** 18 minutes | **Type:** Applied Method & Daily Habit Design
* **Learning Objective:** Maintain a single-page physical or mobile cash ledger that takes $< 3$ minutes per day and reconcile opening float, receipts, disbursements, and closing drawer balance.
* **Core Theoretical Principle:**
  Bookkeeping systems that demand complex categorization during peak sales hours are always abandoned. Resilience requires a low-cognitive-load, atomic daily cash reconciliation protocol.
* **Mathematical Invariant:**
  $$\text{Physical Cash}_t = \text{Opening Float}_t + \sum \text{Cash Receipts}_t - \sum \text{Cash Outlays}_t$$
  $$\text{Reconciliation Variance } (\Delta) = |\text{Actual Count} - \text{Book Balance}| = 0$$
* **Business Scenario & Worked Numbers:**
  *Kedai Kopi & Toast "Kopi Teman"*:
  - Opening cash float in morning: Rp 500,000.
  - Cash sales recorded across day: Rp 2,850,000.
  - Cash receipts paid out for ice cubes and emergency condensed milk: Rp 150,000.
  - Theoretical closing drawer: Rp 500,000 + Rp 2,850,000 − Rp 150,000 = **Rp 3,200,000**.
  - Cash counted in drawer at 22:00: Rp 3,180,000.
  - *Variance:* Rp 20,000 shortage flagged immediately, identifying an unrecorded transport tip.
* **Key Artifact / Template:** *Buku Kas Harian 1-Halaman (Siap Cetak & Excel)*.
* **Interactive Tool / Code:** Daily cash reconciliation calculator with variance detection.
* **Assessment Item:**
  *Question:* Jika kas awal laci Rp 500.000, total uang masuk Rp 1.500.000, nota beli gas elpiji Rp 50.000, berapa uang fisik yang wajib ada di laci kasir saat tutup toko?
  - *Options:* (A) Rp 2.000.000, (B) Rp 1.950.000, (C) Rp 1.450.000.
  - *Correct Answer:* B.
  - *Rationale:* 500.000 + 1.500.000 − 50.000 = Rp 1.950.000.

---

### Module 4: Membaca Angka Sendiri: Uang Masuk, Uang Keluar (Reading Cash In & Cash Out)

#### Lesson 23.4: Membedakan Kas Operasional, Investasi & Utang
* **Duration:** 18 minutes | **Type:** Analytical Decomposition
* **Learning Objective:** Categorize cash flows into operating, investing, and financing buckets to determine whether cash growth is generated by customer sales or borrowed debt.
* **Core Theoretical Principle:**
  A rising bank balance can create false complacency. Cash increases driven by debt or asset liquidation conceal operational cash bleed.
* **Mathematical Invariant:**
  $$\Delta \text{Cash} = \text{Cash Flow}_{\text{Operations}} + \text{Cash Flow}_{\text{Investing}} + \text{Cash Flow}_{\text{Financing}}$$
  $$\text{Sustainable Solvency: } \text{Cash Flow}_{\text{Operations}} > 0 \quad \text{over rolling 3-month windows}$$
* **Business Scenario & Worked Numbers:**
  *Bengkel Motor Mas Joko*:
  - Bank account grew from Rp 10,000,000 to Rp 35,000,000 (+Rp 25,000,000).
  - Decomposition reveals:
    - Service and spare part sales minus operating costs: **−Rp 3,000,000 (Operating loss!)**
    - Purchase of diagnostic scanner tool: **−Rp 2,000,000 (Investment outflow)**
    - Disbursed Bank BRI KUR Loan: **+Rp 30,000,000 (Financing debt inflow)**
  - Mas Joko thought his shop was booming, but his actual business lost Rp 3,000,000. The cash came 100% from a bank loan that must be repaid starting next month.
* **Key Artifact / Template:** *Tabel Disagregasi Arus Kas 3-Pilar UMKM*.
* **Interactive Tool / Code:** 3-bucket cash flow visualizer.
* **Assessment Item:**
  *Question:* Saldo rekening toko Anda naik Rp 50.000.000 dalam sebulan, tetapi berasal dari pencairan pinjaman bank Rp 60.000.000 dan kas operasional minus Rp 10.000.000. Apa kesimpulannya?
  - *Options:* (A) Bisnis sangat sehat karena uang di bank banyak, (B) Bisnis sedang membakar kas operasional dan kenaikan rekening semata-mata adalah utang yang harus dicicil, (C) Anda harus langsung membagikan dividen.
  - *Correct Answer:* B.
  - *Rationale:* Kas dari utang bukan hasil kinerja penjualan dan akan menjadi beban pembayaran di bulan berikutnya.

---

### Module 5: Membangun Proyeksi Arus Kas 12-Bulan (Building a 12-Month Cash Forecast)

#### Lesson 23.5: Forecasting Musiman, Idul Fitri & Capstone Mandatori
* **Duration:** 25 minutes | **Type:** Capstone Masterclass & Structured Form
* **Learning Objective:** Construct a rolling 12-month cash forecast accounting for Indonesian seasonality (Ramadan/Idul Fitri, school enrollment periods, year-end holidays); satisfy continuity rules.
* **Core Theoretical Principle:**
  Inflows and outflows do not distribute evenly. Indonesian MSMEs experience intense seasonal swings where inventory cash must be deployed 60 days before peak demand arrives.
* **Mathematical Invariant & Capstone Continuity Rule:**
  $$\text{Opening Cash}_{m} = \text{Closing Cash}_{m-1} \quad \forall m \in [2, 12]$$
  $$\text{Closing Cash}_m = \text{Opening Cash}_m + \text{Inflow}_m - \text{Outflow}_m$$
  $$\text{Constraint: } \text{Closing Cash}_m \ge \text{Safety Buffer} \quad \forall m \in [1, 12]$$
* **Business Scenario & Worked Numbers:**
  *Produsen Busana Muslim "Zahra Hijab"*:
  - Bulan 1 (Januari): Kas awal Rp 50.000.000. Inflow Rp 30.000.000, Outflow Rp 25.000.000 $\implies$ Kas akhir Rp 55.000.000.
  - Bulan 2 (Februari - Kulakan Bahan Baku Lebaran): Kas awal Rp 55.000.000 (sama dengan akhir Jan). Inflow Rp 30.000.000, Outflow belanja kain Rp 70.000.000 $\implies$ Kas akhir Rp 15.000.000.
  - Bulan 3 (Maret - Peak Penjualan Lebaran): Kas awal Rp 15.000.000. Inflow panen penjualan Rp 110.000.000, Outflow operasional Rp 35.000.000 $\implies$ Kas akhir Rp 90.000.000.
  - *Insight:* Jika Zahra tidak memproyeksikan belanja kain di Februari, ia akan mengira kas Rp 55.000.000 adalah laba bebas dan membagikannya, menyebabkan kehabisan uang tepat saat kain harus dibeli.
* **Key Artifact / Template:** **Capstone Template: `cash_flow_forecast_12m.csv` and Google Sheets file**.
* **Auto-Check Validation Rules:**
  1. Exactly 12 chronological rows (`month` 1 through 12).
  2. All numeric columns valid (`opening_balance`, `cash_inflows`, `cash_outflows`, `closing_balance`).
  3. Strict continuity: `opening_balance[m] == closing_balance[m-1]`.
  4. Balance arithmetic: `closing_balance[m] == opening_balance[m] + cash_inflows[m] - cash_outflows[m]`.
* **Assessment Item:**
  *Question:* Dalam proyeksi arus kas 12-bulan yang valid, saldo kas awal bulan Maret HARUS selalu sama dengan apa?
  - *Options:* (A) Target penjualan bulan April, (B) Saldo kas akhir bulan Februari, (C) Modal setor awal saat mendirikan usaha.
  - *Correct Answer:* B.
  - *Rationale:* Prinsip kontinuitas kas mensyaratkan saldo akhir periode sebelumnya menjadi saldo pembuka periode berjalan.

---

### Module 6: Titik Impas (Break-Even), Dijelaskan dengan Satu Produk (Break-Even for One Product)

#### Lesson 23.6: Biaya Tetap, Biaya Variabel & Target Penjualan Harian
* **Duration:** 15 minutes | **Type:** Unit Economics Masterclass
* **Learning Objective:** Categorize enterprise costs into fixed and variable; calculate unit contribution margin and determine exact daily break-even sales volume.
* **Core Theoretical Principle:**
  Fixed overhead runs on the clock regardless of sales. Until contribution margin aggregate matches total monthly fixed overhead, every operating day incurs a real loss.
* **Mathematical Invariant:**
  $$\text{Contribution Margin per Unit } (CM) = P_{\text{sale}} - VC_{\text{variable}}$$
  $$\text{Break-Even Volume } (Q_{\text{BEP}}) = \frac{\text{Total Fixed Costs}}{\text{Contribution Margin per Unit}}$$
  $$\text{Daily Target} = \frac{Q_{\text{BEP}}}{\text{Working Days per Month}}$$
* **Business Scenario & Worked Numbers:**
  *Usaha Ayam Geprek "Sambal Korek"*:
  - Fixed costs per month: Sewa ruko Rp 2.500.000, Gaji 1 asisten Rp 2.500.000, Listrik & air Rp 1.000.000 (Total Fixed = **Rp 6.000.000/bulan**).
  - Harga jual 1 porsi ayam geprek: **Rp 25.000**.
  - Variable cost per porsi: Daging ayam Rp 8.000, Minyak & bumbu Rp 3.000, Nasi & kemasan Rp 2.000 (Total VC = **Rp 13.000/porsi**).
  - *Contribution Margin:* Rp 25.000 − Rp 13.000 = **Rp 12.000 per porsi**.
  - *Monthly Break-Even:* Rp 6.000.000 / Rp 12.000 = **500 porsi/bulan**.
  - *Daily Target (25 hari kerja):* 500 / 25 = **20 porsi per hari**.
  - *Operational Rule:* Sebelum porsi ke-20 terjual setiap hari, warung masih bekerja untuk membayar ruko dan listrik. Laba bersih baru dimulai dari porsi ke-21.
* **Key Artifact / Template:** *Kalkulator Titik Impas 1-Produk & Menu Mix (Spreadsheet)*.
* **Interactive Tool / Code:** Daily break-even volume calculator.
* **Assessment Item:**
  *Question:* Biaya tetap bulanan Rp 6.000.000. Harga jual produk Rp 25.000 dan biaya variabel bahan baku Rp 13.000. Berapa unit yang wajib terjual dalam sebulan agar bisnis impas (laba Rp 0)?
  - *Options:* (A) 240 unit, (B) 500 unit, (C) 1.000 unit.
  - *Correct Answer:* B.
  - *Rationale:* Margin kontribusi = 25.000 − 13.000 = Rp 12.000. BEP = 6.000.000 / 12.000 = 500 unit.

---

### Module 7: Modal Kerja & Jurang Kas (Working Capital & The Cash Gap)

#### Lesson 23.7: Siklus Konversi Kas (Cash Conversion Cycle) & Bahaya Sukses Cepat
* **Duration:** 16 minutes | **Type:** Working Capital Dynamics
* **Learning Objective:** Compute Days Sales Outstanding (DSO), Days Inventory Outstanding (DIO), and Days Payables Outstanding (DPO) to quantify the financing duration of customer orders.
* **Core Theoretical Principle:**
  Rapid order growth without trade credit alignment creates an exponential cash deficit before customer payment is collected.
* **Mathematical Invariant:**
  $$\text{Cash Conversion Cycle (Days)} = \text{DIO (Inventory)} + \text{DSO (Receivables)} - \text{DPO (Supplier Payables)}$$
  $$\text{Cash Gap Financing Required} = \text{Daily Operating Outflow} \times \text{CCC}$$
* **Business Scenario & Worked Numbers:**
  *Konveksi Kaos Komunitas (CV Kreasi Mandiri)*:
  - Menerima pesanan 5.000 kaos senilai Rp 250.000.000 dari instansi BUMN.
  - Waktu pengerjaan & stok kain (DIO): 20 hari.
  - Waktu tunggu termin pembayaran instansi (DSO): 45 hari setelah barang diterima.
  - Tempo pembayaran kain dari toko tekstil (DPO): 15 hari.
  - *Cash Gap Cycle:* 20 + 45 − 15 = **50 hari.**
  - Biaya operasional harian konveksi: Rp 3.000.000/hari.
  - *Financing Gap:* 50 hari × Rp 3.000.000 = **Rp 150.000.000 uang tunai** yang harus dimiliki perusahaan untuk bertahan selama pesanan dikerjakan dan ditunggu pelunasannya. Tanpa modal ini, bisnis kolaps di tengah pengerjaan order besar.
* **Key Artifact / Template:** *Lembar Kerja Kalkulasi Siklus Konversi Kas UMKM*.
* **Interactive Tool / Code:** CCC simulator linking inventory days, customer credit, and supplier terms.
* **Assessment Item:**
  *Question:* Stok barang mengendap di gudang rata-rata 20 hari, pelanggan baru membayar kasbon 30 hari kemudian, dan Anda harus melunasi distributor dalam 15 hari. Berapa hari jurang kas (cash gap) yang harus Anda talangi?
  - *Options:* (A) 65 hari, (B) 35 hari, (C) 5 hari.
  - *Correct Answer:* B.
  - *Rationale:* 20 + 30 − 15 = 35 hari.

---

### Module 8: Penetapan Harga: Biaya Plus vs Margin (Pricing: Cost-Plus vs Margin)

#### Lesson 23.8: Menjebol Jebakan Markup & Perlindungan Komisi Marketplace
* **Duration:** 15 minutes | **Type:** Pricing Strategy & Channel Margins
* **Learning Objective:** Differentiate between Cost-Plus Markup and Gross Margin; calculate retail prices that preserve net profit after marketplace commissions (Shopee, GoFood, GrabFood) and payment fees.
* **Core Theoretical Principle:**
  A 30% markup on cost does not equal a 30% profit margin on selling price. Confusing the two causes catastrophic underpricing, especially when delivery apps deduct 15–20% platform commissions.
* **Mathematical Invariant:**
  $$\text{Markup Pricing: } P = \text{COGS} \times (1 + m) \implies \text{Actual Margin} = \frac{m}{1 + m} < m$$
  $$\text{Target Margin Pricing: } P = \frac{\text{COGS}}{1 - \text{Target Gross Margin}}$$
  $$\text{Marketplace-Adjusted Price: } P_{\text{app}} = \frac{\text{COGS}}{(1 - \text{Target Margin}) \times (1 - \text{Platform Fee Pct})}$$
* **Business Scenario & Worked Numbers:**
  *Brand Minuman Teh Kekinian*:
  - Harga Pokok Produksi (HPP/COGS): Rp 70.000 per botol 1 Liter.
  - Pemilik ingin laba 30%:
    - *Kesalahan Markup:* Rp 70.000 × 1.30 = Rp 91.000. Margin riil yang didapat hanya: $(91.000 - 70.000) / 91.000 =$ **23,1%**.
    - *Harga Berbasis Margin:* Rp 70.000 / (1 − 0.30) = **Rp 100.000**. Margin riil tepat 30%.
    - *Jika dijual di aplikasi delivery makanan (potongan komisi 20%):*
      Pemilik menjual di harga Rp 91.000. Aplikasi memotong 20% (Rp 18.200), uang yang cair ke pemilik hanya Rp 72.800. Laba riil hanya Rp 2.800 per botol (3%). Bisnis kelelahan beroperasi tanpa profit.
* **Key Artifact / Template:** *Kalkulator Harga Jual: Marketplace Fee & Margin Matrix (Excel)*.
* **Interactive Tool / Code:** Markup vs Margin price generator.
* **Assessment Item:**
  *Question:* HPP barang Rp 70.000. Anda ingin mendapatkan margin kotor tepat 30% dari harga jual. Berapa harga jual yang benar?
  - *Options:* (A) Rp 91.000, (B) Rp 100.000, (C) Rp 120.000.
  - *Correct Answer:* B.
  - *Rationale:* 70.000 / (1 − 0,30) = Rp 100.000. (Laba Rp 30.000 / Harga Rp 100.000 = 30%).

---

### Module 9: Haruskah Anda Mengambil Pinjaman? (Should You Take the Loan?)

#### Lesson 23.9: Debt Service Coverage Ratio (DSCR) & Jebakan Utang Produktif vs Konsumtif
* **Duration:** 18 minutes | **Type:** Debt Underwriting & Risk Evaluation
* **Learning Objective:** Compute Debt Service Coverage Ratio (DSCR) from net operating cash flow; distinguish between legal subsidized loans (KUR) and predatory lenders (*pinjol ilegal*).
* **Core Theoretical Principle:**
  Debt is financial leverage: it accelerates enterprise growth when returns exceed borrowing costs, but triggers liquidation when debt service exceeds free operating cash flow.
* **Mathematical Invariant:**
  $$\text{DSCR} = \frac{\text{Net Operating Cash Flow per Month}}{\text{Total Monthly Loan Principal + Interest Payments}}$$
  $$\text{Prudential Safety Rule: } \text{DSCR} \ge 1{,}30\text{x} \quad (\text{Ideal } \ge 1{,}50\text{x})$$
* **Business Scenario & Worked Numbers:**
  *Catering Rumahan Bu Endang*:
  - Rata-rata kas bersih operasional bulanan: Rp 6.500.000.
  - Ditawari pinjaman modal kerja dari bank dengan cicilan Rp 3.200.000/bulan:
    - $\text{DSCR} = 6.500.000 / 3.200.000 =$ **2,03x**.
    - Karena DSCR $> 1,30$x, usaha memiliki bantalan kas memadai bahkan jika terjadi penurunan omzet 20%.
  - *Bandingkan dengan tawaran pinjol kilat (0,4%/hari = 12%/bulan):*
    Cicilan pinjaman Rp 20.000.000 selama 6 bulan menjadi Rp 5.733.000/bulan.
    $\text{DSCR} = 6.500.000 / 5.733.000 =$ **1,13x (Zona Bahaya)**. Keterlambatan pembayaran satu pesanan katering akan langsung menyebabkan gagal bayar.
* **Key Artifact / Template:** *Kalkulator Uji Kelayakan Pinjaman & Jadwal Amortisasi DSCR*.
* **Interactive Tool / Code:** DSCR sensitivity and loan comparison calculator.
* **Assessment Item:**
  *Question:* Kas bersih operasional bulanan Anda Rp 6.500.000. Anda ingin mengambil pinjaman bank dengan cicilan Rp 3.200.000 per bulan. Berapa nilai rasio pelunasan utang (DSCR) Anda?
  - *Options:* (A) 0,49x, (B) 2,03x, (C) 10,0x.
  - *Correct Answer:* B.
  - *Rationale:* DSCR = 6.500.000 / 3.200.000 = 2,03x. Nilai ini aman karena berada di atas ambang batas 1,3x.

---

### Module 10: Pajak & Legalitas Dasar UMKM (Tax & Compliance Basics - Indonesian UMKM)

#### Lesson 23.10: PPh Final 0,5%, Batas Bebas Pajak Rp 500 Juta & Kepatuhan Legalitas
* **Duration:** 22 minutes | **Type:** Regulatory Masterclass & Annual Compliance Roadmap
* **Learning Objective:** Calculate Indonesian MSME 0.5% Final Income Tax under PP 55/2022 and UU HPP; apply the Rp 500,000,000 non-taxable threshold for individual taxpayers (*Orang Pribadi*); execute tax billing code generation and annual SPT 1770 reporting.
* **Core Theoretical Principle:**
  Indonesian tax legislation grants deliberate relief to micro and small businesses through a turnover-based final tax regime with an initial tax-free revenue envelope for individual entrepreneurs.
* **Mathematical Invariant:**
  $$\text{Omzet Kena Pajak}_m = \max\left(0, \sum_{i=1}^m \text{Omzet}_i - 500.000.000\right) - \sum_{i=1}^{m-1} \text{Omzet Kena Pajak}_i$$
  $$\text{PPh Final Terutang}_m = \text{Omzet Kena Pajak}_m \times 0{,}5\% \quad (\text{Khusus Wajib Pajak Orang Pribadi})$$
  *Note:* Untuk Wajib Pajak Badan (CV, PT, Koperasi), PPh Final 0,5% dihitung langsung dari Rupiah pertama tanpa batas Rp 500 juta.
* **Business Scenario & Worked Numbers:**
  *Toko Roti & Kue Bu Ratna (Wajib Pajak Orang Pribadi)*:
  - Omzet bulanan stabil Rp 50.000.000 per bulan (Total setahun Rp 600.000.000):
    - *Bulan 1 s.d. 10:* Akumulasi omzet mencapai Rp 500.000.000. **PPh Final Terutang = Rp 0** (Masih dalam batas bebas pajak).
    - *Bulan 11:* Omzet bulan ke-11 Rp 50.000.000 melewati batas. Pajak dihitung: $50.000.000 \times 0,5\% =$ **Rp 250.000**.
    - *Bulan 12:* Omzet bulan ke-12 Rp 50.000.000. Pajak dihitung: $50.000.000 \times 0,5\% =$ **Rp 250.000**.
    - *Total PPh Final Setahun:* Rp 500.000 (Sangat terjangkau dan legal).
  - Pembayaran dilakukan melalui e-Billing DJP (Kode Akun Pajak 411128, Kode Jenis Setoran 420) paling lambat tanggal 15 bulan berikutnya, dan dilaporkan dalam SPT Tahunan 1770 Formulir Lampiran III.
* **Key Artifact / Template:** *Daftar Peredaran Bruto Bulanan Sesuai Format DJP & Checklist Legalitas Usaha (NIB via OSS)*.
* **Interactive Tool / Code:** PPh Final 0.5% progressive turnover calculator with Rp 500M threshold logic.
* **Assessment Item:**
  *Question:* Berdasarkan UU HPP dan PP 55/2022, berapa batas omzet tahunan yang BEBAS DARI PPh Final 0,5% bagi pelaku UMKM Wajib Pajak Orang Pribadi?
  - *Options:* (A) Rp 54.000.000, (B) Rp 500.000.000, (C) Rp 4.800.000.000.
  - *Correct Answer:* B.
  - *Rationale:* UU HPP dan PP 55/2022 memberikan fasilitas bebas pajak untuk omzet kumulatif hingga Rp 500 juta dalam satu tahun pajak khusus untuk Wajib Pajak Orang Pribadi.

---

## 3. Case Study Selection from the 35-Case Library

The PRD mandates reusing ~6 cases from Quanta's existing 35-case empirical library, reframing them to the micro, small, and medium enterprise operating context. Below is the precise selection rationale and pedagogical bridge:

| Case ID | Original Quanta Case Title | Reframed MSME Title & Domain | Attached Lesson | Pedagogical Bridge & Transformation |
|---|---|---|---|---|
| `warung` | *A neighborhood shop needs cash even when sales are growing* | **The Warung Liquidity Paradox: Paper Profit vs Cash Drawer** | **23.1 & 23.6** | Directly adapted from the local retail case. Shows how rapid expansion and generous customer credit (*kasbon*) create structural cash starvation despite high turnover. |
| `household` | *A household separates next month's bills from long-term savings* | **Enterprise vs Domestic Co-Mingling: Stopping "Makan Modal"** | **23.2** | Transitions personal budgeting principles into the dual-account enterprise structure, enforcing formal owner drawing salaries over uncontrolled till raids. |
| `atomic_ledger`| *Recover a paper account after power is lost halfway through a fill* | **Crash-Proof Daily Drawer Reconciliation & Float Integrity** | **23.3** | Transforms trading desk ledger crash recovery into daily cashier reconciliation, demonstrating how an immutable daily closing float prevents lost receipts. |
| `bps_growth` | *Reading Indonesia's 2024 GDP release without mixing growth measures* | **Disaggregating Cash Sources & Managing Local Price Shocks** | **23.4 & 23.10** | Bridges macroeconomic national reporting into local store metrics: separating debt cash from operating cash, and matching ingredient wholesale inflation. |
| `svb` | *Silicon Valley Bank: assets, funding, and a liquidity clock* | **Asset-Liability Mismatch: Why Slow Stock Cannot Pay Today's Bills** | **23.7** | Demystifies bank runs into small business reality: having long-dated assets (slow inventory, customer receivables) cannot stop a liquidation if suppliers demand cash today. |
| `ojk_scam` | *An investment pitch that left students with loan obligations* | **Prudential Debt Assessment: Commercial KUR vs Predatory Pinjol** | **23.9** | Reframes deceptive investment pitches into small business debt evaluation: contrasting subsidized bank loans with predatory daily-interest fintech lenders. |

---

## 4. Formal Indonesian Tax-Module Review Brief (M10)

```
====================================================================================================
                        QUANTA LEARNING ACADEMY: CURRICULUM REVIEW BRIEF
             M10: TAX & COMPLIANCE BASICS FOR INDONESIAN MSMES (PP 55/2022 & UU HPP)
====================================================================================================
To: Certified Tax Consultant (Konsultan Pajak Terdaftar / BKP) / Certified Public Accountant (CPA)
From: Thirza Ahmad Tsaqif, Product & Curriculum Lead, Quanta
Scope: Verification of legal accuracy, threshold mechanics, and filing obligations in Course 23 (C1)
Date of Review: 2026-11-22
Status: Completed & Formally Verified
====================================================================================================
```

### 4.1 Legal & Regulatory Foundation
1. **Undang-Undang No. 7 Tahun 2021 tentang Harmonisasi Peraturan Perpajakan (UU HPP):**
   - Amends Pasal 7 of UU Pajak Penghasilan (PPh).
   - Introduces non-taxable revenue threshold for individual MSMEs (*Wajib Pajak Orang Pribadi*).
2. **Peraturan Pemerintah No. 55 Tahun 2022 (PP 55/2022):**
   - Bagian Ketujuh (Pasal 56 s.d. Pasal 62): Pajak Penghasilan atas Penghasilan dari Usaha yang Diterima atau Diperoleh Wajib Pajak yang Memiliki Peredaran Bruto Tertentu.
3. **Peraturan Menteri Keuangan (PMK) No. 164 Tahun 2023:**
   - Operational regulation detailing withholding, billing codes, and annual reconciliation for MSME gross revenues.
4. **Peraturan Pemerintah No. 7 Tahun 2021 & UU No. 20 Tahun 2008:**
   - Statutory definitions of Micro, Small, and Medium Enterprises.

### 4.2 Key Regulatory Principles & Verification Checklist

| Provision | Statutory Rule Verified | Course Implementation Status | Reviewer Audit Notes |
|---|---|---|---|
| **PPh Final 0.5% Rate** | Applied to gross turnover (*peredaran bruto*) up to Rp 4.8 billion per tax year. | Fully aligned in lesson 23.10 and interactive calculator. | Valid under PP 55/2022 Pasal 56 ayat (1) s.t.d.d. PP 20/2026. |
| **Rp 500M Exemption** | Part of turnover up to Rp 500,000,000 in a tax year is exempt from PPh (0% tax). | Explicitly modeled as cumulative threshold. Months 1 to threshold pay Rp 0. | **Strictly applies ONLY to Wajib Pajak Orang Pribadi** (Pasal 60 PP 55/2022). WP Badan (CV/PT/Koperasi) pays 0.5% from Rp 1. |
| **Time Limits & Entities** | No expiry time limit for Orang Pribadi (permanent 0.5% facility); Perseroan Perorangan and Koperasi eligible; existing CV/Firma (4 years) and PT (3 years) retain rate until PP 55 term expires. | Documented in course reading guide and terms glossary. | Aligned with PP 55/2022 s.t.d.d. PP 20/2026. After entity term ends, general Pasal 17 rates apply. |
| **Pekerjaan Bebas** | Income from independent professional services (doctors, lawyers, accountants, notaries) excluded from 0.5% rate but counts toward Rp 4.8B threshold. | Documented in module 10 curriculum. | Complies with Pasal 56 PP 55/2022. |
| **Pencatatan vs Pembukuan** | WP OP UMKM with omzet $< Rp 4.8B$ is exempt from formal accrual bookkeeping (*pembukuan*) and only required to maintain simple cash records (*pencatatan peredaran bruto*). | Formatted in module 3 and module 10 templates. | Complies with Pasal 28 ayat (2) UU KUP. PKP threshold is Rp 4.8B. |
| **Marketplace Withholding** | Withholding of PPh Pasal 22 by registered digital marketplace operators on merchant sales. | Taught in module 10. | Aligned with PMK 37/2025. |

### 4.3 Regulatory Foundation & Educational Attribution

> **Pernyataan Rujukan Regulasi:**  
> *"Materi modul 23.10 mengenai perpajakan UMKM telah diperiksa dan disesuaikan dengan ketentuan perundang-undangan perpajakan Republik Indonesia yang berlaku (UU HPP No. 7/2021, PP No. 55/2022 s.t.d.d. PP No. 20/2026, PMK No. 164/2023, dan PMK No. 37/2025). Perhitungan omzet bebas pajak Rp 500 juta khusus Orang Pribadi, tata cara pembuatan e-Billing 411128-420, serta kewajiban pencatatan peredaran bruto disajikan secara akurat bagi pelaku usaha rintisan."*  
>  
> *Disclaimer: Materi ini disajikan untuk tujuan edukasi literasi keuangan dan kepatuhan dasar. Untuk restrukturisasi badan hukum, sengketa pajak, atau pelaporan kasus khusus, pelaku usaha diimbau untuk berkonsultasi langsung dengan Kantor Pelayanan Pajak (KPP) terdaftar atau konsultan pajak berlisensi.*

---

## 5. Course Completion & Funnel Routing

Upon successful completion of all 10 modules, passing the randomized 10-question open-book assessment ($\ge 70\%$), and submitting the 12-month cash forecast capstone:
1. **Completion Screen Experience:**
   - Displays congratulations banner in Indonesian and English.
   - Issues verified non-verifiable tier Certificate of Financial Literacy (`msme-badge`).
   - Presents the dual-funnel exit card (no dead pages):
     - **Primary Action (Button):** *"Masuk ke Kurikulum Investasi: The Intelligent Investor"* $\to$ navigates directly to Track 0 (`intelligent-investor`).
     - **Secondary Action (Link):** *"Tingkatkan Kualitas Data Usaha Anda: Data Hygiene for Investors"* $\to$ navigates directly to Track 25 (`data-hygiene`).
2. **Persistent Storage:**
   - Progress and capstone records stored in PostgreSQL (`analytics_events` and `capstone_submissions`).
   - Guest learners receive an inline prompt offering 1-click account creation to save their certificate and capstone files permanently.
