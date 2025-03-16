import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from thread_manager.manager import set_stop_flag
from handle_data.data import get_data

def search_client(*args):
    full_name, phone, email = args
    data = get_data()
    for client in data.get("clients", []):
        if phone and client.get("phone") == phone:
            return client
        if not phone and full_name and email:
            if client.get("fullName") == full_name and client.get("email") == email:
                return client
    return None

def main_tk(logo_path):
    root = tk.Tk()
    root.title("Soler Realty NYC")
    root.iconbitmap(logo_path)

    # Set an initial and maximum window size
    root.geometry("800x600")  # Fits most screens comfortably
    root.maxsize(1000, 800)   # Prevents the window from growing too large

    # Variable for comments list
    current_comments = []

    # Create a canvas and scrollbar for scrolling
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the form
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Place the canvas and scrollbar in the window
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Client Info Frame ---
    client_info_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2)
    client_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(client_info_frame, text="Full Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_fullname = tk.Entry(client_info_frame, width=40)
    entry_fullname.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(client_info_frame, text="Phone Number:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_phone = tk.Entry(client_info_frame, width=40)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(client_info_frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_email = tk.Entry(client_info_frame, width=40)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    # --- Inquiry Details Frame ---
    inquiry_details_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2)
    inquiry_details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(inquiry_details_frame, text="Inquiry Type (Rent/Buy/Sell):").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    inquiry_type_var = tk.StringVar(root)
    inquiry_type_var.set("Rent")
    inquiry_options = ["Rent", "Buy", "Sell"]
    inquiry_dropdown = tk.OptionMenu(inquiry_details_frame, inquiry_type_var, *inquiry_options)
    inquiry_dropdown.config(width=38)
    inquiry_dropdown.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(inquiry_details_frame, text="Specific Property (if applicable):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_property = tk.Entry(inquiry_details_frame, width=40)
    entry_property.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(inquiry_details_frame, text="Payment Method:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    payment_method_var = tk.StringVar(root)
    payment_method_var.set("Cash")
    payment_options = ["Cash", "Housing-Voucher", "Pre-approval (Sell)", "Other (Comment)"]
    payment_dropdown = tk.OptionMenu(inquiry_details_frame, payment_method_var, *payment_options)
    payment_dropdown.config(width=38)
    payment_dropdown.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(inquiry_details_frame, text="Urgency/Timeline (for selling):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_urgency = tk.Entry(inquiry_details_frame, width=40)
    entry_urgency.grid(row=3, column=1, padx=5, pady=5)

    # --- Comments Frame ---
    comments_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2)
    comments_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    comments_frame.columnconfigure(0, weight=1)
    comments_frame.rowconfigure(1, weight=1)

    tk.Label(comments_frame, text="Comments:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    comment_date_var = tk.StringVar(root)
    comment_date_var.set("")
    comment_date_dropdown = tk.OptionMenu(comments_frame, comment_date_var, "")
    comment_date_dropdown.config(width=15)
    comment_date_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    text_comments = scrolledtext.ScrolledText(comments_frame, width=80, height=10)
    text_comments.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # --- Buttons ---
    def search_and_update():
        nonlocal current_comments
        full_name_val = entry_fullname.get()
        phone_val = entry_phone.get()
        email_val = entry_email.get()
        client = search_client(full_name_val, phone_val, email_val)
        if client is not None:
            entry_fullname.delete(0, tk.END)
            entry_fullname.insert(0, client.get("fullName", ""))
            entry_phone.delete(0, tk.END)
            entry_phone.insert(0, client.get("phone", ""))
            entry_email.delete(0, tk.END)
            entry_email.insert(0, client.get("email", ""))
            inquiry_type_var.set(client.get("inquiryType", "Rent"))
            entry_property.delete(0, tk.END)
            entry_property.insert(0, client.get("specificProperty", ""))
            payment = client.get("paymentMethod")
            payment_method_var.set(payment if payment is not None else "Cash")
            entry_urgency.delete(0, tk.END)
            entry_urgency.insert(0, client.get("urgency") or "")
            current_comments = client.get("comments") or []
            dates = [comment.get("date", "") for comment in current_comments if comment.get("date")]
            dates.sort()
            menu = comment_date_dropdown["menu"]
            menu.delete(0, "end")
            if dates:
                for d in dates:
                    menu.add_command(label=d, command=lambda date=d: comment_date_var.set(date))
                comment_date_var.set(dates[-1])
            else:
                comment_date_var.set("")
                text_comments.delete("1.0", tk.END)
        else:
            print("Client not found.")

    def update_comment_text(*args):
        selected_date = comment_date_var.get()
        for comment in current_comments:
            if comment.get("date") == selected_date:
                text_comments.delete("1.0", tk.END)
                text_comments.insert("1.0", comment.get("comment", ""))
                break

    comment_date_var.trace_add("write", update_comment_text)

    search_button = tk.Button(client_info_frame, text="Search Client", command=search_and_update)
    search_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")

    def on_submit():
        comment_text = text_comments.get("1.0", tk.END).strip()
        new_comment = {"date": datetime.now().strftime("%Y-%m-%d"), "comment": comment_text} if comment_text else {}
        root.client_data = {
            "Full Name": entry_fullname.get(),
            "Phone Number": entry_phone.get(),
            "Email": entry_email.get(),
            "Inquiry Type": inquiry_type_var.get(),
            "Specific Property": entry_property.get(),
            "Payment Method": payment_method_var.get(),
            "Urgency/Timeline": entry_urgency.get(),
            "Comments": [new_comment] if new_comment else []
        }
        set_stop_flag()
        root.destroy()

    submit_button = tk.Button(scrollable_frame, text="Continue", command=on_submit)
    submit_button.grid(row=3, column=0, pady=10, sticky="e")

    return root