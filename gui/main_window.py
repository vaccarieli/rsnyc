import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import re
from thread_manager.manager import set_stop_flag
from handle_data.data import search_client

# List of country codes
country_codes = [
    "+1 (USA, Canada, Puerto Rico)",
    "+507 (Panama)",
    "+58 (Venezuela)",
    "+44 (United Kingdom)",
    "+33 (France)",
    # Add more as needed
]

# **Helper Functions for Widget Creation**
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

# **Phone Number Formatting Functions**
def format_us_phone_number(input_str):
    digits = ''.join(filter(str.isdigit, input_str))[:10]
    if len(digits) <= 3:
        return digits
    elif len(digits) <= 6:
        return f"({digits[:3]}) {digits[3:]}"
    else:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

def format_panama_phone_number(input_str):
    digits = ''.join(filter(str.isdigit, input_str))[:8]
    if len(digits) <= 4:
        return digits
    else:
        return f"{digits[:4]}-{digits[4:]}"

def format_venezuela_phone_number(input_str):
    digits = ''.join(filter(str.isdigit, input_str))[:10]
    if len(digits) <= 3:
        return digits
    else:
        return f"{digits[:3]}-{digits[3:]}"

# Dictionary mapping country codes to formatting functions
formatters = {
    "+1": format_us_phone_number,
    "+507": format_panama_phone_number,
    "+58": format_venezuela_phone_number,
    # Add more formatters for other codes if needed
}

# Define setting_programmatically at module level
setting_programmatically = False

# **Main Tkinter Application Function**
def main_tk(logo_path):
    root = tk.Tk()
    root.title("Soler Realty NYC")
    root.iconbitmap(logo_path)
    root.geometry("730x610")
    root.maxsize(1000, 800)
    root.configure(background='#2b2b2b')

    current_comments = []

    # **Canvas and Scrollbar Setup**
    canvas = tk.Canvas(root, background='#2b2b2b')
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview,
                             background='#4d4d4d', troughcolor='#2b2b2b', activebackground='#5e5e5e')
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, background='#2b2b2b')
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # **Client Info Frame**
    client_info_frame = tk.Frame(scrollable_frame, relief="groove", borderwidth=2, background='#2b2b2b')
    client_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    client_info_frame.columnconfigure(1, weight=1)
    client_info_frame.columnconfigure(2, weight=1)

    # Full Name
    create_label(client_info_frame, "Full Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_fullname = create_entry(client_info_frame, width=40)
    entry_fullname.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

    # Phone Number with Country Code Dropdown
    create_label(client_info_frame, "Phone Number:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    country_code_var = tk.StringVar(root)
    country_code_var.set(country_codes[0])  # Default to +1
    country_dropdown = create_option_menu(client_info_frame, country_code_var, country_codes)
    country_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Phone number entry with StringVar for dynamic formatting
    phone_var = tk.StringVar()
    entry_phone = create_entry(client_info_frame, width=30, textvariable=phone_var)
    entry_phone.grid(row=1, column=2, padx=5, pady=5, sticky="w")

    # Add validation for digits only
    def validate_phone_input(action, char):
        if action == '1':  # Insertion
            return char.isdigit()
        return True  # Allow deletions and other actions

    vcmd = root.register(validate_phone_input)
    entry_phone.config(validate='key', validatecommand=(vcmd, '%d', '%S'))

    # Add paste handling to filter non-digits
    def handle_paste(event):
        try:
            clipboard = root.clipboard_get()
            digits = ''.join(filter(str.isdigit, clipboard))
            entry_phone.insert(tk.INSERT, digits)
        except tk.TclError:
            pass
        return "break"  # Prevent default paste behavior

    entry_phone.bind("<Control-v>", handle_paste)

    # Add a small label with instructions
    create_label(client_info_frame, "(Enter digits only)").grid(row=2, column=2, sticky='w', padx=5, pady=0)

    # Email
    create_label(client_info_frame, "Email:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_email = create_entry(client_info_frame, width=40)
    entry_email.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

    # Search Button
    search_button = create_button(client_info_frame, "Search Client", lambda: search_and_update())
    search_button.grid(row=4, column=2, padx=5, pady=5, sticky="e")

    # **Inquiry Details Frame**
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

    # **Comments Frame**
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

    # **Phone Number Formatting Logic**
    def on_key_release(event):
        global setting_programmatically
        if setting_programmatically:
            return
        selected_code = country_code_var.get().split()[0]
        formatter = formatters.get(selected_code, lambda x: x)
        current_text = phone_var.get()
        formatted = formatter(current_text)
        if formatted != current_text:
            setting_programmatically = True
            phone_var.set(formatted)
            root.update_idletasks()  # Ensure UI updates are processed
            entry_phone.icursor(len(formatted))  # Move cursor to end
            setting_programmatically = False

    entry_phone.bind("<KeyRelease>", on_key_release)

    def on_country_code_change(*args):
        global setting_programmatically
        if setting_programmatically:
            return
        selected_code = country_code_var.get().split()[0]
        current_text = phone_var.get()
        digits = ''.join(filter(str.isdigit, current_text))
        formatter = formatters.get(selected_code, lambda x: x)
        formatted = formatter(digits)
        setting_programmatically = True
        phone_var.set(formatted)
        root.update_idletasks()  # Ensure UI updates are processed
        entry_phone.icursor(len(formatted))
        setting_programmatically = False

    country_code_var.trace_add("write", on_country_code_change)

    def search_and_update():
        nonlocal current_comments
        full_name_val = entry_fullname.get().strip()
        selected_country = country_code_var.get()
        country_code = selected_country.split()[0]
        digits = ''.join(filter(str.isdigit, entry_phone.get()))
        phone_val = (country_code + digits) if digits else None
        email_val = entry_email.get().strip()
        client = search_client(full_name_val, phone_val, email_val)
        
        if client is not None:
            # Update basic fields
            entry_fullname.delete(0, tk.END)
            entry_fullname.insert(0, client.get("fullName", ""))
            entry_email.delete(0, tk.END)
            entry_email.insert(0, client.get("email", ""))

            # Handle phone number formatting
            full_phone = client.get("phone", "")
            matched = False
            for cc in country_codes:
                code = cc.split()[0]
                if full_phone.startswith(code):
                    # Prevent formatting trigger during update
                    global setting_programmatically
                    setting_programmatically = True
                    
                    # Set country code dropdown
                    country_code_var.set(cc)
                    
                    # Extract local number and format
                    local_phone = full_phone[len(code):]
                    formatter = formatters.get(code, lambda x: x)
                    formatted_phone = formatter(local_phone)
                    
                    # Update phone entry directly
                    phone_var.set(formatted_phone)  # Use StringVar instead of widget insert
                    
                    setting_programmatically = False
                    matched = True
                    break
            
            if not matched:
                # Fallback for unknown country codes
                setting_programmatically = True
                country_code_var.set(country_codes[0])
                phone_var.set(full_phone)
                setting_programmatically = False

            # Update other fields
            inquiry_type_var.set(client.get("inquiryType", "Rent"))
            entry_property.delete(0, tk.END)
            entry_property.insert(0, client.get("propertyOfInterest", ""))
            payment = client.get("paymentMethod")
            payment_method_var.set(payment if payment is not None else "Cash")
            entry_urgency.delete(0, tk.END)
            entry_urgency.insert(0, client.get("urgency") or "")
            
            # Handle comments
            current_comments = client.get("comments") or []
            dates = [c.get("date", "") for c in current_comments if c.get("date")]
            dates.sort()
            menu = comment_date_dropdown["menu"]
            menu.delete(0, "end")
            for d in dates:
                menu.add_command(label=d, command=lambda date=d: comment_date_var.set(date))
            comment_date_var.set(dates[-1] if dates else "")
            update_comment_text()
            
        else:
            print("Client not found.")

    # **Update Comment Text Function**
    def update_comment_text(*args):
        selected_date = comment_date_var.get()
        for comment in current_comments:
            if comment.get("date") == selected_date:
                text_comments.delete("1.0", tk.END)
                text_comments.insert("1.0", comment.get("comment", ""))
                break

    comment_date_var.trace_add("write", update_comment_text)

    # **Submit Function**
    def on_submit():
        full_name = entry_fullname.get().strip()
        selected_country = country_code_var.get()
        phone_number = entry_phone.get().strip()
        email = entry_email.get().strip()

        if not full_name or not phone_number or not email:
            exit_choice = messagebox.askyesno(
                "Missing Information",
                "Mandatory fields (Full Name, Phone Number, Email) are missing. Do you want to exit?\n\n- 'Yes' to exit\n- 'No' to continue filling the form",
                parent=root
            )
            if exit_choice:
                confirm_exit = messagebox.askyesno(
                    "Confirm Exit",
                    "Are you sure you want to lose all information entered?",
                    parent=root
                )
                if confirm_exit:
                    set_stop_flag()
                    root.destroy()
        else:
            errors = []
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Email must be in a valid format (e.g., example@domain.com).")
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors), parent=root)
            else:
                comment_text = text_comments.get("1.0", tk.END).strip()
                new_comment = {"date": datetime.now().strftime("%Y-%m-%d"), "comment": comment_text} if comment_text else {}
                country_code = selected_country.split()[0]
                digits = ''.join(filter(str.isdigit, phone_number))
                full_phone_number = country_code + digits
                root.client_data = {
                    "Full Name": full_name,
                    "Phone Number": full_phone_number,
                    "Email": email,
                    "Inquiry Type": inquiry_type_var.get(),
                    "Specific Property": entry_property.get().strip(),
                    "Payment Method": payment_method_var.get(),
                    "Urgency/Timeline": entry_urgency.get().strip(),
                    "Comments": [new_comment] if new_comment else []
                }
                set_stop_flag()
                root.destroy()

    # **Submit Button**
    submit_button = create_button(scrollable_frame, "Continue", on_submit)
    submit_button.grid(row=3, column=0, pady=10, sticky="e")

    return root