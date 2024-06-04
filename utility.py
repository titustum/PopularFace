import face_recognition
import json
import pickle
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Assuming you've already defined your User model
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(String(36), primary_key=True)
    name = Column(String(100))
    image = Column(String(100), unique=True)
    about = Column(Text)

# Configure SQLAlchemy engine to connect to MySQL
# Replace 'mysql://username:password@hostname:port/database_name' with your MySQL connection details
engine = create_engine('mysql://root@localhost:3306/popularface')

# Create database tables if they don't exist
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def fetch_users_from_database():
    return session.query(User).all()

def create_face_encodings(users):
    known_face_encodings = []
    for user in users:
        image_path = f'static/uploads/{user.image}'
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)

    with open('data/face_encodings.pkl', 'wb') as file:
        pickle.dump(known_face_encodings, file)

def check_face(unknown_image_path, users=[]):
    with open('data/face_encodings.pkl', 'rb') as file:
        known_face_encodings = pickle.load(file)
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        distances =  face_recognition.face_distance(known_face_encodings, unknown_face_encoding)
        
        results = []
        for user, distance in zip(users, distances):
            percentage = round(((1 - distance) * 100), 2)
            percentage = max(0, min(percentage, 100))
            results.append({
                "id": user.id,
                "image": user.image,
                "name": user.name,
                "about": user.about,
                "match": f"{percentage}%"
            })

        results.sort(key=lambda x: float(x['match'].strip('%')), reverse=True)  # Sort based on match percentage
        return results[:5]

# Fetch users from database
# users = fetch_users_from_database()
# create_face_encodings(users) # Uncomment this if you haven't already created face encodings

# results = check_face("images/unknown/4.webp", users)

# print(json.dumps(results))
