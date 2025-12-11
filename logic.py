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

        nama = nama.strip()
        
        if nama=="":
            messagebox.showwarning("Peringatan", "Nama akun tidak boleh kosong!")
            return
        
        keylist=list(akun.keys())
        for i in range (len(keylist)):
            if nama==keylist[i]:
                messagebox.showwarning("Gagal", "Akun sudah ada.")
                return

        akun[nama] = []
        messagebox.showinfo("Berhasil", f"Akun '{nama}' berhasil ditambahkan.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")


# EDIT AKUN
def edit_akun():
    try:
       keylist=list(akun.keys())
        if len(keylist)==0:
            messagebox.showwarning("Peringatan", "Belum ada akun yang bisa diedit.")
            return
        
        pilih = simpledialog.askstring(
            "Edit Akun",
            f"Daftar akun:\n{', '.join(akun.keys())}\n\nMasukkan nama akun yang ingin diedit:"
        )
        
        pilih = pilih.strip()

        keylist=list(akun.keys())
        for i in range (len(keylist)):
            if pilih==keylist[i]:
                nama_baru = simpledialog.askstring("Edit Akun", "Masukkan nama baru:")
                nama_baru = nama_baru.strip()
                if nama_baru=="":
                    messagebox.showwarning("Peringatan", "Nama akun tidak boleh kosong!")
                    return
                else:
                    akun[nama_baru] = akun.pop(pilih)
                messagebox.showinfo("Berhasil", f"Akun '{pilih}' berhasil diubah menjadi '{nama_baru}'.")
                return
            else:
                messagebox.showwarning("Gagal", "Akun tidak ditemukan.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")


# TAMBAH TRANSAKSI PEMASUKAN / PENGELUARAN
def tambah_transaksi():
    try:
        if not akun:
            messagebox.showwarning("Peringatan", "Belum ada akun! Silakan tambah akun terlebih dahulu.")
            return

        pilih = simpledialog.askstring(
            "Tambah Transaksi",
            f"Daftar akun:\n{', '.join(akun.keys())}\n\nMasukkan nama akun:"
        )

        if not pilih:
            return
            
        pilih = pilih.strip()

        if not pilih or pilih not in akun:
            messagebox.showwarning("Gagal", "Akun tidak ditemukan!")
            return

        jenis = simpledialog.askstring(
            "Jenis Transaksi",
            "Masukkan jenis transaksi (income/expense):"
        )

        if not jenis:
            return 
            
        jenis = jenis.strip().lower()

        if jenis not in ["income", "expense"]:
            messagebox.showwarning("Gagal", "Jenis transaksi hanya 'income' atau 'expense'!")
            return

        if jenis == "income":
            prompt = "Masukkan kategori untuk transaksi income:\nMisalnya: Gaji, Proyek, Uang Bulanan"
        else:
            prompt = "Masukkan kategori untuk transaksi expense:\nMisalnya: Makanan, Tagihan, Entertainment"
        
        kategori = simpledialog.askstring("Kategori Transaksi", prompt)

        if not kategori:
            return 
            
        kategori = kategori.strip().lower()

        if not kategori:
            messagebox.showwarning("Gagal", "Kategori tidak boleh kosong!")
            return

        jumlah_str = simpledialog.askstring("Jumlah Uang", "Masukkan jumlah (angka):")
        if not jumlah_str:
            return  
            
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


# PIE CHART INCOME
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


# PIE CHART EXPENSE
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
        matikan = messagebox.askyesno("Status Reminder", "Pengingat tabungan sudah berjalan. Apakah anda ingin mematikannya?")

        if matikan:
            saving_reminder_active = False
            messagebox.showinfo("Info", "Reminder berhasil dimatikan.")

            return
        
    nominal = int(simpledialog.askstring("Nominal","Masukan nominal yang ingin ditabung: "))
    interval_hari = int(simpledialog.askstring("Waktu Menabung","Masukkan frekuensi menabung (dalam hari): "))


    saving_reminder_active = True
    
    messagebox.showinfo("Aktif", f"Reminder aktif! Anda akan diingatkan menabung Rp {nominal:,} secara berkala.")

    loop_reminder(window_utama, nominal, interval_hari)


def loop_reminder(window_utama, nominal, interval_hari):
    global saving_reminder_active
    
    if not saving_reminder_active:
        return

    ms = interval_hari * 24 * 60 * 60 * 1000

    window_utama.after(ms, lambda: show_popup(window_utama, nominal, interval_hari))

    
#Memunculkan pesan reminder
def show_popup(window_target, nominal, interval_hari):
    
    messagebox.showinfo(
        "Reminder Tabungan", 
        f"Jangan lupa sisihkan Rp {nominal:,} untuk tabungan hari ini!"
    )
    
   
    loop_reminder(window_target, nominal, interval_hari)


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
