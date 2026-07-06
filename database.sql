-- ============================================================
-- Capstone Project Module 1
-- Case Study: Sistem Informasi Pasien Rumah Sakit
-- Skema 5 tabel: pasien, dokter, ruangan, diagnosis, kunjungan
-- ============================================================

CREATE DATABASE IF NOT EXISTS rumah_sakit;
USE rumah_sakit;

-- Drop dalam urutan terbalik karena kunjungan mereferensikan tabel lain
DROP TABLE IF EXISTS kunjungan;
DROP TABLE IF EXISTS pasien;
DROP TABLE IF EXISTS dokter;
DROP TABLE IF EXISTS ruangan;
DROP TABLE IF EXISTS diagnosis;

-- ============================================================
-- 1. TABEL DOKTER
-- ============================================================
CREATE TABLE dokter (
    id_dokter    VARCHAR(10)  NOT NULL PRIMARY KEY,
    nama_dokter  VARCHAR(100) NOT NULL,
    spesialisasi VARCHAR(50)  NOT NULL,
    no_telp      VARCHAR(20)
);

INSERT INTO dokter VALUES
('D01', 'Dr. Adi Nugroho',    'Penyakit Dalam', '021-555-0001'),
('D02', 'Dr. Bayu Wijaya',    'Jantung',        '021-555-0002'),
('D03', 'Dr. Citra Kirana',   'Bedah',          '021-555-0003'),
('D04', 'Dr. Dini Aulia',     'Anak',           '021-555-0004'),
('D05', 'Dr. Eka Pratiwi',    'Saraf',          '021-555-0005'),
('D06', 'Dr. Fajar Hidayat',  'Penyakit Dalam', '021-555-0006'),
('D07', 'Dr. Gita Permata',   'Mata',           '021-555-0007'),
('D08', 'Dr. Hadi Surya',     'Jantung',        '021-555-0008');

-- ============================================================
-- 2. TABEL RUANGAN
-- ============================================================
CREATE TABLE ruangan (
    id_ruangan     VARCHAR(10)    NOT NULL PRIMARY KEY,
    nama_ruangan   VARCHAR(50)    NOT NULL,
    kelas          VARCHAR(20)    NOT NULL,
    tarif_per_hari DECIMAL(12, 2) NOT NULL
);

INSERT INTO ruangan VALUES
('R01', 'Mawar 101',            'VIP',        1500000.00),
('R02', 'Anggrek 201',          'Kelas I',    1000000.00),
('R03', 'Melati 301',           'Kelas II',    700000.00),
('R04', 'Dahlia 401',           'Kelas III',   400000.00),
('R05', 'IGD Utama',            'IGD',               0.00),
('R06', 'Poli Penyakit Dalam',  'Poliklinik',        0.00),
('R07', 'Poli Jantung',         'Poliklinik',        0.00),
('R08', 'Tulip VIP',            'VIP',        1800000.00);

-- ============================================================
-- 3. TABEL DIAGNOSIS
-- ============================================================
CREATE TABLE diagnosis (
    kode_dx        VARCHAR(10)  NOT NULL PRIMARY KEY,
    nama_diagnosis VARCHAR(100) NOT NULL,
    kategori       VARCHAR(50)  NOT NULL
);

INSERT INTO diagnosis VALUES
('DX01', 'Hipertensi',       'Penyakit Dalam'),
('DX02', 'Diabetes Melitus', 'Penyakit Dalam'),
('DX03', 'Gagal Jantung',    'Jantung'),
('DX04', 'Aritmia',          'Jantung'),
('DX05', 'Apendisitis',      'Bedah'),
('DX06', 'Demam Tifoid',     'Penyakit Dalam'),
('DX07', 'Gastritis',        'Penyakit Dalam'),
('DX08', 'Bronkopneumonia',  'Anak'),
('DX09', 'Stroke',           'Saraf'),
('DX10', 'Migrain',          'Saraf'),
('DX11', 'Katarak',          'Mata'),
('DX12', 'ISPA',             'Anak');

-- ============================================================
-- 4. TABEL PASIEN
-- ============================================================
CREATE TABLE pasien (
    id_pasien     VARCHAR(10)  NOT NULL PRIMARY KEY,
    nama_pasien   VARCHAR(100) NOT NULL,
    usia          INT          NOT NULL,
    jenis_kelamin VARCHAR(10)  NOT NULL,
    alamat        VARCHAR(200),
    no_telp       VARCHAR(20)
);

INSERT INTO pasien VALUES
('P001', 'Budi Santoso',        45, 'L', 'Jl. Mawar 12, Jakarta',       '0812-1111-0001'),
('P002', 'Siti Rahayu',         32, 'P', 'Jl. Melati 8, Bandung',       '0812-1111-0002'),
('P003', 'Ahmad Fauzi',         67, 'L', 'Jl. Kenanga 22, Jakarta',     '0812-1111-0003'),
('P004', 'Dewi Lestari',        28, 'P', 'Jl. Anggrek 5, Surabaya',     '0812-1111-0004'),
('P005', 'Rini Wulandari',      55, 'P', 'Jl. Cendana 17, Jakarta',     '0812-1111-0005'),
('P006', 'Hendra Gunawan',      40, 'L', 'Jl. Dahlia 9, Bandung',       '0812-1111-0006'),
('P007', 'Yuliana Putri',       23, 'P', 'Jl. Flamboyan 3, Jakarta',    '0812-1111-0007'),
('P008', 'Bambang Sutrisno',    72, 'L', 'Jl. Kamboja 11, Bekasi',      '0812-1111-0008'),
('P009', 'Maya Sari',           36, 'P', 'Jl. Tulip 6, Tangerang',      '0812-1111-0009'),
('P010', 'Eko Prasetyo',        50, 'L', 'Jl. Bougenville 14, Depok',   '0812-1111-0010'),
('P011', 'Fitri Handayani',     29, 'P', 'Jl. Aster 7, Jakarta',        '0812-1111-0011'),
('P012', 'Doni Kurniawan',      44, 'L', 'Jl. Bunga 19, Bandung',       '0812-1111-0012'),
('P013', 'Sri Wahyuni',         61, 'P', 'Jl. Wijaya 4, Jakarta',       '0812-1111-0013'),
('P014', 'Agus Setiawan',       38, 'L', 'Jl. Soka 21, Bekasi',         '0812-1111-0014'),
('P015', 'Lina Marlina',        52, 'P', 'Jl. Edelweis 8, Jakarta',     '0812-1111-0015'),
('P016', 'Reza Pratama',         7, 'L', 'Jl. Sakura 2, Bandung',       '0812-1111-0016'),
('P017', 'Indah Permatasari',   41, 'P', 'Jl. Teratai 13, Jakarta',     '0812-1111-0017'),
('P018', 'Joko Susilo',         58, 'L', 'Jl. Bakung 5, Surabaya',      '0812-1111-0018'),
('P019', 'Nurul Hidayah',       33, 'P', 'Jl. Lavender 9, Tangerang',   '0812-1111-0019'),
('P020', 'Tono Sugiarto',       65, 'L', 'Jl. Mawar 27, Jakarta',       '0812-1111-0020'),
('P021', 'Vina Anggraini',      26, 'P', 'Jl. Lotus 11, Depok',         '0812-1111-0021'),
('P022', 'Rangga Maulana',      12, 'L', 'Jl. Pinus 8, Bandung',        '0812-1111-0022'),
('P023', 'Endah Sulistiowati',  47, 'P', 'Jl. Cempaka 6, Bekasi',       '0812-1111-0023'),
('P024', 'Bagas Wicaksono',     34, 'L', 'Jl. Akasia 14, Jakarta',      '0812-1111-0024'),
('P025', 'Tania Maharani',      19, 'P', 'Jl. Seroja 3, Bandung',       '0812-1111-0025');

-- ============================================================
-- 5. TABEL KUNJUNGAN (transaksi utama, menjembatani semua master)
-- ============================================================
CREATE TABLE kunjungan (
    id_kunjungan VARCHAR(10)    NOT NULL PRIMARY KEY,
    id_pasien    VARCHAR(10)    NOT NULL,
    id_dokter    VARCHAR(10)    NOT NULL,
    id_ruangan   VARCHAR(10)    NOT NULL,
    kode_dx      VARCHAR(10)    NOT NULL,
    tgl_masuk    DATE           NOT NULL,
    tgl_keluar   DATE,
    status_rawat VARCHAR(20)    NOT NULL,
    biaya        DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (id_pasien)  REFERENCES pasien(id_pasien),
    FOREIGN KEY (id_dokter)  REFERENCES dokter(id_dokter),
    FOREIGN KEY (id_ruangan) REFERENCES ruangan(id_ruangan),
    FOREIGN KEY (kode_dx)    REFERENCES diagnosis(kode_dx)
);

INSERT INTO kunjungan VALUES
('K001','P001','D01','R03','DX01','2026-01-05','2026-01-08','Rawat Inap',   3500000.00),
('K002','P002','D06','R06','DX02','2026-01-07','2026-01-07','Rawat Jalan',   850000.00),
('K003','P003','D02','R01','DX03','2026-01-09','2026-01-16','Rawat Inap',  15500000.00),
('K004','P004','D03','R04','DX05','2026-01-12','2026-01-15','Rawat Inap',   4200000.00),
('K005','P005','D01','R06','DX01','2026-01-14','2026-01-14','Rawat Jalan',   650000.00),
('K006','P006','D06','R03','DX02','2026-01-19','2026-01-23','Rawat Inap',   4400000.00),
('K007','P007','D03','R05','DX05','2026-01-26','2026-01-26','IGD',          1500000.00),
('K008','P008','D08','R08','DX03','2026-02-02','2026-02-11','Rawat Inap',  19500000.00),
('K009','P009','D01','R06','DX07','2026-02-04','2026-02-04','Rawat Jalan',   450000.00),
('K010','P010','D02','R05','DX04','2026-02-06','2026-02-06','IGD',          2800000.00),
('K011','P011','D01','R04','DX06','2026-02-09','2026-02-11','Rawat Inap',   2100000.00),
('K012','P012','D06','R06','DX01','2026-02-13','2026-02-13','Rawat Jalan',   720000.00),
('K013','P013','D08','R01','DX03','2026-02-16','2026-02-24','Rawat Inap',  16800000.00),
('K014','P014','D01','R05','DX07','2026-02-18','2026-02-18','IGD',           900000.00),
('K015','P015','D06','R02','DX02','2026-03-03','2026-03-07','Rawat Inap',   5800000.00),
('K016','P016','D04','R04','DX08','2026-03-05','2026-03-08','Rawat Inap',   2700000.00),
('K017','P017','D05','R06','DX10','2026-03-09','2026-03-09','Rawat Jalan',   800000.00),
('K018','P018','D05','R01','DX09','2026-03-11','2026-03-19','Rawat Inap',  18500000.00),
('K019','P019','D04','R06','DX12','2026-03-13','2026-03-13','Rawat Jalan',   550000.00),
('K020','P020','D07','R02','DX11','2026-03-16','2026-03-18','Rawat Inap',   8200000.00),
('K021','P021','D04','R05','DX12','2026-03-20','2026-03-20','IGD',          1100000.00),
('K022','P022','D04','R04','DX08','2026-04-02','2026-04-05','Rawat Inap',   2400000.00),
('K023','P023','D01','R06','DX07','2026-04-06','2026-04-06','Rawat Jalan',   500000.00),
('K024','P024','D02','R07','DX04','2026-04-08','2026-04-08','Rawat Jalan',  1200000.00),
('K025','P025','D04','R06','DX12','2026-04-10','2026-04-10','Rawat Jalan',   480000.00),
('K026','P001','D06','R06','DX01','2026-04-14','2026-04-14','Rawat Jalan',   650000.00),
('K027','P003','D02','R07','DX03','2026-04-17','2026-04-17','Rawat Jalan',  1500000.00),
('K028','P005','D06','R06','DX01','2026-04-21','2026-04-21','Rawat Jalan',   620000.00),
('K029','P008','D08','R07','DX03','2026-05-04','2026-05-04','Rawat Jalan',  1450000.00),
('K030','P010','D01','R06','DX02','2026-05-06','2026-05-06','Rawat Jalan',   780000.00),
('K031','P013','D02','R08','DX04','2026-05-08','2026-05-15','Rawat Inap',  17200000.00),
('K032','P006','D01','R06','DX02','2026-05-11','2026-05-11','Rawat Jalan',   850000.00),
('K033','P018','D05','R06','DX10','2026-05-13','2026-05-13','Rawat Jalan',   900000.00),
('K034','P020','D07','R06','DX11','2026-05-18','2026-05-18','Rawat Jalan',   650000.00),
('K035','P007','D03','R04','DX05','2026-05-20','2026-05-23','Rawat Inap',   3800000.00),
('K036','P002','D06','R06','DX02','2026-06-02','2026-06-02','Rawat Jalan',   870000.00),
('K037','P017','D05','R06','DX10','2026-06-05','2026-06-05','Rawat Jalan',   780000.00),
('K038','P004','D03','R03','DX05','2026-06-08','2026-06-11','Rawat Inap',   4500000.00),
('K039','P011','D01','R06','DX06','2026-06-12','2026-06-12','Rawat Jalan',   600000.00),
('K040','P015','D06','R06','DX02','2026-06-16','2026-06-16','Rawat Jalan',   820000.00);
