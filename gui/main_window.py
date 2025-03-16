import tkinter as tk
from datetime import datetime
from thread_manager.manager import set_stop_flag
from handle_data.data import get_data

def search_client(*args):
    # Unpack the arguments; assume they are provided in order: fullName, phone, email.
    full_name, phone, email = args
    data = get_data()  # Retrieve the JSON data

    for client in data.get("clients", []):
        # Use phone number as primary search criteria
        if phone and client.get("phone") == phone:
            return client
        # Fall back to matching fullName and email if phone is not provided.
        if not phone:
            if full_name and email:
                if client.get("fullName") == full_name and client.get("email") == email:
                    return client
    return None

def main_tk(logo_path):
    root = tk.Tk()
    root.title("Soler Realty NYC")
    root.iconbitmap(logo_path)
    
    # Variable to hold the current comments list from a found client.
    current_comments = []

    # --- Top Section: Full Name, Phone Number, Email, and Search Button ---
    tk.Label(root, text="Full Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_fullname = tk.Entry(root, width=40)
    entry_fullname.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Phone Number:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_phone = tk.Entry(root, width=40)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_email = tk.Entry(root, width=40)
    entry_email.grid(row=2, column=1, padx=5, pady=5)
    
    # Function to update the comments text based on selected date.
    def update_comment_text(*args):
        selected_date = comment_date_var.get()
        for comment in current_comments:
            if comment.get("date") == selected_date:
                text_comments.delete("1.0", tk.END)
                text_comments.insert("1.0", comment.get("comment", ""))
                break

    # Create the variable and OptionMenu for selecting comment dates.
    comment_date_var = tk.StringVar(root)
    comment_date_var.set("")  # Initially empty
    comment_date_dropdown = tk.OptionMenu(root, comment_date_var, "")
    comment_date_dropdown.config(width=15)
    comment_date_dropdown.grid(row=2, column=2, padx=5, pady=5, sticky="n")
    # Trace changes to update the comments text.
    comment_date_var.trace_add("write", update_comment_text)
    
    def search_and_update():
        nonlocal current_comments
        full_name_val = entry_fullname.get()
        phone_val = entry_phone.get()
        email_val = entry_email.get()
        client = search_client(full_name_val, phone_val, email_val)
        if client is not None:
            # Update basic fields
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
            
            # Update Comments dropdown.
            current_comments = client.get("comments") or []
            dates = [comment.get("date", "") for comment in current_comments if comment.get("date")]
            dates.sort()  # Sort dates in ascending order.
            # Update the OptionMenu with these dates.
            menu = comment_date_dropdown["menu"]
            menu.delete(0, "end")
            if dates:
                for d in dates:
                    menu.add_command(label=d, command=lambda date=d: comment_date_var.set(date))
                # Set default to the latest date.
                comment_date_var.set(dates[-1])
            else:
                comment_date_var.set("")
                text_comments.delete("1.0", tk.END)
        else:
            print("Client not found.")

    # Search Client Button on the right side, spanning rows 0-2
    search_button = tk.Button(root, text="Search Client", command=search_and_update)
    search_button.grid(row=0, column=2, rowspan=3, padx=5, pady=5, sticky="n")
    
    # --- Remaining Fields ---
    tk.Label(root, text="Inquiry Type (Rent/Buy/Sell):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    inquiry_type_var = tk.StringVar(root)
    inquiry_type_var.set("Rent")
    inquiry_options = ["Rent", "Buy", "Sell"]
    inquiry_dropdown = tk.OptionMenu(root, inquiry_type_var, *inquiry_options)
    inquiry_dropdown.config(width=38)
    inquiry_dropdown.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
    
    tk.Label(root, text="Specific Property (if applicable):").grid(row=4, column=0, sticky='e', padx=5, pady=5)
    entry_property = tk.Entry(root, width=40)
    entry_property.grid(row=4, column=1, padx=5, pady=5, columnspan=2)
    
    tk.Label(root, text="Payment Method:").grid(row=5, column=0, sticky='e', padx=5, pady=5)
    payment_method_var = tk.StringVar(root)
    payment_method_var.set("Cash")
    payment_options = ["Cash", "Housing-Voucher", "Pre-approval (Sell)", "Other (Comment)"]
    payment_dropdown = tk.OptionMenu(root, payment_method_var, *payment_options)
    payment_dropdown.config(width=38)
    payment_dropdown.grid(row=5, column=1, padx=5, pady=5, columnspan=2)
    
    tk.Label(root, text="Urgency/Timeline (for selling):").grid(row=6, column=0, sticky='e', padx=5, pady=5)
    entry_urgency = tk.Entry(root, width=40)
    entry_urgency.grid(row=6, column=1, padx=5, pady=5, columnspan=2)
    
    # Row 7: Comments (multiline text) with increased size and vertical scrollbar
    tk.Label(root, text="Comments:").grid(row=7, column=0, sticky='e', padx=5, pady=5)
    text_comments = tk.Text(root, width=80, height=18)
    text_comments.grid(row=7, column=1, padx=5, pady=5, columnspan=2)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=text_comments.yview)
    text_comments.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=7, column=3, sticky="ns", padx=5, pady=5)

    
    def on_submit():
        # Get the current comment text from the widget.
        comment_text = text_comments.get("1.0", tk.END).strip()
        # Create a new comment entry with today's date if comment_text is not empty.
        new_comment = {"date": datetime.now().strftime("%Y-%m-%d"), "comment": comment_text} if comment_text else {}
        
        # Save form data; here, we wrap the comment in a list.
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
    
    submit_button = tk.Button(root, text="Continue", command=on_submit)
    submit_button.grid(row=8, column=0, columnspan=3, pady=10)
    
    return root
