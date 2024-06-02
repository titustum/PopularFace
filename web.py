from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/popularface'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

import uuid
from werkzeug.utils import secure_filename

# Define a model for the database table
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID as primary key
    name = db.Column(db.String(100))
    image_uuid = db.Column(db.String(36))  # UUID as string
    image_ext = db.Column(db.String(10))    # File extension
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
        # Generate a UUID for the image filename
        image_uuid = str(uuid.uuid4())
        # Get the file extension
        image_ext = image.filename.rsplit('.', 1)[1]

        # Make the filename secure
        filename = secure_filename(image_uuid + '.' + image_ext)

        # Save the image to the file system
        image.save('static/images/' + filename)

        # Create a new user instance
        new_user = User(id=user_id, name=name, about=about, image_uuid=image_uuid, image_ext=image_ext)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('upload_details'))
    return render_template('upload.html')


if __name__ == '__main__': 
    with app.app_context():
        # Create the database tables before running the app
        db.create_all()
    app.run(debug=True)

