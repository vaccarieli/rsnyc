import tkinter as tk
from thread_manager.manager import set_stop_flag

def main_tk():
    root = tk.Tk()
    root.title("Client Information Form")

    # Create and place labels and entries for each field
    tk.Label(root, text="Full Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_fullname = tk.Entry(root, width=40)
    entry_fullname.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Phone Number (Best Contact):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_phone = tk.Entry(root, width=40)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_email = tk.Entry(root, width=40)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Inquiry Type (Rent/Buy/Sell):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_inquiry = tk.Entry(root, width=40)
    entry_inquiry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(root, text="Specific Property (if applicable):").grid(row=4, column=0, sticky='e', padx=5, pady=5)
    entry_property = tk.Entry(root, width=40)
    entry_property.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(root, text="Payment Method (for buying):").grid(row=5, column=0, sticky='e', padx=5, pady=5)
    entry_payment = tk.Entry(root, width=40)
    entry_payment.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(root, text="Urgency/Timeline (for selling):").grid(row=6, column=0, sticky='e', padx=5, pady=5)
    entry_urgency = tk.Entry(root, width=40)
    entry_urgency.grid(row=6, column=1, padx=5, pady=5)

    def on_submit():
        # Gather the form data into a dictionary
        root.client_data = {
            "Full Name": entry_fullname.get(),
            "Phone Number": entry_phone.get(),
            "Email": entry_email.get(),
            "Inquiry Type": entry_inquiry.get(),
            "Specific Property": entry_property.get(),
            "Payment Method": entry_payment.get(),
            "Urgency/Timeline": entry_urgency.get()
        }

        # Signal to stop the recording loop
        set_stop_flag()

        # Optionally, close the window once done
        root.destroy()

    # Create the Continue button
    submit_button = tk.Button(root, text="Continue", command=on_submit)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    return root
