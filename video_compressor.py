import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import re

FFMPEG_PATH = r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

def select_video():
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.mov *.mkv *.avi")]
    )
    if file_path:
        input_path.set(file_path)

def get_video_duration(file_path):
    cmd = [FFMPEG_PATH, "-i", file_path]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        h, m, s = map(float, match.groups())
        return h * 3600 + m * 60 + s
    return 0

def compress_video():
    threading.Thread(target=run_compression).start()

def run_compression():
    input_file = input_path.get()
    if not input_file:
        messagebox.showerror("Error", "Please select a video file")
        return

    output_file = os.path.splitext(input_file)[0] + "_compressed.mp4"
    duration = get_video_duration(input_file)

    progress_bar["value"] = 0
    status_label.config(text="Starting compression...")

    command = [
        FFMPEG_PATH,
        "-i", input_file,
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "medium",
        "-progress", "pipe:1",
        "-nostats",
        output_file
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        if "out_time_ms" in line and duration > 0:
            out_time_ms = int(line.split("=")[1])
            progress = (out_time_ms / 1_000_000) / duration * 100
            progress = min(progress, 100)

            progress_bar["value"] = progress
            status_label.config(text=f"Compressing... {int(progress)}%")

    process.wait()

    progress_bar["value"] = 100
    status_label.config(text="Compression completed ✔")
    messagebox.showinfo("Success", f"Video compressed!\nSaved as:\n{output_file}")

# ---------------- GUI ---------------- #

app = tk.Tk()
app.title("Local Video Compressor")
app.geometry("460x260")
app.resizable(False, False)

input_path = tk.StringVar()

tk.Label(app, text="Select Video File", font=("Arial", 12)).pack(pady=8)
tk.Entry(app, textvariable=input_path, width=55).pack(pady=4)

tk.Button(app, text="Browse", command=select_video).pack(pady=4)
tk.Button(
    app,
    text="Compress Video",
    command=compress_video,
    bg="green",
    fg="white"
).pack(pady=10)

progress_bar = ttk.Progressbar(app, length=380, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(app, text="Waiting...", font=("Arial", 10))
status_label.pack()

app.mainloop()
