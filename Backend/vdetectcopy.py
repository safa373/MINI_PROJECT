# from __future__ import absolute_import
# from __future__  import division
# from __future__ import print_function
# import tensorflow as tf
# import numpy as np
# from skimage.io import imread
# from skimage.transform import resize
# import cv2
# import numpy as np
# import os
# from PIL import Image
# from io import BytesIO
# import time
#
# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())
#
# def mamon_videoFightModel2(tf,wight='mamonbest947oscombo-drive.hdfs'):
#     layers = tf.keras.layers
#     models = tf.keras.models
#     losses = tf.keras.losses
#     optimizers = tf.keras.optimizers
#     metrics = tf.keras.metrics
#     num_classes = 2
#     cnn = models.Sequential()
#     #cnn.add(base_model)
#
#     input_shapes=(160,160,3)
#     np.random.seed(1234)
#     vg19 = tf.keras.applications.vgg19.VGG19
#     base_model = vg19(include_top=False,weights='imagenet',input_shape=(160, 160,3))
#     # Freeze the layers except the last 4 layers
#     #for layer in base_model.layers:
#     #    layer.trainable = False
#
#     cnn = models.Sequential()
#     cnn.add(base_model)
#     cnn.add(layers.Flatten())
#     model = models.Sequential()
#
#     model.add(layers.TimeDistributed(cnn,  input_shape=(30, 160, 160, 3)))
#     model.add(layers.LSTM(30 , return_sequences= True))
#
#     model.add(layers.TimeDistributed(layers.Dense(90)))
#     model.add(layers.Dropout(0.1))
#
#     model.add(layers.GlobalAveragePooling1D())
#
#     model.add(layers.Dense(512, activation='relu'))
#     model.add(layers.Dropout(0.3))
#
#     model.add(layers.Dense(num_classes, activation="sigmoid"))
#
#     adam = optimizers.Adam(lr=0.0005, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
#     model.load_weights(wight)
#     rms = optimizers.RMSprop()
#
#     model.compile(loss='binary_crossentropy', optimizer=adam, metrics=["accuracy"])
#
#     return model
#
# import numpy as np
# from skimage.transform import resize
# np.random.seed(1234)
# model22 = mamon_videoFightModel2(tf)
#
#
# def video_mamonreader(cv2,filename):
#     frames = np.zeros((30, 160, 160, 3), dtype=np.float)
#     i=0
#     print(frames.shape)
#     vc = cv2.VideoCapture(filename)
#     if vc.isOpened():
#         rval , frame = vc.read()
#     else:
#         rval = False
#     frm = resize(frame,(160,160,3))
#     frm = np.expand_dims(frm,axis=0)
#     if(np.max(frm)>1):
#         frm = frm/255.0
#     frames[i][:] = frm
#     i +=1
#     print("reading video")
#     while i < 30:
#         rval, frame = vc.read()
#         frm = resize(frame,(160,160,3))
#         frm = np.expand_dims(frm,axis=0)
#         if(np.max(frm)>1):
#             frm = frm/255.0
#         frames[i][:] = frm
#         i +=1
#     return frames
#
# def pred_fight(model,video,acuracy=0.9):
#     pred_test = model.predict(video)
#     if pred_test[0][1] >=acuracy:
#         return True , pred_test[0][1]
#     else:
#         return False , pred_test[0][1]
#
#
# def main_fight(vidoss):
#     vid = video_mamonreader(cv2,vidoss)
#     datav = np.zeros((1, 30, 160, 160, 3), dtype=np.float)
#     datav[0][:][:] = vid
#     millis = int(round(time.time() * 1000))
#     print(millis)
#     f , precent = pred_fight(model22,datav,acuracy=0.65)
#     millis2 = int(round(time.time() * 1000))
#     print(millis2)
#     res_mamon = {'fight':f , 'precentegeoffight':str(precent)}
#     res_mamon['processing_time'] =  str(millis2-millis)
#     return res_mamon
#
#
#
#
# res = main_fight('cpl.mp4')
# print(res)
#
#
# res = main_fight('cpl2.mp4')
# print(res)
#
# res = main_fight('bully.mp4')
# print(res)
#
# res = main_fight('fight12.mp4')
# print(res)
#
#
#
#
#
#
#
#
#
#
#


# from __future__ import absolute_import, division, print_function
# import tensorflow as tf
# import numpy as np
# import cv2
# from skimage.transform import resize
# import time
#
# # ============================
# # Build the Fight Detection Model
# # ============================
# def mamon_videoFightModel2(weight_path=r'C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\mamonbest947oscombo-drive.hdfs'):
#     layers = tf.keras.layers
#     models = tf.keras.models
#     optimizers = tf.keras.optimizers
#
#     num_classes = 2
#     input_shape = (160, 160, 3)
#
#     # Base CNN (VGG19 pretrained)
#     base_model = tf.keras.applications.vgg19.VGG19(
#         include_top=False, weights='imagenet', input_shape=input_shape
#     )
#
#     cnn = models.Sequential([
#         base_model,
#         layers.Flatten()
#     ])
#
#     # Full model (CNN + LSTM)
#     model = models.Sequential()
#     model.add(layers.TimeDistributed(cnn, input_shape=(30, 160, 160, 3)))
#     model.add(layers.LSTM(30, return_sequences=True))
#     model.add(layers.TimeDistributed(layers.Dense(90)))
#     model.add(layers.Dropout(0.1))
#     model.add(layers.GlobalAveragePooling1D())
#     model.add(layers.Dense(512, activation='relu'))
#     model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(num_classes, activation="sigmoid"))
#
#     # Optimizer
#     adam = optimizers.Adam(learning_rate=0.0005)
#     model.compile(loss='binary_crossentropy', optimizer=adam, metrics=["accuracy"])
#
#     # Load Trained Weights
#     model.load_weights(weight_path)
#
#     return model
#
#
# # ============================
# # Read Frames from Video
# # ============================
# def video_mamonreader(filename, max_frames=30, size=(160, 160)):
#     frames = np.zeros((max_frames, size[0], size[1], 3), dtype=np.float32)
#
#     cap = cv2.VideoCapture(filename)
#     i = 0
#     while i < max_frames:
#         ret, frame = cap.read()
#         if not ret:
#             break  # Stop if video ends
#
#         frame_resized = resize(frame, (*size, 3))
#         if np.max(frame_resized) > 1:
#             frame_resized = frame_resized / 255.0  # Normalize to [0,1]
#
#         frames[i] = frame_resized
#         i += 1
#
#     cap.release()
#     return frames
#
#
# # ============================
# # Prediction Function
# # ============================
# def pred_fight(model, video, threshold=0.65):
#     pred = model.predict(video)
#     fight_prob = pred[0][1]
#     return (fight_prob >= threshold), fight_prob
#
#
# # ============================
# # Main Function
# # ============================
# def main_fight(video_path, model):
#     start_time = int(round(time.time() * 1000))
#
#     frames = video_mamonreader(video_path)
#     datav = np.expand_dims(frames, axis=0)  # (1, 30, 160, 160, 3)
#
#     fight_detected, prob = pred_fight(model, datav, threshold=0.65)
#
#     end_time = int(round(time.time() * 1000))
#     result = {
#         'fight_detected': fight_detected,
#         'fight_probability': float(prob),
#         'processing_time_ms': end_time - start_time
#     }
#     return result
#
#
# # ============================
# # Example Run
# # ============================
# if __name__ == "__main__":
#     # model22 = mamon_videoFightModel2('mamonbest947oscombo-drive.hdfs')
#
#     test_videos = ['cpl.mp4', 'cpl2.mp4', 'bully.mp4', 'fight12.mp4']
#     for vid in test_videos:
#         res = main_fight(vid, model22)
#         print(f"Video: {vid} => {res}")

import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from transformers import BlipProcessor, BlipForConditionalGeneration

# ============================
# Load BLIP Model
# ============================
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


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
        if not ret:
            break

        if frame_count % frame_skip == 0:
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
