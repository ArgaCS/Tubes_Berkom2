
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import logic

# WINDOW UTAMA
root = tk.Tk()
root.geometry("1100x600")
root.configure(bg="white")
root.title("Cash Flow")

# Make the window responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# SPACE KOSONG DI KIRI
space_left = tk.Frame(root, width=50, height=50, bg="white")
space_left.grid(row=0, column=0, sticky="ns")

# FRAME UTAMA
main_page = tk.Frame(root, bg="#E4E4E4", width=870, height=600)
main_page.grid(row=0, column=2, padx=15, pady=20, sticky="nsew")
main_page.grid_rowconfigure(4, weight=1)
main_page.grid_columnconfigure(0, weight=1)
main_page.grid_columnconfigure(1, weight=1)
main_page.grid_columnconfigure(2, weight=1)

current_account = tk.StringVar()

# FUNGSI PINDAH PAGE
def clear_main_page():
    for widget in main_page.winfo_children():
        widget.destroy()

# FUNGSI REFRESH DATA
def refresh_transaction_page():
    page_transaksi()

# TRANSACTION PAGE 
def page_transaksi():
    clear_main_page()
    
    # TAMBAH AKUN
    button_addAccount = tk.Button(main_page, text="+ Add Account", bg="white", 
                                   command=lambda: [logic.tambah_akun(), refresh_transaction_page()])
    button_addAccount.grid(row=1, column=0, padx=10, pady=20, sticky="w")


    # TAMBAH TRANSAKSI
    button_addTransaction = tk.Button(main_page, text="Add Transaction", width=15, 
                                      command=lambda: [logic.tambah_transaksi(), refresh_transaction_page()])
    button_addTransaction.grid(row=1, column=1, padx=10, pady=20, sticky="w")

    # EDIT AKUN BUTTON
    button_editAccount = tk.Button(main_page, text="Edit Account", width=12, bg="#FFE4B5",
                                   command=lambda: [logic.edit_akun(), refresh_transaction_page()])
    button_editAccount.grid(row=1, column=2, padx=10, pady=20, sticky="w")

    # TOTAL BALANCE - Tampilkan berdasarkan akun yang dipilih
    totalbalance_card = tk.Frame(main_page, bg="white", width=260, height=90, 
                                 highlightbackground="black", highlightthickness=1)
    totalbalance_card.grid(row=2, column=0, padx=10, pady=20, sticky="ew")
    totalbalance_card.grid_propagate(False)
    
    # AKUN DIPILIH
    selected_account = current_account.get()
    
    # PRINT SELECTED DI TERMINAL
    print(f"DEBUG - Selected Account: '{selected_account}'")
    print(f"DEBUG - Available Accounts: {list(logic.akun.keys())}")
    
    # 
    is_specific_account = (
        selected_account 
        and selected_account != "" 
        and selected_account != "All Accounts" 
        and selected_account in logic.akun
    )
    
    print(f"DEBUG - Is Specific Account: {is_specific_account}")
    
    if is_specific_account:
        tk.Label(totalbalance_card, text=f"Balance: {selected_account}", bg="white", fg="gray", 
                font=("Arial", 9)).place(x=10, y=10)
        balance = logic.account_balance(selected_account)
        print(f"DEBUG - Account Balance for '{selected_account}': {balance}")
    else:
        tk.Label(totalbalance_card, text="Total Cash Balance (All)", bg="white", fg="gray", 
                font=("Arial", 9)).place(x=10, y=10)
        balance = logic.total_balance()
        print(f"DEBUG - Total Balance (All): {balance}")
    
    #WARNA FONT
    balance_warna = "green" if balance >= 0 else "red"
    tk.Label(totalbalance_card, text=f"Rp {balance:,}", bg="white", fg=balance_warna, 
             font=("Arial", 14, "bold")).place(x=10, y=40)

    # INCOME CARD
    income_card = tk.Frame(main_page, bg="white", width=260, height=90, 
                          highlightbackground="black", highlightthickness=1)
    income_card.grid(row=2, column=1, padx=10, pady=20, sticky="ew")
    income_card.grid_propagate(False)
    
    if is_specific_account:
        tk.Label(income_card, text=f"Income: {selected_account}", bg="white", fg="gray",
                font=("Arial", 9)).place(x=10, y=10)
        income = logic.account_income(selected_account)
    else:
        tk.Label(income_card, text="Total Income (All)", bg="white", fg="gray",
                font=("Arial", 9)).place(x=10, y=10)
        income = logic.total_income()
    
    tk.Label(income_card, text=f"Rp {income:,}", bg="white", fg="green", 
             font=("Arial", 14, "bold")).place(x=10, y=40)

    # EXPENSE CARD
    expenses_card = tk.Frame(main_page, bg="white", width=260, height=90, 
                            highlightbackground="black", highlightthickness=1)
    expenses_card.grid(row=2, column=2, padx=10, pady=20, sticky="ew")
    expenses_card.grid_propagate(False)
    
    if is_specific_account:
        tk.Label(expenses_card, text=f"Expense: {selected_account}", bg="white", fg="gray",
                font=("Arial", 9)).place(x=10, y=10)
        expense = logic.account_expense(selected_account)
    else:
        tk.Label(expenses_card, text="Total Expenses (All)", bg="white", fg="gray",
                font=("Arial", 9)).place(x=10, y=10)
        expense = logic.total_expense()
    
    tk.Label(expenses_card, text=f"Rp {expense:,}", bg="white", fg="red", 
             font=("Arial", 14, "bold")).place(x=10, y=40)

    # RECENT ACTIVITIES
    recentActivities_card = tk.Frame(main_page, width=820, height=350, bg="white", 
                                     highlightbackground="black", highlightthickness=1)
    recentActivities_card.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
    recentActivities_card.grid_propagate(False)
    
    tk.Label(recentActivities_card, text="Recent Activities", bg="white", fg="grey", 
             font=("Arial", 12, "bold")).place(x=10, y=10)
    
    # RECENT ACTIVITIES SCROLL
    canvas = tk.Canvas(recentActivities_card, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(recentActivities_card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # RECENT TRANSACTION
    all_transactions = []
    for account_name, transactions in logic.akun.items():
        for t in transactions:
            all_transactions.append((account_name, t))
    
    # 10 TRANSAKSI
    recent = all_transactions[-10:]
    recent.reverse()
    
    if recent:
        y_pos = 0
        for account_name, t in recent:
            color = "green" if t["jenis"] == "income" else "red"
            sign = "+" if t["jenis"] == "income" else "-"
            
            transaction_frame = tk.Frame(scrollable_frame, bg="white")
            transaction_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(transaction_frame, text=f"{account_name}", bg="white", 
                    font=("Arial", 10, "bold")).pack(side="left")
            tk.Label(transaction_frame, text=f" | {t['kategori']}", bg="white", 
                    font=("Arial", 10)).pack(side="left")
            tk.Label(transaction_frame, text=f" | {sign}Rp {t['jumlah']:,}", bg="white", 
                    fg=color, font=("Arial", 10, "bold")).pack(side="left")
    else:
        tk.Label(scrollable_frame, text="No transactions yet. Add some to get started!", 
                bg="white", fg="gray").pack(padx=10, pady=20)
    
    canvas.place(x=0, y=40, width=800, height=300)
    scrollbar.place(x=800, y=40, height=300)
    

def page_summary():
    clear_main_page()
    
    tk.Label(main_page, text="Financial Summary", bg="#E4E4E4", 
             font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=3, pady=20)

    button_incomeSummary = tk.Button(main_page, text="Income Summary", bg="lightgreen", 
                                     fg="black", width=20, height=3, 
                                     command=logic.pie_income, font=("Arial", 12))
    button_incomeSummary.grid(row=1, column=0, padx=20, pady=40)

    button_expensesSummary = tk.Button(main_page, text="Expenses Summary", bg="lightcoral", 
                                       fg="black", width=20, height=3, 
                                       command=logic.pie_expense, font=("Arial", 12))
    button_expensesSummary.grid(row=1, column=2, padx=20, pady=40)
    
    # SUMMARY AKUN
    stats_frame = tk.Frame(main_page, bg="white", highlightbackground="black", 
                          highlightthickness=1)
    stats_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
    
    tk.Label(stats_frame, text="Total Accounts: ", bg="white", 
             font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
    tk.Label(stats_frame, text=str(len(logic.akun)), bg="white", 
             font=("Arial", 12, "bold")).grid(row=0, column=1, padx=20, pady=10, sticky="w")
    
    total_transactions = sum(len(trans) for trans in logic.akun.values())
    tk.Label(stats_frame, text="Total Transactions: ", bg="white", 
             font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
    tk.Label(stats_frame, text=str(total_transactions), bg="white", 
             font=("Arial", 12, "bold")).grid(row=1, column=1, padx=20, pady=10, sticky="w")

def page_plan():
    clear_main_page()

    tk.Label(
        main_page,
        text="Financial Planning",
        bg="white",
        fg="black",
        font=("Poppins", 18, "bold")
    ).pack(pady=15)

    #Template 50-30-20
    tk.Button(
        main_page, text="Template 50-30-20",
        command=logic.apply_503020,
        bg="white", fg="black", bd=0,
        font=("Poppins", 11), padx=8, pady=4
    ).pack(pady=5)

    #PYF
    tk.Button(
        main_page, text="Template Pay Yourself First",
        command=logic.apply_PYF,
        bg="white", fg="black", bd=0,
        font=("Poppins", 11), padx=8, pady=4
    ).pack(pady=5)

    #Reminder Tabungan
    tk.Button(
        main_page,
        command=lambda: logic.start_saving_reminder(root),
        text="Reminder Tabungan",
        bg="white", fg="black", bd=0,
        font=("Poppins", 11), padx=8, pady=4
    ).pack(pady=20)

    #KALKU INFLASI
    tk.Button(
        main_page, text="Hitung Inflasi",
        command=logic.hitung_inflasi,
        bg="black", fg="white", bd=0,
        font=("Poppins", 11), padx=10, pady=4
    ).pack(pady=10)


# MENU BAR
sidebar_menu = tk.Frame(root, bg="white", width=180, height=400)
sidebar_menu.grid(row=0, column=1, sticky="ns", padx=10, pady=20)

# BUTTON DI SIDEBAR
button_transaction = tk.Button(sidebar_menu, bg="white", text="Transaction", 
                               width=12, height=2, font=("Poppins", 12), 
                               command=page_transaksi)
button_summary = tk.Button(sidebar_menu, text="Summary", width=12, height=2, 
                          font=("Poppins", 12), command=page_summary)
button_plan = tk.Button(sidebar_menu, text="Plan", width=12, height=2, 
                       font=("Poppins", 12), command=page_plan)

# PACKING BUTTON
button_transaction.grid(row=0, pady=(20, 15))
button_summary.grid(row=1, pady=(0, 15))
button_plan.grid(row=2, pady=(0, 15))

page_transaksi()
root.mainloop()
