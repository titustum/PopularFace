import face_recognition
from datetime import datetime, timezone 
import pickle
import os
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
load_dotenv()

# Assuming you've already defined your User model
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True)
    name = Column(String(200))
    image = Column(String(200), unique=True)
    occupation = Column(String(200), unique=True)
    about = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

# Configure SQLAlchemy engine to connect to MySQL
# Replace 'mysql://username:password@hostname:port/database_name' with your MySQL connection details
engine = create_engine(os.getenv("DATABASE_URL"))

# Create database tables if they don't exist
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def fetch_users_from_database():
    return session.query(User).order_by(User.created_at).all()

# fetch_specified_users
def fetch_specified_users(specified_ids=[]):
    return session.query(User).filter(User.id.in_(specified_ids)).order_by(User.created_at).all()

def create_face_encodings():
    known_face_encodings = []
    users = fetch_users_from_database()
    for user in users:
        image_path = f'static/uploads/{user.image}'
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append([user.id,face_encoding])

    with open('data/face_encodings.pkl', 'wb') as file:
        # print(known_face_encodings)
        pickle.dump(known_face_encodings, file)
 

def check_face(unknown_image_path):
    try:
        # Load known face encodings from pickle file
        with open('data/face_encodings.pkl', 'rb') as file:
            encodings = pickle.load(file)

        user_ids = []
        known_face_encodings = []

        for user_id, known_face_encoding in encodings:
            user_ids.append(user_id)
            known_face_encodings.append(known_face_encoding)

        # Load unknown image
        unknown_image = face_recognition.load_image_file(unknown_image_path)

        # Compute face encoding for unknown image
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        # Calculate distances between unknown face encoding and known face encodings
        distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)

        user_id_distances = []

        for id, distance in zip(user_ids, distances):
            user_id_distances.append([id, distance])

        # print(user_id_distances)
        
        results = []

        counter = 0

        # Fetch specified users from the database
        users = fetch_specified_users(user_ids)

        for user in users:
            if user.id in user_ids:
                percentage = round(((1 - distances[counter]) * 100), 2)
                percentage = max(0, min(percentage, 100))
                user.about = user.about if len(user.about) <= 500 else user.about[:300] + "..."
                results.append({
                     "id": user.id,
                    "image": user.image,
                    "name": user.name,
                    "occupation": user.occupation,
                    "about": user.about,
                    "match": f"{percentage}%"  
                })
                counter += 1

        results.sort(key=lambda x: float(x['match'].strip('%')), reverse=True)  # Sort based on match percentage
        return results[:5]
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# Fetch users from database
# users = fetch_users_from_database()
# create_face_encodings() # Uncomment this if you haven't already created face encodings

# results = check_face("images/unknown/4.webp", users)

# print(json.dumps(results))

# check_face("static/unknown/20240604-232156_download (10).jpg")