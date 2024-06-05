from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy 
import os
from datetime import datetime, timezone 
import uuid
from werkzeug.utils import secure_filename

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") 

# Configure the MySQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/popularface'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a model for the database table

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    name = db.Column(db.String(200), unique=True)
    image = db.Column(db.String(200))
    occupation = db.Column(db.String(200))
    about = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))




# Route to recognize faces
@app.route('/', methods=['GET'])
def check_image():
    return render_template('index.html')


# Route to upload details
@app.route('/upload', methods=['GET', 'POST'])
def upload_details():
    if request.method == 'POST':
        name = request.form['name']
        occupation = request.form['occupation']
        about = request.form['about']
        image = request.files['image']

        # Generate a UUID for the user
        user_uid = str(uuid.uuid4())
        # Generate a unique filename for the image
        image_filename = str(uuid.uuid4())

        # Make the filename secure
        filename = secure_filename(image_filename)

        # Get the file extension
        _, image_ext = os.path.splitext(image.filename)

        # Save the image to the file system
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + image_ext))

        # Create a new user instance
        new_user = User(uuid=user_uid, name=name, about=about, occupation=occupation, image=filename + image_ext)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f"{name} user has been added successfully!")
        return redirect(url_for('upload_details'))
    
    return render_template('upload.html')


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_details = [{"id": user.id, "name": user.name, "image": url_for('static', filename='images/' + user.image), "description": user.about } for user in users]
    return jsonify(user_details)


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_detail = {"name": user.name, "image": url_for('static', filename='images/' + user.image), "description": user.about}
    return jsonify(user_detail)


from utility import check_face, create_face_encodings
import time

@app.route('/checkface', methods=['POST'])
def checkface():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Remove all available images in the folder
    folder_path = 'static/unknown/'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Generate a unique filename based on the current time
    current_time = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{current_time}_{file.filename}"

    filepath = os.path.join('static/unknown/', filename)
    file.save(filepath)

    # users = User.query.order_by(User.created_at).all()
    results = check_face(filepath) 

    return jsonify({"original_image": filepath, "results": results})




@app.route('/train', methods=['GET'])
def train_system():
    create_face_encodings()
    return "Done, System is now trained!"


if __name__ == '__main__': 
    with app.app_context():
        # Create the database tables before running the app
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
