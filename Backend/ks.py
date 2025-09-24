import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from transformers import BlipProcessor, BlipForConditionalGeneration

# ============================
# Load BLIP Model (LOCAL PATH)
# ============================
# Replace this path with the folder where your Salesforce model files are stored
local_model_path = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\Salesforce"

processor = BlipProcessor.from_pretrained(local_model_path)
blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)


# ============================
# Caption Generator
# ============================
def generate_caption(frame):
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    inputs = processor(pil_image, return_tensors="pt")
    output = blip_model.generate(**inputs, max_new_tokens=30)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption


def summarize_video(video_path, frame_skip=30):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    captions = []

    while True:
        ret, frame = cap.read()

        caption = generate_caption(frame)
        captions.append(caption)
        frame_count += 1

    cap.release()

    if not captions:
        return "No captions generated"

    # Simple summary: pick most frequent / first caption
    return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)


# ============================
# Tkinter Desktop App
# ============================
class VideoCaptionApp:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Video Caption Generator")

        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.caption_label = tk.Label(root, text="Generating caption...", font=("Arial", 14), wraplength=600)
        self.caption_label.pack(pady=10)

        # Generate video-level caption
        self.caption = summarize_video(video_path)
        self.caption_label.config(text=f"Video Caption: {self.caption}")

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.canvas.config(image=img)
            self.canvas.image = img

        self.root.after(30, self.update_frame)


# ============================
# Run App
# ============================
if __name__ == "__main__":
    video_file = "cpl.mp4"  # change this to your test video

    root = tk.Tk()
    app = VideoCaptionApp(root, video_file)
    root.mainloop()
