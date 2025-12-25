import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_video():
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.mov *.mkv *.avi")]
    )
    if file_path:
        input_path.set(file_path)

def compress_video():
    input_file = input_path.get()
    if not input_file:
        messagebox.showerror("Error", "Please select a video file")
        return

    output_file = os.path.splitext(input_file)[0] + "_compressed.mp4"

    command = [
        r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
        "-i", input_file,
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "medium",
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", f"Video compressed!\nSaved as:\n{output_file}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Compression failed")

# GUI
app = tk.Tk()
app.title("Local Video Compressor")
app.geometry("420x200")

input_path = tk.StringVar()

tk.Label(app, text="Select Video File", font=("Arial", 12)).pack(pady=10)
tk.Entry(app, textvariable=input_path, width=50).pack(pady=5)

tk.Button(app, text="Browse", command=select_video).pack(pady=5)
tk.Button(app, text="Compress Video", command=compress_video, bg="green", fg="white").pack(pady=15)

app.mainloop()
