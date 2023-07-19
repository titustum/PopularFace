import os
import json
import pickle
import face_recognition


names = [
    "HON. MEJJADONK, BENJAMIN GATHIRU",
    "HON. (AMB.) LANGAT BENJAMIN KIPKIRUI",
    "HON. (DR.) GICHUKI EDWIN MUGO",
    "HON. (DR.) JACKSON KIPKEMOI KOSGEI",
    "HON. (DR.) PUKOSE ROBERT",
    "HON. (ENG.) NZAMBIA KITHUA THUDDEUS",
    "HON. ABDI ALI ABDI",
    "HON. ABDI KHAMIS CHOME",
    "HON. ABDI, YUSUF HASSAN",
]

images = [
    "mini_gathiru_cropped_1.jpg",
    "LANGAT_BENJAMIN_KIPKIRUI.jpg",
    "Gichuki_Edwin_Mugo.jpg",
    "Kosgei_Jackson_Kipkemoi.jpg",
    "mini_cropped_Pukose.jpg",
    "NZAMBIA KITHUA THUDDEUS.jpg",
    "abdi_ali_abdi.jpg",
    "Abdi_Khamis_Chome2.jpg",
    "yusuf_hassan.jpg"
]


encodings = []
for im in images:
    image = face_recognition.load_image_file(img)
    
    encodings.append()
