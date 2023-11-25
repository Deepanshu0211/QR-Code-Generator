import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("400x800")

        # Styles
        label_style = {'font': ('Helvetica', 12)}
        entry_style = {'font': ('Helvetica', 12), 'width': 20}
        button_style = {'font': ('Helvetica', 12), 'padx': 10, 'pady': 5}

        # Text Entry
        self.text_label = tk.Label(self.root, text="Enter text for QR code:", **label_style)
        self.text_label.pack(pady=(20, 0))

        self.text_entry = tk.Entry(self.root, **entry_style)
        self.text_entry.pack()

        # Image Upload
        self.image_label = tk.Label(self.root, text="Upload an image:", **label_style)
        self.image_label.pack(pady=(20, 0))

        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image, **button_style)
        self.upload_button.pack()

        # Generate QR Code Button
        self.generate_button = tk.Button(self.root, text="Generate QR Code", command=self.generate_qr_code, **button_style)
        self.generate_button.pack(pady=20)

        # Save QR Code Button
        self.save_button = tk.Button(self.root, text="Save QR Code", command=self.save_qr_code, **button_style)
        self.save_button.pack(pady=20)

        # Display QR Code
        self.qr_code_label = tk.Label(self.root, text="QR Code:", **label_style)
        self.qr_code_label.pack()

        self.qr_code_image_label = tk.Label(self.root)
        self.qr_code_image_label.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_path = file_path
        self.image_label.config(text=f"Image: {file_path}")

    def generate_qr_code(self):
        text_data = self.text_entry.get()

        if not text_data and not hasattr(self, 'image_path'):
            messagebox.showerror("Error", "Please enter text or upload an image.")
            return

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        if text_data:
            qr.add_data(text_data)
        elif hasattr(self, 'image_path'):
            with open(self.image_path, 'rb') as image_file:
                image_data = image_file.read()
                qr.add_data(image_data)

        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Display QR Code Image
        tk_image = ImageTk.PhotoImage(qr_image)
        self.qr_code_image_label.config(image=tk_image)
        self.qr_code_image_label.image = tk_image
        self.qr_code_image = qr_image

    def save_qr_code(self):
        if hasattr(self, 'qr_code_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            self.qr_code_image.save(file_path)
            messagebox.showinfo("Success", "QR Code saved successfully.")
        else:
            messagebox.showerror("Error", "No QR Code to save. Generate one first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
