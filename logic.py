import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

akun = {} 
current_plan_template = None
plan_limits = {}
saving_reminder_active = False
saving_interval_days = 0
saving_amount = 0
saving_time = ""

# TAMBAH AKUN
def tambah_akun():
    try:
        nama = simpledialog.askstring("Tambah Akun", "Masukkan nama akun/dompet:")
        if not nama:
            return  # User cancelled

        # Remove extra whitespace
        nama = nama.strip()
        
        if not nama:
            messagebox.showwarning("Peringatan", "Nama akun tidak boleh kosong!")
            return

        if nama in akun:
            messagebox.showwarning("Gagal", "Akun sudah ada.")
            return

        akun[nama] = []
        messagebox.showinfo("Berhasil", f"Akun '{nama}' berhasil ditambahkan.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# EDIT AKUN
def edit_akun():
    try:
        if not akun:
            messagebox.showwarning("Peringatan", "Belum ada akun yang bisa diedit.")
            return
        
        # pilih akun
        pilih = simpledialog.askstring(
            "Edit Akun",
            f"Daftar akun:\n{', '.join(akun.keys())}\n\nMasukkan nama akun yang ingin diedit:"
        )
        
        if not pilih:
            return  # User cancelled
            
        pilih = pilih.strip()
        
        if not pilih or pilih not in akun:
            messagebox.showwarning("Gagal", "Akun tidak ditemukan.")
            return

        # input nama baru
        nama_baru = simpledialog.askstring("Edit Akun", "Masukkan nama baru:")
        if not nama_baru:
            return  # User cancelled
            
        nama_baru = nama_baru.strip()
        
        if not nama_baru:
            messagebox.showwarning("Peringatan", "Nama akun tidak boleh kosong!")
            return

        if nama_baru in akun:
            messagebox.showwarning("Gagal", "Nama baru sudah digunakan.")
            return

        # ganti nama akun
        akun[nama_baru] = akun.pop(pilih)
        messagebox.showinfo("Berhasil", f"Akun '{pilih}' berhasil diubah menjadi '{nama_baru}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# TAMBAH PEMASUKAN / PENGELUARAN
def tambah_transaksi():
    try:
        if not akun:
            messagebox.showwarning("Peringatan", "Belum ada akun! Silakan tambah akun terlebih dahulu.")
            return

        # pilih akun
        pilih = simpledialog.askstring(
            "Tambah Transaksi",
            f"Daftar akun:\n{', '.join(akun.keys())}\n\nMasukkan nama akun:"
        )

        if not pilih:
            return  # User cancelled
            
        pilih = pilih.strip()

        if not pilih or pilih not in akun:
            messagebox.showwarning("Gagal", "Akun tidak ditemukan!")
            return

        # pilih jenis transaksi
        jenis = simpledialog.askstring(
            "Jenis Transaksi",
            "Masukkan jenis transaksi (income/expense):"
        )

        if not jenis:
            return  # User cancelled
            
        jenis = jenis.strip().lower()

        if jenis not in ["income", "expense"]:
            messagebox.showwarning("Gagal", "Jenis transaksi hanya 'income' atau 'expense'!")
            return

        # pilih kategori
        if jenis == "income":
            prompt = "Masukkan kategori untuk transaksi income:\nMisalnya: Gaji, Proyek, Uang Bulanan"
        else:
            prompt = "Masukkan kategori untuk transaksi expense:\nMisalnya: Makanan, Tagihan, Entertainment"
        
        kategori = simpledialog.askstring("Kategori Transaksi", prompt)

        if not kategori:
            return  # User cancelled
            
        kategori = kategori.strip().lower()

        if not kategori:
            messagebox.showwarning("Gagal", "Kategori tidak boleh kosong!")
            return

        # input jumlah uang
        jumlah_str = simpledialog.askstring("Jumlah Uang", "Masukkan jumlah (angka):")
        if not jumlah_str:
            return  # User cancelled
            
        try:
            jumlah = int(jumlah_str.strip())
            if jumlah <= 0:
                messagebox.showwarning("Gagal", "Jumlah harus lebih dari 0!")
                return
        except ValueError:
            messagebox.showwarning("Gagal", "Jumlah harus berupa angka!")
            return
        
        #TERAPKAN TEMPLATE FINANSIAL JIKA INCOME
        if (current_plan_template == "50-30-20") and (jenis == "income"):
            apply_503020()
        elif  (current_plan_template == "PYF") and (jenis == "income"):
            apply_PYF()
            

        # PLAN LIMIT CHECKING
        bagian = None
        if current_plan_template and jenis == "expense":
            if kategori in ["makanan", "tagihan"]:
                bagian = "needs"
            elif kategori in ["entertainment"]:
                bagian = "wants"
            
            if bagian:
                total = sum(t["jumlah"] for t in akun[pilih]
                            if t["jenis"] == "expense" and t["kategori"] == kategori)

                if total + jumlah > plan_limits[bagian]:
                    messagebox.showwarning(
                        "Limit Exceeded",
                        f"Pengeluaran kategori '{kategori}' sudah melebihi batas template {bagian}."
                    )
                    return
        

        akun[pilih].append({"jenis": jenis, "kategori": kategori, "jumlah": jumlah})
        messagebox.showinfo("Sukses", f"Transaksi {jenis} '{kategori}' sebesar Rp {jumlah:,} berhasil ditambahkan ke akun '{pilih}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# POP-UP OUTPUT: Tampilkan akun dan transaksi
def tampilkan_data():
    try:
        if not akun:
            messagebox.showinfo("Data", "Belum ada akun.")
            return

        output = "=== DATA KEUANGAN ===\n"

        for nama, trans in akun.items():
            output += f"\n{'='*40}\n"
            output += f"Akun: {nama}\n"
            output += f"{'='*40}\n"
            
            if not trans:
                output += "  (Belum ada transaksi)\n"
            else:
                total_balance = 0
            
                for t in trans:
                    if t["jenis"].lower() == "expense":
                        jumlah_str = f"-Rp {t['jumlah']:,}"
                        total_balance -= t["jumlah"]
                    else:
                        jumlah_str = f"+Rp {t['jumlah']:,}"
                        total_balance += t["jumlah"]
                    output += f"  {t['jenis'].capitalize():10} | {t['kategori']:20} | {jumlah_str}\n"
                
                output += f"\n  Total Balance Akun '{nama}': Rp {total_balance:,}\n"

        output += f"\n{'='*40}\n"
        output += f"TOTAL SEMUA AKUN: Rp {total_balance():,}\n"
        output += f"{'='*40}\n"

        messagebox.showinfo("Data Keuangan", output)
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

#Grafik Income Summary
def pie_income():
    try:
        if not akun:
            messagebox.showwarning("Peringatan", "Belum ada akun.")
            return

        pilih = simpledialog.askstring(
            "Pilih Akun",
            f"Daftar akun:\n{', '.join(akun.keys())}\n\nMasukkan nama akun:"
        )

        if not pilih:
            return  # User cancelled
            
        pilih = pilih.strip()

        if not pilih or pilih not in akun:
            messagebox.showwarning("Gagal", "Akun tidak ditemukan.")
            return

        data = {}

        for t in akun[pilih]:
            if t["jenis"] == "income":
                if t["kategori"] in data:
                    data[t["kategori"]] += t["jumlah"]
                else:
                    data[t["kategori"]] = t["jumlah"]

        if not data:
            messagebox.showinfo("Info", "Belum ada data income di akun ini.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))
        colors = plt.cm.Greens(range(100, 255, int(155/len(data))))
        wedges, texts, autotexts = ax.pie(data.values(), labels=data.keys(), 
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90)
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        ax.set_title(f"Income Distribution - {pilih}", fontsize=14, fontweight='bold', pad=20)

        # Close button
        exit_ax = plt.axes([0.01, 0.92, 0.06, 0.06]) 
        btn_exit = Button(exit_ax, 'X', color='lightcoral')

        def close_chart(event):
            plt.close(fig)

        btn_exit.on_clicked(close_chart)

        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Grafik Expense Summary
def pie_expense():
    try:
        if not akun:
            messagebox.showwarning("Peringatan", "Belum ada akun.")
            return

        pilih = simpledialog.askstring(
            "Pilih Akun",
            f"Daftar akun:\n{', '.join(akun.keys())}\n\nMasukkan nama akun:"
        )

        if not pilih:
            return  # User cancelled
            
        pilih = pilih.strip()

        if not pilih or pilih not in akun:
            messagebox.showwarning("Gagal", "Akun tidak ditemukan.")
            return

        data = {}

        for t in akun[pilih]:
            if t["jenis"] == "expense":
                if t["kategori"] in data:
                    data[t["kategori"]] += t["jumlah"]
                else:
                    data[t["kategori"]] = t["jumlah"]

        if not data:
            messagebox.showinfo("Info", "Belum ada data expense di akun ini.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))
        colors = plt.cm.Reds(range(100, 255, int(155/len(data))))
        wedges, texts, autotexts = ax.pie(data.values(), labels=data.keys(), 
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90)
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        ax.set_title(f"Expense Distribution - {pilih}", fontsize=14, fontweight='bold', pad=20)

        # Close button
        exit_ax = plt.axes([0.01, 0.92, 0.06, 0.06]) 
        btn_exit = Button(exit_ax, 'X', color='lightcoral')

        def close_chart(event):
            plt.close(fig)

        btn_exit.on_clicked(close_chart)

        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# TOTAL INCOME (SEMUA AKUN)
def total_income():
    try:
        total = 0
        for trans in akun.values():
            for t in trans:
                if t["jenis"] == "income":
                    total += t["jumlah"]
        return total
    except Exception:
        return 0

# TOTAL EXPENSE (SEMUA AKUN)
def total_expense():
    try:
        total = 0
        for trans in akun.values():
            for t in trans:
                if t["jenis"] == "expense":
                    total += t["jumlah"]
        return total
    except Exception:
        return 0

# TOTAL BALANCE (INCOME - EXPENSE)
def total_balance():
    try:
        return total_income() - total_expense()
    except Exception:
        return 0

# BALANCE PER AKUN (BARU)
def account_balance(account_name):
    """Menghitung balance untuk akun tertentu"""
    try:
        if account_name not in akun:
            return 0
        
        balance = 0
        for t in akun[account_name]:
            if t["jenis"] == "income":
                balance += t["jumlah"]
            else:  # expense
                balance -= t["jumlah"]
        return balance
    except Exception:
        return 0

# INCOME PER AKUN (BARU)
def account_income(account_name):
    """Menghitung total income untuk akun tertentu"""
    try:
        if account_name not in akun:
            return 0
        
        total = 0
        for t in akun[account_name]:
            if t["jenis"] == "income":
                total += t["jumlah"]
        return total
    except Exception:
        return 0

# EXPENSE PER AKUN (BARU)
def account_expense(account_name):
    """Menghitung total expense untuk akun tertentu"""
    try:
        if account_name not in akun:
            return 0
        
        total = 0
        for t in akun[account_name]:
            if t["jenis"] == "expense":
                total += t["jumlah"]
        return total
    except Exception:
        return 0
    
#Hitung inflasi
def hitung_inflasi():
    
    nilai_masa_depan = 0
    nilai_awal = 0

    jenis_inflasi = simpledialog.askstring(
            "Jenis Inflasi",
            f"Nilai input sendiri atau balance? (sendiri/balance)"
        )
    
    if not jenis_inflasi:
        return  # User cancelled
    
    jenis_inflasi.strip().lower()

    if jenis_inflasi == "sendiri":
        nilai_awal = float(simpledialog.askstring("Hitung Inflasi", "Masukkan nilai uang saat ini:"))
    elif jenis_inflasi == "balance":
        nilai_awal = total_balance()

    try:
        inflasi = float(simpledialog.askstring("Inflasi", "Masukkan inflasi per tahun (%):"))
        tahun = int(simpledialog.askstring("Tahun", "Masukkan jumlah tahun yang akan datang:"))
    except:
        messagebox.showwarning("Error", "Input tidak valid!")
        return
        
    #RUMUS INFLASI
    nilai_masa_depan = nilai_awal / ((1 + inflasi/100) ** tahun)

    messagebox.showinfo(
        "Hasil Inflasi",
        f"Nilai uang Rp{nilai_awal:,.0f} \n"
        f"dengan inflasi {inflasi}% selama {tahun} tahun\n\n"
        f"Nilainya menjadi ≈ Rp{nilai_masa_depan:,.0f}"
    )


#Reminder pengingat menabung
def start_saving_reminder(window_utama):
    global saving_reminder_active

    if saving_reminder_active:
        messagebox.showinfo("Info", "Pengingat tabungan sudah berjalan.")
        return

    # --- SETTING (UBAH ANGKA DI SINI) ---
    nominal = 50000          # Nominal yang diingatkan
    interval_detik = 10      # Muncul setiap 10 detik (Ganti jadi 86400 untuk 1 hari)
    # ------------------------------------

    # Ubah status jadi aktif
    saving_reminder_active = True
    
    # Beri info awal bahwa reminder dimulai
    messagebox.showinfo("Aktif", f"Reminder aktif! Anda akan diingatkan menabung Rp {nominal:,} secara berkala.")

    # Mulai hitungan mundur
    loop_reminder(window_utama, nominal, interval_detik)


def loop_reminder(window_utama, nominal, interval_detik):
    global saving_reminder_active
    
    # Jika tombol dimatikan (opsional), berhenti
    if not saving_reminder_active:
        return

    # Hitung milidetik
    ms = interval_detik * 1000

    # Jadwalkan fungsi pop-up
    window_utama.after(ms, lambda: show_popup(window_utama, nominal, interval_detik))

#Memunculkan pesan reminder
def show_popup(window_target, nominal, interval_detik):
    
    messagebox.showinfo(
        "Reminder Tabungan", 
        f"Jangan lupa sisihkan Rp {nominal:,} untuk tabungan hari ini!"
    )
    
   
    loop_reminder(window_target, nominal, interval_detik)


def apply_503020():
    global current_plan_template, plan_limits

    current_plan_template = "50-30-20"
    plan_limits = {"needs": 0, "wants": 0, "savings": 0}
    
    balance = total_balance()

    if balance <= 0:
        messagebox.showinfo("Info", "Saldo masih kosong, template akan diterapkan ketika ada income.")
        return

    plan_limits["needs"] += balance * 0.50
    plan_limits["wants"] += balance * 0.30
    plan_limits["savings"] += balance * 0.20

    messagebox.showinfo(
        "Template Applied",
        f"Template 50-30-20 berhasil diterapkan.\n\n"
        f"Needs: Rp {int(plan_limits['needs']):,}\n"
        f"Wants: Rp {int(plan_limits['wants']):,}\n"
        f"Savings: Rp {int(plan_limits['savings']):,}"
    )

#Template Finansial pay yourself first
def apply_PYF():
    global current_plan_template, plan_limits

    current_plan_template = "PYF"
    plan_limits = {"needs": 0, "wants": 0, "savings": 0}

    balance = total_balance()

    if balance <= 0:
        messagebox.showinfo("Info", "Saldo masih kosong, template akan diterapkan ketika ada income.")
        return

    plan_limits["savings"] += balance * 0.30
    sisa = balance - plan_limits["savings"]
    plan_limits["needs"] += sisa * 0.70
    plan_limits["wants"] += sisa * 0.30

    messagebox.showinfo(
        "Template Applied",
        f"Template Pay your self first berhasil diterapkan.\n\n"
        f"Needs: Rp {int(plan_limits['needs']):,}\n"
        f"Wants: Rp {int(plan_limits['wants']):,}\n"
        f"Savings: Rp {int(plan_limits['savings']):,}"
    )


 
