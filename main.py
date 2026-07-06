import mysql.connector
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import date, datetime

# ─── Konfigurasi koneksi MySQL ───────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "rumah_sakit"
}


def get_connection():
    """Membuat koneksi ke database MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 1 – LIHAT DATA KUNJUNGAN (INNER JOIN 5 tabel + ORDER BY)
# ══════════════════════════════════════════════════════════════════════════════

def lihat_kunjungan():
    """Menampilkan seluruh kunjungan beserta data pasien, dokter, ruangan,
    dan diagnosis lewat INNER JOIN 5 tabel."""
    print("\n" + "=" * 100)
    print("           DATA KUNJUNGAN PASIEN (JOIN 5 tabel)")
    print("=" * 100)

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT  k.id_kunjungan,
                    p.nama_pasien,
                    p.usia,
                    d.nama_dokter,
                    d.spesialisasi,
                    r.kelas,
                    dx.nama_diagnosis,
                    k.tgl_masuk,
                    k.status_rawat,
                    k.biaya
            FROM    kunjungan  k
            INNER JOIN pasien    p  ON k.id_pasien  = p.id_pasien
            INNER JOIN dokter    d  ON k.id_dokter  = d.id_dokter
            INNER JOIN ruangan   r  ON k.id_ruangan = r.id_ruangan
            INNER JOIN diagnosis dx ON k.kode_dx    = dx.kode_dx
            ORDER BY k.tgl_masuk DESC, k.id_kunjungan
        """)
        rows = cursor.fetchall()

        if not rows:
            print("Tidak ada data kunjungan.")
            return

        headers = ["ID", "Pasien", "Usia", "Dokter", "Spesialisasi",
                   "Kelas", "Diagnosis", "Tgl Masuk", "Status", "Biaya (Rp)"]
        formatted = [
            (r[0], r[1], r[2], r[3], r[4], r[5], r[6],
             r[7].strftime("%Y-%m-%d"), r[8], f"{r[9]:,.0f}")
            for r in rows
        ]
        print(tabulate(formatted, headers=headers, tablefmt="grid"))
        print(f"\nTotal kunjungan: {len(rows)}")

    except mysql.connector.Error as e:
        print(f"[ERROR] Gagal mengambil data: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 2 – STATISTIK DESKRIPTIF (Aggregate + GROUP BY lintas tabel)
# ══════════════════════════════════════════════════════════════════════════════

def show_statistik():
    """Menampilkan statistik deskriptif numerik dan agregasi GROUP BY
    pada kategori diagnosis, kelas ruangan, dan spesialisasi dokter."""
    print("\n" + "=" * 70)
    print("         STATISTIK DESKRIPTIF KUNJUNGAN PASIEN")
    print("=" * 70)

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # ── Statistik biaya & usia global ─────────────────────────
        cursor.execute("""
            SELECT  COUNT(*),
                    AVG(k.biaya), MIN(k.biaya), MAX(k.biaya),
                    SUM(k.biaya), STDDEV(k.biaya),
                    AVG(p.usia), MIN(p.usia), MAX(p.usia)
            FROM    kunjungan k
            INNER JOIN pasien p ON k.id_pasien = p.id_pasien
        """)
        s = cursor.fetchone()

        print("\n  [Ringkasan Umum]")
        print(f"  Jumlah Kunjungan : {int(s[0])}")
        print(f"  Rata-rata Biaya  : Rp {float(s[1]):>14,.2f}")
        print(f"  Biaya Terendah   : Rp {float(s[2]):>14,.2f}")
        print(f"  Biaya Tertinggi  : Rp {float(s[3]):>14,.2f}")
        print(f"  Total Pendapatan : Rp {float(s[4]):>14,.2f}")
        print(f"  Std. Deviasi     : Rp {float(s[5]):>14,.2f}")
        print(f"  Rata-rata Usia   : {float(s[6]):.1f} tahun "
              f"(min {int(s[7])}, max {int(s[8])})")

        # ── Per kategori diagnosis (GROUP BY) ─────────────────────
        cursor.execute("""
            SELECT  dx.kategori,
                    COUNT(*)        AS jml,
                    AVG(k.biaya)    AS rata,
                    SUM(k.biaya)    AS total
            FROM    kunjungan  k
            INNER JOIN diagnosis dx ON k.kode_dx = dx.kode_dx
            GROUP BY dx.kategori
            ORDER BY total DESC
        """)
        rows = cursor.fetchall()
        print("\n  [Per Kategori Diagnosis]")
        formatted = [(r[0], r[1], f"{float(r[2]):,.0f}", f"{float(r[3]):,.0f}")
                     for r in rows]
        print(tabulate(formatted,
                       headers=["Kategori", "Jml", "Rata Biaya", "Total"],
                       tablefmt="simple",
                       colalign=("left", "center", "right", "right")))

        # ── Per kelas ruangan (GROUP BY) ──────────────────────────
        cursor.execute("""
            SELECT  r.kelas,
                    COUNT(*)        AS jml,
                    AVG(k.biaya)    AS rata,
                    SUM(k.biaya)    AS total
            FROM    kunjungan k
            INNER JOIN ruangan r ON k.id_ruangan = r.id_ruangan
            GROUP BY r.kelas
            ORDER BY rata DESC
        """)
        rows = cursor.fetchall()
        print("\n  [Per Kelas Ruangan]")
        formatted = [(r[0], r[1], f"{float(r[2]):,.0f}", f"{float(r[3]):,.0f}")
                     for r in rows]
        print(tabulate(formatted,
                       headers=["Kelas", "Jml", "Rata Biaya", "Total"],
                       tablefmt="simple",
                       colalign=("left", "center", "right", "right")))

        # ── Per spesialisasi dokter (GROUP BY) ────────────────────
        cursor.execute("""
            SELECT  d.spesialisasi,
                    COUNT(*)        AS jml,
                    SUM(k.biaya)    AS pendapatan
            FROM    kunjungan k
            INNER JOIN dokter d ON k.id_dokter = d.id_dokter
            GROUP BY d.spesialisasi
            ORDER BY pendapatan DESC
        """)
        rows = cursor.fetchall()
        print("\n  [Per Spesialisasi Dokter]")
        formatted = [(r[0], r[1], f"{float(r[2]):,.0f}") for r in rows]
        print(tabulate(formatted,
                       headers=["Spesialisasi", "Jml", "Total Pendapatan"],
                       tablefmt="simple",
                       colalign=("left", "center", "right")))

    except mysql.connector.Error as e:
        print(f"[ERROR] Gagal mengambil statistik: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 3 – VISUALISASI DATA
# ══════════════════════════════════════════════════════════════════════════════

def show_visualisasi():
    """Menampilkan 4 grafik berbasis hasil JOIN multi-tabel."""
    print("\n" + "=" * 60)
    print("           DATA VISUALIZATION")
    print("=" * 60)
    print("  Menampilkan grafik, harap tunggu...")

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # ── Pie chart: distribusi kategori diagnosis ──────────────
        cursor.execute("""
            SELECT dx.kategori, COUNT(*)
            FROM   kunjungan k
            INNER JOIN diagnosis dx ON k.kode_dx = dx.kode_dx
            GROUP BY dx.kategori
            ORDER BY dx.kategori
        """)
        kat_data   = cursor.fetchall()
        kat_labels = [r[0] for r in kat_data]
        kat_counts = [r[1] for r in kat_data]

        # ── Pie chart: distribusi kelas ruangan ───────────────────
        cursor.execute("""
            SELECT r.kelas, COUNT(*)
            FROM   kunjungan k
            INNER JOIN ruangan r ON k.id_ruangan = r.id_ruangan
            GROUP BY r.kelas
            ORDER BY r.kelas
        """)
        kls_data   = cursor.fetchall()
        kls_labels = [r[0] for r in kls_data]
        kls_counts = [r[1] for r in kls_data]

        # ── Bar chart: total pendapatan per spesialisasi ──────────
        cursor.execute("""
            SELECT d.spesialisasi, SUM(k.biaya)
            FROM   kunjungan k
            INNER JOIN dokter d ON k.id_dokter = d.id_dokter
            GROUP BY d.spesialisasi
            ORDER BY SUM(k.biaya) DESC
        """)
        sp_data   = cursor.fetchall()
        sp_labels = [r[0] for r in sp_data]
        sp_total  = [float(r[1]) / 1_000_000 for r in sp_data]

        # ── Histogram: biaya kunjungan ────────────────────────────
        cursor.execute("SELECT biaya FROM kunjungan")
        biaya_jt = [float(r[0]) / 1_000_000 for r in cursor.fetchall()]

        # ── Plot ──────────────────────────────────────────────────
        fig, axes = plt.subplots(2, 2, figsize=(13, 9))
        fig.suptitle("Dashboard Data Kunjungan Rumah Sakit",
                     fontsize=15, fontweight="bold", y=1.01)

        colors_kat = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
                      "#59a14f", "#edc949"]
        colors_kls = ["#ff9da7", "#9c755f", "#bab0ac", "#d4a5a5",
                      "#86bcb6", "#a0cbe8"]

        # [0,0] Pie – Kategori Diagnosis
        axes[0, 0].pie(kat_counts, labels=kat_labels,
                       autopct="%1.1f%%", startangle=90,
                       colors=colors_kat)
        axes[0, 0].set_title("Distribusi Kategori Diagnosis")

        # [0,1] Pie – Kelas Ruangan
        axes[0, 1].pie(kls_counts, labels=kls_labels,
                       autopct="%1.1f%%", startangle=90,
                       colors=colors_kls)
        axes[0, 1].set_title("Distribusi Kelas Ruangan")

        # [1,0] Bar – Pendapatan per Spesialisasi
        axes[1, 0].barh(sp_labels, sp_total, color="#4e79a7",
                        edgecolor="white")
        axes[1, 0].set_title("Total Pendapatan per Spesialisasi")
        axes[1, 0].set_xlabel("Pendapatan (juta Rp)")
        axes[1, 0].invert_yaxis()

        # [1,1] Histogram – Biaya
        axes[1, 1].hist(biaya_jt, bins=8, color="#f28e2b",
                        edgecolor="white")
        axes[1, 1].set_title("Distribusi Biaya Kunjungan")
        axes[1, 1].set_xlabel("Biaya (juta Rp)")
        axes[1, 1].set_ylabel("Jumlah Kunjungan")
        rata = sum(biaya_jt) / len(biaya_jt)
        axes[1, 1].axvline(rata, color="red", linestyle="--",
                           label=f"Mean: {rata:.2f}jt")
        axes[1, 1].legend()

        plt.tight_layout()
        plt.show()
        print("  Grafik berhasil ditampilkan.")

    except mysql.connector.Error as e:
        print(f"[ERROR] Gagal mengambil data: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 4 – TAMBAH KUNJUNGAN BARU
# ══════════════════════════════════════════════════════════════════════════════

STATUS_RAWAT_VALID = ["Rawat Inap", "Rawat Jalan", "IGD"]
JENIS_KELAMIN_VALID = ["L", "P"]


def _input_tidak_kosong(prompt):
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("  [!] Input tidak boleh kosong. Coba lagi.")


def _input_integer(prompt, minimum=0, maksimum=None):
    while True:
        try:
            nilai = int(input(prompt).strip())
            if nilai < minimum:
                print(f"  [!] Nilai minimal {minimum}. Coba lagi.")
            elif maksimum and nilai > maksimum:
                print(f"  [!] Nilai maksimal {maksimum}. Coba lagi.")
            else:
                return nilai
        except ValueError:
            print("  [!] Masukkan angka bulat yang valid. Coba lagi.")


def _input_float(prompt, minimum=0):
    while True:
        try:
            nilai = float(input(prompt).strip())
            if nilai < minimum:
                print(f"  [!] Nilai minimal {minimum}. Coba lagi.")
            else:
                return nilai
        except ValueError:
            print("  [!] Masukkan angka yang valid. Coba lagi.")


def _input_tanggal(prompt, default_hari_ini=False, boleh_kosong=False):
    """Input tanggal dengan format YYYY-MM-DD."""
    while True:
        nilai = input(prompt).strip()
        if not nilai:
            if default_hari_ini:
                return date.today()
            if boleh_kosong:
                return None
            print("  [!] Tanggal tidak boleh kosong. Coba lagi.")
            continue
        try:
            return datetime.strptime(nilai, "%Y-%m-%d").date()
        except ValueError:
            print("  [!] Format salah. Gunakan YYYY-MM-DD. Coba lagi.")


def _pilih_dari_list(prompt, opsi):
    for i, item in enumerate(opsi, 1):
        print(f"  {i}. {item}")
    while True:
        try:
            pilihan = int(input(prompt).strip())
            if 1 <= pilihan <= len(opsi):
                return opsi[pilihan - 1]
            print(f"  [!] Pilih angka 1–{len(opsi)}. Coba lagi.")
        except ValueError:
            print("  [!] Masukkan angka. Coba lagi.")


def _pilih_dari_db(cursor, prompt, query, header):
    """Tampilkan baris hasil query, lalu minta user memilih lewat nomor.
    Mengembalikan tuple baris yang dipilih (kolom pertama biasanya ID)."""
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"\n  {header}")
    for i, row in enumerate(rows, 1):
        deskripsi = " | ".join(str(x) for x in row[1:])
        print(f"  {i:2d}. [{row[0]}] {deskripsi}")
    while True:
        try:
            pilihan = int(input(prompt).strip())
            if 1 <= pilihan <= len(rows):
                return rows[pilihan - 1]
            print(f"  [!] Pilih angka 1–{len(rows)}. Coba lagi.")
        except ValueError:
            print("  [!] Masukkan angka. Coba lagi.")


def _generate_id(cursor, tabel, kolom, prefix, lebar=3):
    """Generate ID berikutnya berdasar nilai terbesar di tabel."""
    cursor.execute(f"SELECT {kolom} FROM {tabel} ORDER BY {kolom} DESC LIMIT 1")
    row = cursor.fetchone()
    nomor = int(row[0][len(prefix):]) + 1 if row else 1
    return f"{prefix}{nomor:0{lebar}d}"


def _tambah_pasien_baru(cursor):
    """Buat pasien baru, return id_pasien-nya."""
    id_pasien = _generate_id(cursor, "pasien", "id_pasien", "P")
    print(f"\n  ID Pasien baru : {id_pasien}")
    nama  = _input_tidak_kosong("  Nama Pasien   : ")
    usia  = _input_integer("  Usia (tahun)  : ", minimum=0, maksimum=150)
    print("  Jenis Kelamin (L/P):")
    jk    = _pilih_dari_list("  Pilih nomor   : ", JENIS_KELAMIN_VALID)
    alamat = input("  Alamat        : ").strip() or None
    telp   = input("  No. Telp      : ").strip() or None
    cursor.execute("""
        INSERT INTO pasien VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_pasien, nama, usia, jk, alamat, telp))
    return id_pasien


def add_kunjungan():
    """Menambahkan kunjungan baru. Bisa memilih pasien yang sudah ada
    atau membuat pasien baru sekaligus."""
    print("\n" + "=" * 60)
    print("           TAMBAH KUNJUNGAN BARU")
    print("=" * 60)

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # 1. Pilih atau buat pasien
        print("\n  Pasien existing atau pasien baru?")
        pilihan = _pilih_dari_list("  Pilih nomor   : ",
                                   ["Pasien sudah ada", "Pasien baru"])
        if pilihan == "Pasien sudah ada":
            pasien = _pilih_dari_db(
                cursor,
                "  Pilih pasien  : ",
                "SELECT id_pasien, nama_pasien, usia, jenis_kelamin "
                "FROM pasien ORDER BY id_pasien",
                "Daftar Pasien:"
            )
            id_pasien   = pasien[0]
            nama_pasien = pasien[1]
        else:
            id_pasien   = _tambah_pasien_baru(cursor)
            cursor.execute("SELECT nama_pasien FROM pasien WHERE id_pasien=%s",
                           (id_pasien,))
            nama_pasien = cursor.fetchone()[0]

        # 2. Pilih dokter
        dokter = _pilih_dari_db(
            cursor,
            "  Pilih dokter  : ",
            "SELECT id_dokter, nama_dokter, spesialisasi "
            "FROM dokter ORDER BY spesialisasi, nama_dokter",
            "Daftar Dokter:"
        )

        # 3. Pilih ruangan
        ruangan = _pilih_dari_db(
            cursor,
            "  Pilih ruangan : ",
            "SELECT id_ruangan, nama_ruangan, kelas, tarif_per_hari "
            "FROM ruangan ORDER BY tarif_per_hari DESC",
            "Daftar Ruangan:"
        )

        # 4. Pilih diagnosis
        dx = _pilih_dari_db(
            cursor,
            "  Pilih diag.   : ",
            "SELECT kode_dx, nama_diagnosis, kategori "
            "FROM diagnosis ORDER BY kategori, nama_diagnosis",
            "Daftar Diagnosis:"
        )

        # 5. Tanggal
        print("\n  (Tekan Enter untuk hari ini)")
        tgl_masuk  = _input_tanggal("  Tgl masuk (YYYY-MM-DD): ",
                                    default_hari_ini=True)
        print("  (Tekan Enter jika belum keluar)")
        tgl_keluar = _input_tanggal("  Tgl keluar (YYYY-MM-DD): ",
                                    boleh_kosong=True)

        # 6. Status rawat
        print("\n  Status Rawat:")
        status = _pilih_dari_list("  Pilih nomor   : ", STATUS_RAWAT_VALID)

        # 7. Biaya
        biaya = _input_float("\n  Biaya (Rp)    : ", minimum=0)

        # 8. Generate id_kunjungan
        id_kunjungan = _generate_id(cursor, "kunjungan", "id_kunjungan", "K")

        # 9. Konfirmasi
        print("\n  ── Konfirmasi Kunjungan ─────────────────────")
        print(f"  ID Kunjungan : {id_kunjungan}")
        print(f"  Pasien       : [{id_pasien}] {nama_pasien}")
        print(f"  Dokter       : [{dokter[0]}] {dokter[1]} ({dokter[2]})")
        print(f"  Ruangan      : [{ruangan[0]}] {ruangan[1]} ({ruangan[2]})")
        print(f"  Diagnosis    : [{dx[0]}] {dx[1]} ({dx[2]})")
        print(f"  Tgl Masuk    : {tgl_masuk}")
        print(f"  Tgl Keluar   : {tgl_keluar or '-'}")
        print(f"  Status Rawat : {status}")
        print(f"  Biaya        : Rp {biaya:,.2f}")
        print("  ─────────────────────────────────────────────")

        konfirmasi = input("  Simpan kunjungan? (y/n): ").strip().lower()
        if konfirmasi != "y":
            conn.rollback()
            print("  [INFO] Penambahan kunjungan dibatalkan.")
            return

        cursor.execute("""
            INSERT INTO kunjungan VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_kunjungan, id_pasien, dokter[0], ruangan[0], dx[0],
              tgl_masuk, tgl_keluar, status, biaya))
        conn.commit()
        print(f"  [OK] Kunjungan {id_kunjungan} berhasil ditambahkan!")

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"  [ERROR] Gagal menyimpan data: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 5 – LAPORAN PER DOKTER (JOIN + GROUP BY + HAVING + ORDER BY)
# ══════════════════════════════════════════════════════════════════════════════

def laporan_dokter():
    """Menampilkan laporan pendapatan per dokter, hanya dokter yang
    menangani ≥ N kunjungan (HAVING)."""
    print("\n" + "=" * 70)
    print("           LAPORAN PRODUKTIVITAS DOKTER")
    print("=" * 70)

    minimal = _input_integer("  Tampilkan dokter dengan minimal berapa "
                             "kunjungan? (default 3): ", minimum=1) \
              if input("  Atur ambang batas? (y/n, default n): ") \
                  .strip().lower() == "y" else 3
    print(f"\n  Menampilkan dokter dengan ≥ {minimal} kunjungan...\n")

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT  d.id_dokter,
                    d.nama_dokter,
                    d.spesialisasi,
                    COUNT(*)      AS jml,
                    SUM(k.biaya)  AS pendapatan,
                    AVG(k.biaya)  AS rata,
                    MIN(k.biaya)  AS min_biaya,
                    MAX(k.biaya)  AS max_biaya
            FROM    kunjungan k
            INNER JOIN dokter d ON k.id_dokter = d.id_dokter
            GROUP BY d.id_dokter, d.nama_dokter, d.spesialisasi
            HAVING COUNT(*) >= %s
            ORDER BY pendapatan DESC
        """, (minimal,))
        rows = cursor.fetchall()

        if not rows:
            print(f"  Tidak ada dokter dengan ≥ {minimal} kunjungan.")
            return

        headers = ["ID", "Dokter", "Spesialisasi", "Jml",
                   "Total Pendapatan", "Rata-rata", "Min", "Max"]
        formatted = [
            (r[0], r[1], r[2], r[3],
             f"{float(r[4]):,.0f}", f"{float(r[5]):,.0f}",
             f"{float(r[6]):,.0f}", f"{float(r[7]):,.0f}")
            for r in rows
        ]
        print(tabulate(formatted, headers=headers, tablefmt="grid",
                       colalign=("left", "left", "left", "center",
                                 "right", "right", "right", "right")))

    except mysql.connector.Error as e:
        print(f"[ERROR] Gagal mengambil laporan: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 6 – PASIEN BIAYA DI ATAS RATA-RATA (Subquery)
# ══════════════════════════════════════════════════════════════════════════════

def pasien_biaya_tinggi():
    """Menampilkan kunjungan dengan biaya melebihi rata-rata seluruh
    kunjungan, menggunakan subquery."""
    print("\n" + "=" * 80)
    print("           KUNJUNGAN DENGAN BIAYA DI ATAS RATA-RATA")
    print("=" * 80)

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # Ambil rata-rata dulu untuk ditampilkan
        cursor.execute("SELECT AVG(biaya) FROM kunjungan")
        rata = float(cursor.fetchone()[0])
        print(f"\n  Rata-rata biaya seluruh kunjungan: Rp {rata:,.2f}\n")

        cursor.execute("""
            SELECT  k.id_kunjungan,
                    p.nama_pasien,
                    p.usia,
                    d.nama_dokter,
                    dx.nama_diagnosis,
                    r.kelas,
                    k.status_rawat,
                    k.biaya
            FROM    kunjungan k
            INNER JOIN pasien    p  ON k.id_pasien  = p.id_pasien
            INNER JOIN dokter    d  ON k.id_dokter  = d.id_dokter
            INNER JOIN diagnosis dx ON k.kode_dx    = dx.kode_dx
            INNER JOIN ruangan   r  ON k.id_ruangan = r.id_ruangan
            WHERE   k.biaya > (SELECT AVG(biaya) FROM kunjungan)
            ORDER BY k.biaya DESC
        """)
        rows = cursor.fetchall()

        if not rows:
            print("  Tidak ada kunjungan dengan biaya di atas rata-rata.")
            return

        headers = ["ID", "Pasien", "Usia", "Dokter", "Diagnosis",
                   "Kelas", "Status", "Biaya (Rp)"]
        formatted = [
            (r[0], r[1], r[2], r[3], r[4], r[5], r[6], f"{float(r[7]):,.0f}")
            for r in rows
        ]
        print(tabulate(formatted, headers=headers, tablefmt="grid"))
        print(f"\n  Total: {len(rows)} kunjungan di atas rata-rata.")

    except mysql.connector.Error as e:
        print(f"[ERROR] Gagal mengambil data: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR 7 – MASTER DATA UNIK (DISTINCT)
# ══════════════════════════════════════════════════════════════════════════════

def lihat_master():
    """Menampilkan nilai-nilai unik (DISTINCT) dari tiap master."""
    print("\n" + "=" * 60)
    print("           MASTER DATA – NILAI UNIK (DISTINCT)")
    print("=" * 60)

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT spesialisasi FROM dokter "
                       "ORDER BY spesialisasi")
        print("\n  [Spesialisasi Dokter]")
        for r in cursor.fetchall():
            print(f"    • {r[0]}")

        cursor.execute("SELECT DISTINCT kategori FROM diagnosis "
                       "ORDER BY kategori")
        print("\n  [Kategori Diagnosis]")
        for r in cursor.fetchall():
            print(f"    • {r[0]}")

        cursor.execute("SELECT DISTINCT kelas FROM ruangan "
                       "ORDER BY kelas")
        print("\n  [Kelas Ruangan]")
        for r in cursor.fetchall():
            print(f"    • {r[0]}")

        cursor.execute("SELECT DISTINCT status_rawat FROM kunjungan "
                       "ORDER BY status_rawat")
        print("\n  [Status Rawat (yang pernah dicatat)]")
        for r in cursor.fetchall():
            print(f"    • {r[0]}")

    except mysql.connector.Error as e:
        print(f"[ERROR] Gagal mengambil master data: {e}")
    finally:
        cursor.close()
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════════════════════════════

def tampil_menu():
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║      SISTEM INFORMASI PASIEN RUMAH SAKIT       ║")
    print("╠" + "═" * 48 + "╣")
    print("║  1. Lihat Data Kunjungan (JOIN 5 tabel)        ║")
    print("║  2. Statistik & GROUP BY                       ║")
    print("║  3. Visualisasi Data                           ║")
    print("║  4. Tambah Kunjungan Baru                      ║")
    print("║  5. Laporan Dokter (HAVING)                    ║")
    print("║  6. Kunjungan di Atas Rata-rata (Subquery)     ║")
    print("║  7. Master Data Unik (DISTINCT)                ║")
    print("║  0. Keluar                                     ║")
    print("╚" + "═" * 48 + "╝")


def main():
    print("\n  Selamat datang di Sistem Informasi Pasien Rumah Sakit!")

    try:
        conn = get_connection()
        conn.close()
        print("  Koneksi database berhasil.")
    except mysql.connector.Error as e:
        print(f"\n  [ERROR] Tidak dapat terhubung ke database: {e}")
        print("  Pastikan MySQL aktif dan konfigurasi DB_CONFIG sudah benar.")
        return

    while True:
        tampil_menu()
        pilihan = input("  Pilih menu (0-7): ").strip()

        if pilihan == "1":
            lihat_kunjungan()
        elif pilihan == "2":
            show_statistik()
        elif pilihan == "3":
            show_visualisasi()
        elif pilihan == "4":
            add_kunjungan()
        elif pilihan == "5":
            laporan_dokter()
        elif pilihan == "6":
            pasien_biaya_tinggi()
        elif pilihan == "7":
            lihat_master()
        elif pilihan == "0":
            print("\n  Terima kasih. Sampai jumpa!\n")
            break
        else:
            print("  [!] Pilihan tidak valid. Masukkan angka 0–7.")


if __name__ == "__main__":
    main()
