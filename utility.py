import face_recognition
import os

class User:
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description


users = [
    User("Njuguna Ndung’u","National Treasury and Planning"),
    User("Dr. William Samoei Ruto, C.G.H", "The President of the Republic of Kenya and Commander-in-Chief of the Defence Forces"),
    User("Hon. Rigathi Gachagua", "The Deputy President of the Republic of Kenya"),
    User("Mr. Musalia Mudavadi", "Prime Cabinet Secretary and Foreign Affairs"),
    User("Prof. Kithure Kindiki", "Interior and National Administration"),
]

 
known_face_encodings = []

for image_path in os.listdir('images/known/'):
    image  = face_recognition.load_image_file(f"images/known/{image_path}")
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding) 

#print(face_encodings)


unknown_image  = face_recognition.load_image_file("images/unknown/unknown.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[1]

#print(unknown_face_encoding)


# result = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance=0.6)
result = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)

print(result)
