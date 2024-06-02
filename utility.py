import face_recognition
import os
import pickle

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



def create_face_encodings():
    known_face_encodings = []
    for image_path in os.listdir('images/known/'):
        image  = face_recognition.load_image_file(f"images/known/{image_path}")
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding) 

    #print(face_encodings)
    
    # Save face encodings in pickle file 
    with open('data/face_encodings.pkl', 'wb') as file: 
        pickle.dump(known_face_encodings, file) 





def check_face(unknown_image_path):
    with open('data/face_encodings.pkl', 'rb') as file: 
        known_face_encodings = pickle.load(file)
        unknown_image  = face_recognition.load_image_file(unknown_image_path)
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        #print(unknown_face_encoding)

        # result = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance=0.6)
        return face_recognition.face_distance(known_face_encodings, unknown_face_encoding)

    

# create_face_encodings()

result = check_face("images/unknown/2.jpg")
# print(result)

results = []

for user, distance in zip(users, result):
    percentage = round(((1-distance)*100), 2)
    percentage = max(0, min(percentage, 100))
    results.append({
        "name":user.name,
        "description":user.description,
        "match": f"{percentage}%"
    })

results.sort(key = lambda x: x['match'], reverse=True)
print(results)