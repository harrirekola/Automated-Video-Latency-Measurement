import tkinter as tk
from PIL import ImageTk, Image
import qrcode
import time
from datetime import datetime, timedelta
from decimal import Decimal
import json
import os
from qrcodegen import QrCode, QrSegment

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Convert QR code to PIL image
    img = qr.make_image(fill='black', back_color='white').convert("RGB")
    return img

# Function to append a timestamp to the JSON file
def add_timestamp_to_json(event_data, json_file=f'timestamps.json'):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(event_data)

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def start_qr_code_generation():
    start_button.pack_forget()
    root.after(5000, lambda: update_qr_code(0))

def update_qr_code(counter):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    qr_data = f"Frame number {counter} Timestamp: {timestamp}"

    start = time.perf_counter()
    img = generate_qr_code(qr_data)
    end = time.perf_counter()
    elapsed_time = end - start

    tk_img = ImageTk.PhotoImage(img)
    qr_label.config(image=tk_img)
    qr_label.image = tk_img

    timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    adjusted_timestamp_dt = timestamp_dt - timedelta(seconds=elapsed_time)
    adjusted_timestamp = adjusted_timestamp_dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    timestamp_label.config(text=f"Original Timestamp: {timestamp} | Adjusted Timestamp: {adjusted_timestamp} | Processing Time: {elapsed_time:.6f} seconds")

    event_data = {
        "frame": counter,
        "original_timestamp": timestamp,
        "adjusted_timestamp": adjusted_timestamp,
        "processing_time": elapsed_time
    }
    add_timestamp_to_json(event_data)

    # 1000 ms / desired FPS
    root.after(int(Decimal(1000) / Decimal(60)), update_qr_code, counter + 1)

if __name__ == "__main__":
    # JSON data

    # tkinter root window
    root = tk.Tk()
    root.geometry("300x300")
    root.attributes('-fullscreen', True)
    root.configure(background='white')

    # display QR code
    qr_label = tk.Label(root)
    qr_label.pack()

    # display timestamp
    timestamp_label = tk.Label(root, font=("Arial", 14), bg='black')
    timestamp_label.pack()

    # button to start the QR code generation
    start_button = tk.Button(root, text="Start", font=("Arial", 14), command=start_qr_code_generation)
    start_button.pack(pady=20)

    root.mainloop()
