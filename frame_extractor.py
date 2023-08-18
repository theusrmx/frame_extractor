import cv2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from threading import Thread

class VideoToFramesConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Vídeo para Frames")

        self.video_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.progress_var = tk.DoubleVar()

        tk.Label(self.root, text="Selecione o vídeo de entrada:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.video_path, width=50).pack(pady=5)
        tk.Button(self.root, text="Selecionar Vídeo", command=self.select_video).pack()

        tk.Label(self.root, text="Selecione o diretório de saída para os frames:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.output_dir, width=50).pack(pady=5)
        tk.Button(self.root, text="Selecionar Diretório", command=self.select_output_dir).pack()

        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10)

        tk.Button(self.root, text="Converter Vídeo para Frames", command=self.convert_video).pack()

    def select_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Arquivos de Vídeo", "*.mp4 *.avi *.mkv")])
        if video_path:
            self.video_path.set(video_path)

    def select_output_dir(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir.set(output_dir)

    def convert_video(self):
        video_path = self.video_path.get()
        output_dir = self.output_dir.get()

        if not video_path or not output_dir:
            messagebox.showerror("Erro", "Por favor, selecione o vídeo de entrada e o diretório de saída.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0

        def conversion_thread():
            nonlocal frame_count
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_filename = os.path.join(output_dir, f'{frame_count:04d}.jpg')
                cv2.imwrite(frame_filename, frame)
                frame_count += 1
                self.progress_var.set((frame_count / total_frames) * 100)

            cap.release()
            messagebox.showinfo("Conclusão", f"Total de frames separados: {frame_count}")

        thread = Thread(target=conversion_thread)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToFramesConverter(root)
    root.mainloop()
