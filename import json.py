import json
from deepface import DeepFace
r=DeepFace.verify(img1_path="C:/Users/NHUT HIEU/Downloads/QLNS/hinhchup/captured_image_20240521_133306.jpg", img2_path="C:/Users/NHUT HIEU/Downloads/QLNS/hinh/nhuthieu_000378.jpg", model_name="Facenet512")

print(json.dumps(r, indent=2))