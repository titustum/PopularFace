from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os, json
import uuid
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/popularface'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a model for the database table
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID as primary key
    name = db.Column(db.String(100))
    image = db.Column(db.String(100), unique=True)  # Unique filename for image
    about = db.Column(db.Text) 

# Route to upload details
@app.route('/', methods=['GET', 'POST'])
def upload_details():
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']
        image = request.files['image']

        # Generate a UUID for the user
        user_id = str(uuid.uuid4())
        # Generate a unique filename for the image
        image_filename = str(uuid.uuid4())

        # Make the filename secure
        filename = secure_filename(image_filename)

        # Get the file extension
        _, image_ext = os.path.splitext(image.filename)

        # Save the image to the file system
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + image_ext))

        # Create a new user instance
        new_user = User(id=user_id, name=name, about=about, image=filename + image_ext)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

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


@app.route('/checkface', methods=['GET'])
def check_image():
    return render_template('upload_to_check.html')

@app.route('/checkface/result', methods=['GET'])
def check_face_result():
    return render_template('check_face_result.html')



from Utility import check_face

@app.route('/checkface', methods=['POST'])
def checkface():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filepath = os.path.join('static/unknown/', file.filename)
    file.save(filepath)

    users = User.query.all()
    results = check_face(filepath, users)
    os.remove(filepath)  # Remove the uploaded file after checking

    return jsonify(results)


if __name__ == '__main__': 
    with app.app_context():
        # Create the database tables before running the app
        db.create_all()
    app.run(debug=True)
