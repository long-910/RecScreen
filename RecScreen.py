import tkinter as tk
from tkinter import ttk
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageTk

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.root.geometry("400x300")

        self.record_button = ttk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=5)

        self.gif_button = ttk.Button(self.root, text="Convert to GIF", command=self.convert_to_gif, state="disabled")
        self.gif_button.pack(pady=5)

        self.window_label = ttk.Label(self.root, text="Window coordinates (x, y, width, height):")
        self.window_label.pack()
        self.window_entry = ttk.Entry(self.root)
        self.window_entry.insert(0, "0, 0, 800, 600")  # デフォルト値
        self.window_entry.pack(pady=5)

        self.fps_label = ttk.Label(self.root, text="FPS:")
        self.fps_label.pack()
        self.fps_entry = ttk.Entry(self.root)
        self.fps_entry.insert(0, "10")  # デフォルト値
        self.fps_entry.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=400, height=200)
        self.canvas.pack()

        self.recording = False
        self.out = None
        self.frames = []

    def start_recording(self):
        self.recording = True
        self.record_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.window_entry.config(state="disabled")
        self.fps_entry.config(state="disabled")

        window_x, window_y, window_width, window_height = map(int, self.window_entry.get().split(','))
        fps = int(self.fps_entry.get())

        filename = 'screen_record.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(filename, fourcc, fps, (window_width, window_height))

        self.record_screen(window_x, window_y, window_width, window_height)

    def record_screen(self, x, y, width, height):
        if self.recording:
            img = pyautogui.screenshot(region=(x, y, width, height))
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.out.write(frame)
            self.frames.append(frame)
            self.show_frame(frame)
            self.root.after(1000 // 10, self.record_screen, x, y, width, height)

    def stop_recording(self):
        self.recording = False
        self.out.release()
        self.record_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.gif_button.config(state="normal")
        self.window_entry.config(state="normal")
        self.fps_entry.config(state="normal")

    def show_frame(self, frame):
        frame = cv2.resize(frame, (400, 200))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor="nw", image=imgtk)

    def convert_to_gif(self):
        gif_filename = 'screen_record.gif'
        delay = int(1000 / int(self.fps_entry.get()))
        gif = cv2.VideoWriter(gif_filename, cv2.VideoWriter_fourcc(*'GIF'), int(self.fps_entry.get()), (400, 200))
        for frame in self.frames:
            gif.write(frame)
        gif.release()
        print("GIF saved as", gif_filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
