# import cv2
# import numpy as np
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from DBConnection import Database  # make sure this works with your project
#
# # ============================
# # Load BLIP Model (LOCAL PATH)
# # ============================
# local_model_path = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\Salesforce"
#
# processor = BlipProcessor.from_pretrained(local_model_path)
# blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)
#
#
# # ============================
# # Caption Generator
# # ============================
# def generate_caption(frame):
#     pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     inputs = processor(pil_image, return_tensors="pt")
#     output = blip_model.generate(**inputs, max_new_tokens=30)
#     caption = processor.decode(output[0], skip_special_tokens=True)
#     return caption.lower()   # return in lowercase for easy matching
#
#
# # ============================
# # Violence Detection Keywords
# # ============================
# VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]
# student="SELECT * FROM `myapp_student`"
#
# def is_violent_caption(caption):
#     return any(word in caption for word in VIOLENCE_KEYWORDS)
#
# # ============================
# # Video Summarizer
# # ============================
# def summarize_video(video_path, frame_skip=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     captions = []
#     db = Database()   # Initialize DB connection
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         cv2.imshow("Video", frame)
#
#         if frame_count % frame_skip == 0:
#             caption = generate_caption(frame)
#             captions.append(caption)
#             print(f"[Frame {frame_count}] Caption: {caption}")
#
#             # Check if caption indicates violence
#             if is_violent_caption(caption):
#                 print("🚨 Violence Detected! Saving to Database...")
#                 from datetime import datetime
#                 mediapath = "C:\\Users\\amaya\\Desktop\\VIOLENCE DETECTION\\VIOLENCE DETECTION\\violencedetection web\\violencedetection\\media\\"
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 filepath = mediapath + filename
#                 cv2.imwrite(filepath, frame)
#
#                 # Insert into SQL (violence table)
#                 qry1 = f"INSERT INTO `myapp_violence` (`date`,`time`,`photo`) VALUES (CURDATE(),CURTIME(),'/media/{filename}')"
#                 violence_id = db.insert(qry1)  # <-- this should return the inserted row ID
#
#                 # Insert sub-image linked to violence_id
#                 qry2 = f"INSERT INTO `myapp_violencehub` (`action`,`STUDENT_id`,`VIOLENCE_id`) VALUES ('pending','1','{violence_id}')"
#                 db.insert(qry2)
#                 # violence_id = db.insert("INSERT INTO `myapp_violence` (`date`,`time`,`image`) VALUES (CURDATE(),CURTIME(),'/media/{filename}')")
#                 # db.insert(violence_id)
#                 #
#                 # # Save image proof
#                 #
#                 #
#                 # # Insert sub-image linked to violence_id
#                 # qry = f"INSERT INTO `myapp_incident_sub_images` (`action`,`STUDENT_id`,`VIOLENCE_id`) VALUES ('pending','1','{violence_id}')"
#                 # db.insert(qry)
#
#         frame_count += 1
#
#         # Quit with 'q'
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     if not captions:
#         return "No captions generated"
#
#     # Simple summary: pick most frequent caption
#     return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)
#
#
# # ============================
# # Run
# # ============================
# if __name__ == "__main__":
#     video_file = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\video1.mp4"
#     try:
#         summary = summarize_video(video_file, frame_skip=30)
#         print("\n=== Final Video Caption ===")
#         print(summary)
#     except Exception as e:
#         print("🔥 Error inside summarize_video():", e)
#     # summary = summarize_video(video_file, frame_skip=30)
#     # print("\n=== Final Video Caption ===")
#     # print(summary)

# import cv2
# import numpy as np
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import face_recognition
# import os
# from datetime import datetime
# from DBConnection import Database  # your DB connection class
#
# # ============================
# # Load BLIP Model (LOCAL PATH)
# # ============================
# local_model_path = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\Salesforce"
#
# processor = BlipProcessor.from_pretrained(local_model_path)
# blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)
#
# # ============================
# # Paths
# # ============================
# BASE_DIR = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection web\violencedetection"
# MEDIA_DIR = os.path.join(BASE_DIR, "media")
#
# # ============================
# # Violence Keywords
# # ============================
# VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]
#
# # ============================
# # Caption Generator
# # ============================
# def generate_caption(frame):
#     pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     inputs = processor(pil_image, return_tensors="pt")
#     output = blip_model.generate(**inputs, max_new_tokens=30)
#     caption = processor.decode(output[0], skip_special_tokens=True)
#     return caption.lower()  # lowercase for easy matching
#
# def is_violent_caption(caption):
#     return any(word in caption for word in VIOLENCE_KEYWORDS)
#
# # ============================
# # Face Matching Function
# # ============================
# def match_student(frame_path, db):
#     """Match violence frame with student photos in DB"""
#     try:
#         frame_img = face_recognition.load_image_file(frame_path)
#         frame_encodings = face_recognition.face_encodings(frame_img)
#         if not frame_encodings:
#             return None
#         frame_encoding = frame_encodings[0]
#     except Exception as e:
#         print("❌ Error encoding frame:", e)
#         return None
#
#     students = db.select("SELECT id, photo FROM myapp_student")
#
#     for student in students:
#         db_photo = student["photo"]  # stored like "/media/xxx.jpg"
#         student_photo_path = os.path.join(BASE_DIR, db_photo.strip("/"))
#
#         if not os.path.exists(student_photo_path):
#             print(f"⚠️ Photo not found: {student_photo_path}")
#             continue
#
#         try:
#             stu_img = face_recognition.load_image_file(student_photo_path)
#             stu_encodings = face_recognition.face_encodings(stu_img)
#             if not stu_encodings:
#                 continue
#
#             match = face_recognition.compare_faces([stu_encodings[0]], frame_encoding, tolerance=0.5)
#             if match[0]:
#                 print(f"✅ Match found: Student ID {student['id']}")
#                 return student["id"]
#         except Exception as e:
#             print("❌ Error processing student photo:", e)
#
#     return None
#
# # ============================
# # Video Summarizer
# # ============================
# def summarize_video(video_path, frame_skip=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     captions = []
#     db = Database()  # DB connection
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         cv2.imshow("Video", frame)
#
#         if frame_count % frame_skip == 0:
#             caption = generate_caption(frame)
#             captions.append(caption)
#             print(f"[Frame {frame_count}] Caption: {caption}")
#
#             if is_violent_caption(caption):
#                 print("🚨 Violence Detected! Saving to Database...")
#
#                 # Save violence frame
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 filepath = os.path.join(MEDIA_DIR, filename)
#                 cv2.imwrite(filepath, frame)
#
#                 # Insert into violence table
#                 qry1 = f"""
#                     INSERT INTO myapp_violence (date, time, photo)
#                     VALUES (CURDATE(), CURTIME(), '/media/{filename}')
#                 """
#                 violence_id = db.insert(qry1)
#
#                 # Try to match with student
#                 student_id = match_student(filepath, db)
#
#                 if student_id:
#                     qry2 = f"""
#                         INSERT INTO myapp_violencehub (action, STUDENT_id, VIOLENCE_id)
#                         VALUES ('pending', '{student_id}', '{violence_id}')
#                     """
#                     db.insert(qry2)
#                     print(f"📝 Violence linked to student {student_id}")
#                 else:
#                     print("❌ No student match found")
#
#         frame_count += 1
#
#         # Quit with 'q'
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     if not captions:
#         return "No captions generated"
#
#     # Simple summary: pick most frequent caption
#     return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)
#
# # ============================
# # Run
# # ============================
# if __name__ == "__main__":
#     video_file = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\video1.mp4"
#     try:
#         summary = summarize_video(video_file, frame_skip=30)
#         print("\n=== Final Video Caption ===")
#         print(summary)
#     except Exception as e:
#         print("🔥 Error inside summarize_video():", e)

# import cv2
# import numpy as np
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import face_recognition
# import os
# from datetime import datetime
# from DBConnection import Database  # your DB connection class
#
# # ============================
# # Load BLIP Model (LOCAL PATH)
# # ============================
# local_model_path = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\Salesforce"
#
# processor = BlipProcessor.from_pretrained(local_model_path)
# blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)
#
# # ============================
# # Paths
# # ============================
# BASE_DIR = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection web\violencedetection"
# MEDIA_DIR = os.path.join(BASE_DIR, "media")
#
# # ============================
# # Violence Keywords
# # ============================
# VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]
#
# # ============================
# # Caption Generator
# # ============================
# def generate_caption(frame):
#     pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     inputs = processor(pil_image, return_tensors="pt")
#     output = blip_model.generate(**inputs, max_new_tokens=30)
#     caption = processor.decode(output[0], skip_special_tokens=True)
#     return caption.lower()  # lowercase for easy matching
#
# def is_violent_caption(caption):
#     return any(word in caption for word in VIOLENCE_KEYWORDS)
#
# # ============================
# # Face Matching (MULTIPLE STUDENTS)
# # ============================
# def match_students(frame_path, db):
#     """Match ALL student faces in a violence frame"""
#     matched_students = []
#
#     try:
#         frame_img = face_recognition.load_image_file(frame_path)
#         frame_encodings = face_recognition.face_encodings(frame_img)
#
#         if not frame_encodings:
#             return []
#     except Exception as e:
#         print("❌ Error encoding frame:", e)
#         return []
#
#     students = db.select("SELECT id, photo FROM myapp_student")
#
#     for frame_encoding in frame_encodings:  # check each detected face
#         for student in students:
#             db_photo = student["photo"]  # stored like "/media/xxx.jpg"
#             student_photo_path = os.path.join(BASE_DIR, db_photo.strip("/"))
#
#             if not os.path.exists(student_photo_path):
#                 print(f"⚠️ Photo not found: {student_photo_path}")
#                 continue
#
#             try:
#                 stu_img = face_recognition.load_image_file(student_photo_path)
#                 stu_encodings = face_recognition.face_encodings(stu_img)
#                 if not stu_encodings:
#                     continue
#
#                 match = face_recognition.compare_faces([stu_encodings[0]], frame_encoding, tolerance=0.5)
#                 if match[0]:
#                     if student["id"] not in matched_students:
#                         matched_students.append(student["id"])
#                         print(f"✅ Match found: Student ID {student['id']}")
#             except Exception as e:
#                 print("❌ Error processing student photo:", e)
#
#     return matched_students
#
# # ============================
# # Video Summarizer
# # ============================
# def summarize_video(video_path, frame_skip=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     captions = []
#     db = Database()  # DB connection
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         cv2.imshow("Video", frame)
#
#         if frame_count % frame_skip == 0:
#             caption = generate_caption(frame)
#             captions.append(caption)
#             print(f"[Frame {frame_count}] Caption: {caption}")
#
#             if is_violent_caption(caption):
#                 print("🚨 Violence Detected! Saving to Database...")
#
#                 # Save violence frame
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 filepath = os.path.join(MEDIA_DIR, filename)
#                 cv2.imwrite(filepath, frame)
#
#                 # Insert into violence table
#                 qry1 = f"""
#                     INSERT INTO myapp_violence (date, time, photo)
#                     VALUES (CURDATE(), CURTIME(), '/media/{filename}')
#                 """
#                 violence_id = db.insert(qry1)
#
#                 # Match ALL students in the frame
#                 student_ids = match_students(filepath, db)
#
#                 if student_ids:
#                     for sid in student_ids:
#                         qry2 = f"""
#                             INSERT INTO myapp_violencehub (action, STUDENT_id, VIOLENCE_id)
#                             VALUES ('pending', '{sid}', '{violence_id}')
#                         """
#                         db.insert(qry2)
#                         print(f"📝 Violence linked to student {sid}")
#                 else:
#                     print("❌ No student match found in this frame")
#
#         frame_count += 1
#
#         # Quit with 'q'
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     if not captions:
#         return "No captions generated"
#
#     # Simple summary: pick most frequent caption
#     return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)
#
# # ============================
# # Run
# # ============================
# if __name__ == "__main__":
#     video_file = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\video1.mp4"
#     try:
#         summary = summarize_video(video_file, frame_skip=30)
#         print("\n=== Final Video Caption ===")
#         print(summary)
#     except Exception as e:
#         print("🔥 Error inside summarize_video():", e)


# import cv2
# import numpy as np
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import face_recognition
# import os
# from datetime import datetime
# from DBConnection import Database  # your DB connection class
#
# # ============================
# # Load BLIP Model (LOCAL PATH)
# # ============================
# local_model_path = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\Salesforce"
#
# processor = BlipProcessor.from_pretrained(local_model_path)
# blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)
#
# # ============================
# # Paths
# # ============================
# BASE_DIR = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection web\violencedetection"
# MEDIA_DIR = os.path.join(BASE_DIR, "media")
#
# # ============================
# # Violence Keywords
# # ============================
# VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]
#
# # ============================
# # Caption Generator
# # ============================
# def generate_caption(frame):
#     pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     inputs = processor(pil_image, return_tensors="pt")
#     output = blip_model.generate(**inputs, max_new_tokens=30)
#     caption = processor.decode(output[0], skip_special_tokens=True)
#     return caption.lower()
#
# def is_violent_caption(caption):
#     return any(word in caption for word in VIOLENCE_KEYWORDS)
#
# # ============================
# # Face Matching (ONE TIME – pick main student)
# # ============================
# def find_student(frame_path, db):
#     """Find the first matching student in DB"""
#     try:
#         frame_img = face_recognition.load_image_file(frame_path)
#         frame_encodings = face_recognition.face_encodings(frame_img)
#         if not frame_encodings:
#             return None
#         frame_encoding = frame_encodings[0]
#     except Exception as e:
#         print("❌ Error encoding frame:", e)
#         return None
#
#     students = db.select("SELECT id, photo FROM myapp_student")
#
#     for student in students:
#         db_photo = student["photo"]
#         student_photo_path = os.path.join(BASE_DIR, db_photo.strip("/"))
#
#         if not os.path.exists(student_photo_path):
#             continue
#
#         try:
#             stu_img = face_recognition.load_image_file(student_photo_path)
#             stu_encodings = face_recognition.face_encodings(stu_img)
#             if not stu_encodings:
#                 continue
#
#             match = face_recognition.compare_faces([stu_encodings[0]], frame_encoding, tolerance=0.5)
#             if match[0]:
#                 print(f"✅ Student matched: {student['id']}")
#                 return student["id"]
#         except Exception as e:
#             print("❌ Error processing student photo:", e)
#
#     return None
#
# # ============================
# # Video Summarizer
# # ============================
# def summarize_video(video_path, frame_skip=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     captions = []
#     db = Database()  # DB connection
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         cv2.imshow("Video", frame)
#
#         if frame_count % frame_skip == 0:
#             caption = generate_caption(frame)
#             captions.append(caption)
#             print(f"[Frame {frame_count}] Caption: {caption}")
#
#             if is_violent_caption(caption):
#                 print("🚨 Violence Detected! Saving to Database...")
#
#                 # Save violence frame
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 filepath = os.path.join(MEDIA_DIR, filename)
#                 cv2.imwrite(filepath, frame)
#
#                 # Try to find student (once per violent frame)
#                 student_id = find_student(filepath, db)
#
#                 if student_id:
#                     # Insert into Violence (with student reference, NO photo)
#                     qry1 = f"""
#                         INSERT INTO myapp_violence (STUDENT_id, date, time)
#                         VALUES ('{student_id}', CURDATE(), CURTIME())
#                     """
#                     violence_id = db.insert(qry1)
#
#                     # Insert the fight frame into Violencehub (linked to Violence)
#                     qry2 = f"""
#                         INSERT INTO myapp_violencehub (VIOLENCE_id, action, photo)
#                         VALUES ('{violence_id}', 'pending', '/media/{filename}')
#                     """
#                     db.insert(qry2)
#
#                     print(f"📝 Violence record created for student {student_id}, fight frame saved.")
#                 else:
#                     print("❌ No student matched in this frame.")
#
#         frame_count += 1
#
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     if not captions:
#         return "No captions generated"
#
#     return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)
#
# # ============================
# # Run
# # ============================
# if __name__ == "__main__":
#     video_file = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection detection\violencedetection\video1.mp4"
#     try:
#         summary = summarize_video(video_file, frame_skip=30)
#         print("\n=== Final Video Caption ===")
#         print(summary)
#     except Exception as e:
#         print("🔥 Error inside summarize_video():", e)

# import cv2
# import numpy as np
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import face_recognition
# import os
# from datetime import datetime
# from DBConnection import Database  # your DB connection class
#
# # ============================
# # Load BLIP Model (LOCAL PATH)
# # ============================
# local_model_path = r"C:\Users\safam\Downloads\violencedetection-cam\violencedetection\Salesforce"
#
# processor = BlipProcessor.from_pretrained(local_model_path)
# blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)
#
# # ============================
# # Paths
# # ============================
# BASE_DIR = r"C:\Users\safam\Downloads\violencedetection\violencedetection"
# MEDIA_DIR = os.path.join(BASE_DIR, "media")
#
# # ============================
# # Violence Keywords
# # ============================
# VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]
#
# # ============================
# # Caption Generator
# # ============================
# def generate_caption(frame):
#     pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     inputs = processor(pil_image, return_tensors="pt")
#     output = blip_model.generate(**inputs, max_new_tokens=30)
#     caption = processor.decode(output[0], skip_special_tokens=True)
#     return caption.lower()
#
# def is_violent_caption(caption):
#     return any(word in caption for word in VIOLENCE_KEYWORDS)
#
# # ============================
# # Face Matching (Improved)
# # ============================
# def find_student(frame_path, db):
#     """Try to match any face in frame with DB students"""
#     try:
#         frame_img = face_recognition.load_image_file(frame_path)
#         frame_encodings = face_recognition.face_encodings(frame_img)
#         if not frame_encodings:
#             return None
#     except Exception as e:
#         print("❌ Error encoding frame:", e)
#         return None
#
#     students = db.select("SELECT id, photo FROM myapp_student")
#
#     for student in students:
#         db_photo = student["photo"]
#         student_photo_path = os.path.join(BASE_DIR, db_photo.strip("/"))
#         print(db_photo)
#
#         if not os.path.exists(student_photo_path):
#             continue
#
#         try:
#             stu_img = face_recognition.load_image_file(student_photo_path)
#             stu_encodings = face_recognition.face_encodings(stu_img)
#             if not stu_encodings:
#                 continue
#
#             # Compare each detected face in frame with student photo
#             for face_encoding in frame_encodings:
#                 match = face_recognition.compare_faces([stu_encodings[0]], face_encoding, tolerance=0.6)
#                 print(match)
#                 if match[0]:
#                     print(f"✅ Student matched: {student['id']}")
#                     return student["id"]
#         except Exception as e:
#             print("❌ Error processing student photo:", e)
#
#     return None
#
# # ============================
# # Video Summarizer
# # ============================
# def summarize_video(video_path, frame_skip=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     captions = []
#     db = Database()  # DB connection
#
#     student_id = None
#     violence_id = None  # Store only once
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         cv2.imshow("Video", frame)
#
#         if frame_count % frame_skip == 0:
#             caption = generate_caption(frame)
#             captions.append(caption)
#             print(f"[Frame {frame_count}] Caption: {caption}")
#
#             if is_violent_caption(caption):
#                 print("🚨 Violence Detected! Saving to Database...")
#
#                 # Save violence frame
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 filepath = os.path.join(MEDIA_DIR, filename)
#                 cv2.imwrite(filepath, frame)
#
#                 # STEP 1: First time → detect student and insert into Violence
#                 if student_id is None:
#                     student_id = find_student(filepath, db)
#                     print(student_id)
#
#                     if student_id:
#                         qry1 = f"""
#                             INSERT INTO myapp_violence (STUDENT_id, date, time)
#                             VALUES ('{student_id}', CURDATE(), CURTIME())
#                         """
#                         violence_id = db.insert(qry1)
#                         print(f"📝 Violence record created for student {student_id}")
#                     else:
#                         print("❌ No student matched. Skipping frame save.")
#                         continue  # skip saving until student is matched
#
#                 # STEP 2: Already matched → keep saving fight frames
#                 if violence_id:
#                     qry2 = f"""
#                         INSERT INTO myapp_violencehub (VIOLENCE_id, action, photo)
#                         VALUES ('{violence_id}', 'pending', '/media/{filename}')
#                     """
#                     db.insert(qry2)
#                     print(f"📸 Fight frame saved for student {student_id}")
#
#         frame_count += 1
#
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     if not captions:
#         return "No captions generated"
#
#     return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)
#
# # ============================
# # Run
# # ============================
# if __name__ == "__main__":
#     video_file = r"C:\Users\safam\Downloads\violencedetection-cam\violencedetection\video1.mp4"
#     try:
#         summary = summarize_video(video_file, frame_skip=30)
#         print("\n=== Final Video Caption ===")
#         print(summary)
#     except Exception as e:
#         print("🔥 Error inside summarize_video():", e)


# import cv2
# import numpy as np
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import face_recognition
# import os
# from datetime import datetime
# from DBConnection import Database  # your DB connection class
#
# # ============================
# # Load BLIP Model (LOCAL PATH)
# # ============================
# local_model_path = r"C:\Users\safam\Downloads\violencedetection-cam\violencedetection\Salesforce"
#
# processor = BlipProcessor.from_pretrained(local_model_path)
# blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)
#
# # ============================
# # Paths
# # ============================
# BASE_DIR = r"C:\Users\safam\Downloads\violencedetection\violencedetection"
# # BASE_DIR = r"C:\Users\amaya\Desktop\VIOLENCE DETECTION\VIOLENCE DETECTION\violencedetection web\violencedetection"
# MEDIA_DIR = os.path.join(BASE_DIR, "media")
#
# # ============================
# # Violence Keywords
# # ============================
# VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]
#
# # ============================
# # Caption Generator
# # ============================
# def generate_caption(frame):
#     pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     inputs = processor(pil_image, return_tensors="pt")
#     output = blip_model.generate(**inputs, max_new_tokens=30)
#     caption = processor.decode(output[0], skip_special_tokens=True)
#     return caption.lower()
#
# def is_violent_caption(caption):
#     return any(word in caption for word in VIOLENCE_KEYWORDS)
#
# # ============================
# # Face Matching (one-time use)
# # ============================
# def find_student(frame_path, db):
#     """Try to match any face in frame with DB students"""
#     try:
#         frame_img = face_recognition.load_image_file(frame_path)
#         frame_encodings = face_recognition.face_encodings(frame_img)
#         if not frame_encodings:
#             return None
#     except Exception as e:
#         print("❌ Error encoding frame:", e)
#         return None
#
#     students = db.select("SELECT id, photo FROM myapp_student")
#
#     for student in students:
#         db_photo = student["photo"]  # stored like "/media/student1.jpg"
#         student_photo_path = os.path.join(BASE_DIR, db_photo.strip("/"))
#
#         if not os.path.exists(student_photo_path):
#             continue
#
#         try:
#             stu_img = face_recognition.load_image_file(student_photo_path)
#             stu_encodings = face_recognition.face_encodings(stu_img)
#             if not stu_encodings:
#                 continue
#
#             for face_encoding in frame_encodings:
#                 match = face_recognition.compare_faces([stu_encodings[0]], face_encoding, tolerance=0.6)
#                 if match[0]:
#                     print(f"✅ Student matched: {student['id']}")
#                     return student["id"]
#         except Exception as e:
#             print("❌ Error processing student photo:", e)
#
#     return None
#
# # ============================
# # Video Summarizer
# # ============================
# def summarize_video(video_path, frame_skip=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     captions = []
#     db = Database()  # DB connection
#
#     student_id = None
#     violence_id = None  # only one per video/session
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         cv2.imshow("Video", frame)
#
#         if frame_count % frame_skip == 0:
#             caption = generate_caption(frame)
#             captions.append(caption)
#             print(f"[Frame {frame_count}] Caption: {caption}")
#
#             if is_violent_caption(caption):
#                 print("🚨 Violence Detected! Saving to Database...")
#
#                 # Save frame in media folder
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 filepath = os.path.join(MEDIA_DIR, filename)
#                 cv2.imwrite(filepath, frame)
#
#                 # STEP 1: First time → detect student & create violence record
#                 if violence_id is None:
#                     student_id = find_student(filepath, db)
#                     print(student_id,"==============")
#
#                     if student_id:
#                         qry1 = f"""
#                             INSERT INTO myapp_violence (STUDENT_id, date, time)
#                             VALUES ('{student_id}', CURDATE(), CURTIME())
#                         """
#                         violence_id = db.insert(qry1)
#                         print(f"📝 Violence record created for student {student_id}")
#                     else:
#                         print("❌ No student matched. Violence not stored.")
#                         continue  # Skip until a student is identified
#
#                 # STEP 2: If violence already identified → keep saving frames
#                 if violence_id:
#                     qry2 = f"""
#                         INSERT INTO myapp_violencehub (VIOLENCE_id, action, photo)
#                         VALUES ('{violence_id}', 'pending', '/media/{filename}')
#                     """
#                     db.insert(qry2)
#                     print(f"📸 Frame saved under violence_id {violence_id}")
#
#         frame_count += 1
#
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     if not captions:
#         return "No captions generated"
#
#     return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)
#
# # ============================
# # Run
# # ============================
# if __name__ == "__main__":
#     video_file = r"C:\Users\safam\Downloads\violencedetection-cam\violencedetection\video1.mp4"
#     try:
#         summary = summarize_video(video_file, frame_skip=30)
#         print("\n=== Final Video Caption ===")
#         print(summary)
#     except Exception as e:
#         print("🔥 Error inside summarize_video():", e)

import cv2
import numpy as np
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import face_recognition
import os
from datetime import datetime
from DBConnection import Database  # Your custom DB connection class

# ============================
# Load BLIP Model (LOCAL PATH)
# ============================
local_model_path = r"C:\Users\safam\Downloads\violencedetection-cam\violencedetection\Salesforce"
processor = BlipProcessor.from_pretrained(local_model_path)
blip_model = BlipForConditionalGeneration.from_pretrained(local_model_path)

# ============================
# Paths
# ============================
BASE_DIR = r"C:\Users\safam\Downloads\violencedetection\violencedetection"
MEDIA_DIR = os.path.join(BASE_DIR, "media")

# ============================
# Violence Keywords
# ============================
VIOLENCE_KEYWORDS = ["fight", "fighting", "attack", "violence", "punch", "hit", "kicking", "beating"]

# ============================
# Caption Generator
# ============================
def generate_caption(frame):
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    inputs = processor(pil_image, return_tensors="pt")
    output = blip_model.generate(**inputs, max_new_tokens=30)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption.lower()

def is_violent_caption(caption):
    return any(word in caption for word in VIOLENCE_KEYWORDS)

# ============================
# Face Matching
# ============================
def find_student(frame_path, db):
    """Try to match any face in frame with DB students"""
    try:
        print("🖼️ Checking frame:", frame_path)
        frame_img = face_recognition.load_image_file(frame_path)
        frame_encodings = face_recognition.face_encodings(frame_img)
        print(f"📷 Found {len(frame_encodings)} face(s) in frame")

        if not frame_encodings:
            print("❌ No face found in frame.")
            return None
    except Exception as e:
        print("❌ Error encoding frame:", e)
        return None

    students = db.select("SELECT id, photo FROM myapp_student")

    for student in students:
        db_photo = student["photo"]  # stored like "/media/student1.jpg"
        student_photo_path = os.path.join(BASE_DIR, db_photo.strip("/"))

        print("➡️ Checking student photo:", student_photo_path)

        if not os.path.exists(student_photo_path):
            print("⚠️ Student photo does not exist:", student_photo_path)
            continue

        try:
            stu_img = face_recognition.load_image_file(student_photo_path)
            stu_encodings = face_recognition.face_encodings(stu_img)
            print(f"🧑 Student ID {student['id']}: {len(stu_encodings)} face(s) in student photo")

            if not stu_encodings:
                print("❌ No face found in student photo.")
                continue

            for face_encoding in frame_encodings:
                match = face_recognition.compare_faces([stu_encodings[0]], face_encoding, tolerance=0.6)
                print(f"🔍 Comparing with student {student['id']} → Match: {match[0]}")
                if match[0]:
                    print(f"✅ Student matched: {student['id']}")
                    return student["id"]
        except Exception as e:
            print("❌ Error processing student photo:", e)

    print("❌ No matching student found.")
    return None

# ============================
# Video Summarizer
# ============================
def summarize_video(video_path, frame_skip=30):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    captions = []
    db = Database()

    student_id = None
    violence_id = None

    print("🎥 Starting video analysis:", video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video", frame)

        if frame_count % frame_skip == 0:
            print(f"\n🧠 Analyzing Frame {frame_count}...")
            caption = generate_caption(frame)
            captions.append(caption)
            print(f"[Frame {frame_count}] Caption: {caption}")

            if is_violent_caption(caption):
                print("🚨 Violence Detected! Saving frame...")

                filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
                filepath = os.path.join(MEDIA_DIR, filename)
                cv2.imwrite(filepath, frame)
                print("📸 Frame saved to:", filepath)

                # First detection
                if violence_id is None:
                    student_id = find_student(filepath, db)

                    if student_id:
                        qry1 = f"""
                            INSERT INTO myapp_violence (STUDENT_id, date, time,action)
                            VALUES ('{student_id}', CURDATE(), CURTIME(),'pending')
                        """
                        violence_id = db.insert(qry1)
                        print(f"📝 Violence record created for student {student_id}")
                    else:
                        print("❌ No student matched. Violence not stored.")
                        continue

                # Add to violencehub
                if violence_id:
                    qry2 = f"""
                        INSERT INTO myapp_violencehub (VIOLENCE_id, action, photo)
                        VALUES ('{violence_id}', 'pending', '/media/{filename}')
                    """
                    db.insert(qry2)
                    print(f"📁 Frame linked to violence ID {violence_id}")

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not captions:
        return "No captions generated"
    return captions[0] if len(captions) == 1 else max(set(captions), key=captions.count)

# ============================
# Run Script
# ============================
if __name__ == "__main__":
    video_file = r"C:\Users\safam\Downloads\violencedetection-cam\violencedetection\video1.mp4"
    try:
        summary = summarize_video(video_file, frame_skip=30)
        print("\n=== Final Video Caption Summary ===")
        print(summary)
    except Exception as e:
        print("🔥 Error inside summarize_video():", e)
