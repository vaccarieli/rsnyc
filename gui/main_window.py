import tkinter as tk
from tkinter import scrolledtext, messagebox  # Added messagebox import
from datetime import datetime
from thread_manager.manager import set_stop_flag
from handle_data.data import search_client

# Helper functions for consistent widget styling
def create_label(parent, text, **kwargs):
    return tk.Label(parent, text=text, background='#2b2b2b', foreground='#e0e0e0', **kwargs)

def create_entry(parent, **kwargs):
    return tk.Entry(parent, background='#3c3c3c', foreground='#e0e0e0', insertbackground='#e0e0e0',
                    highlightthickness=1, highlightbackground='#2b2b2b', highlightcolor='#4d4d4d',
                    selectbackground='#4d4d4d', selectforeground='#e0e0e0', relief='flat', **kwargs)

def create_button(parent, text, command, **kwargs):
    return tk.Button(parent, text=text, command=command, background='#424242', foreground='#e0e0e0',
                     activebackground='#5e5e5e', activeforeground='#e0e0e0', relief='flat', borderwidth=0, **kwargs)

def create_option_menu(parent, variable, options, **kwargs):
    option_menu = tk.OptionMenu(parent, variable, *options, **kwargs)
    option_menu.configure(background='#3c3c3c', foreground='#e0e0e0', activebackground='#4d4d4d', activeforeground='#e0e0e0')
    menu = option_menu["menu"]
    menu.configure(background='#3c3c3c', foreground='#e0e0e0', activebackground='#4d4d4d', activeforeground='#e0e0e0')
    return option_menu

def main_tk(logo_path):
    root = tk.Tk()
    root.title("Soler Realty NYC")
    root.iconbitmap(logo_path)
    root.geometry("730x610")
    root.maxsize(1000, 800)
    root.configure(background='#2b2b2b')  # Dark background for the main window

    current_comments = []

    # Canvas and scrollbar setup
    canvas = tk.Canvas(root, background='#2b2b2b')
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview, 
                             background='#4d4d4d', troughcolor='#2b2b2b', activebackground='#5e5e5e')
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, background='#2b2b2b')
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Client Info Frame ---
    client_info_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2, background='#2b2b2b')
    client_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    create_label(client_info_frame, "Full Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_fullname = create_entry(client_info_frame, width=40)
    entry_fullname.grid(row=0, column=1, padx=5, pady=5)

    create_label(client_info_frame, "Phone Number:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_phone = create_entry(client_info_frame, width=40)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)

    create_label(client_info_frame, "Email:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_email = create_entry(client_info_frame, width=40)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    # --- Inquiry Details Frame ---
    inquiry_details_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2, background='#2b2b2b')
    inquiry_details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    create_label(inquiry_details_frame, "Inquiry Type:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    inquiry_type_var = tk.StringVar(root)
    inquiry_type_var.set("Rent")
    inquiry_options = ["Rent", "Buy", "Sell"]
    inquiry_dropdown = create_option_menu(inquiry_details_frame, inquiry_type_var, inquiry_options)
    inquiry_dropdown.config(width=38)
    inquiry_dropdown.grid(row=0, column=1, padx=5, pady=5)

    create_label(inquiry_details_frame, "Property Address of Interest:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_property = create_entry(inquiry_details_frame, width=40)
    entry_property.grid(row=1, column=1, padx=5, pady=5)

    create_label(inquiry_details_frame, "Payment Method:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    payment_method_var = tk.StringVar(root)
    payment_method_var.set("Cash")
    payment_options = ["Cash (Rent/Buy)", "Housing-Voucher (Rent)", "Pre-approval (Sell)", "Other (Comment)"]
    payment_dropdown = create_option_menu(inquiry_details_frame, payment_method_var, payment_options)
    payment_dropdown.config(width=38)
    payment_dropdown.grid(row=2, column=1, padx=5, pady=5)

    create_label(inquiry_details_frame, "Urgency:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_urgency = create_entry(inquiry_details_frame, width=40)
    entry_urgency.grid(row=3, column=1, padx=5, pady=5)

    # --- Comments Frame ---
    comments_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2, background='#2b2b2b')
    comments_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    comments_frame.columnconfigure(0, weight=1)
    comments_frame.rowconfigure(1, weight=1)

    create_label(comments_frame, "Comments:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    comment_date_var = tk.StringVar(root)
    comment_date_var.set("")
    comment_date_dropdown = create_option_menu(comments_frame, comment_date_var, [""])
    comment_date_dropdown.config(width=15)
    comment_date_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    text_comments = scrolledtext.ScrolledText(comments_frame, width=80, height=10, background='#3c3c3c', foreground='#e0e0e0',
                                              insertbackground='#e0e0e0', highlightthickness=1, highlightbackground='#2b2b2b',
                                              highlightcolor='#4d4d4d', selectbackground='#4d4d4d', selectforeground='#e0e0e0')
    text_comments.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    text_comments.vbar.configure(background='#4d4d4d', troughcolor='#2b2b2b', activebackground='#5e5e5e')

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
            entry_property.insert(0, client.get("propertyOfInterest", ""))
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

    search_button = create_button(client_info_frame, "Search Client", search_and_update)
    search_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")

    def on_submit():
        # Check if mandatory fields are empty
        if not entry_fullname.get().strip() or not entry_phone.get().strip() or not entry_email.get().strip():
            # Show dialog with options to continue or exit
            exit_choice = messagebox.askyesno(
                "Missing Information",
                "Mandatory fields are missing. Do you want to exit the application?\n\n- Click 'Yes' to exit\n- Click 'No' to accept and continue filling the form",
                parent=root
            )
            if exit_choice:  # User clicked 'Yes' to exit
                # Show confirmation dialog
                confirm_exit = messagebox.askyesno(
                    "Confirm Exit",
                    "Are you sure you want to lose all information entered?",
                    parent=root
                )
                if confirm_exit:  # User confirmed 'Yes' to exit
                    set_stop_flag()  # Cleanup any background processes
                    root.destroy()   # Close the application
                # If 'No' in confirmation, return to form (do nothing)
            # If 'No' in first dialog, return to form (do nothing)
        else:
            # Proceed with form submission if all fields are filled
            comment_text = text_comments.get("1.0", tk.END).strip()
            new_comment = {"date": datetime.now().strftime("%Y-%m-%d"), "comment": comment_text} if comment_text else {}
            root.client_data = {
                "Full Name": entry_fullname.get().strip(),
                "Phone Number": entry_phone.get().strip(),
                "Email": entry_email.get().strip(),
                "Inquiry Type": inquiry_type_var.get(),
                "Specific Property": entry_property.get().strip(),
                "Payment Method": payment_method_var.get(),
                "Urgency/Timeline": entry_urgency.get().strip(),
                "Comments": [new_comment] if new_comment else []
            }
            set_stop_flag()
            root.destroy()

    submit_button = create_button(scrollable_frame, "Continue", on_submit)
    submit_button.grid(row=3, column=0, pady=10, sticky="e")

    return root