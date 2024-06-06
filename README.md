# PopularFace.ai

Welcome to PopularFace.ai! This is a web-based facial recognition system that utilizes the `face_recognition` Python library and Flask framework. PopularFace.ai is designed to detect popular individuals such as politicians, sportspeople, and journalists, providing basic information about them.

## Features

- **Facial Recognition**: Upload an image of a person, and PopularFace.ai will identify if they are a popular figure.
- **Basic Information**: Receive basic information about the recognized individual, including their name, occupation, and a brief description.
- **Image Comparison**: View the uploaded image alongside the recognized individual's photo for easy comparison.
- **User Feedback**: Users can provide feedback on the recognition results using the like and dislike buttons.
- **Social Sharing**: Share the recognition results with others using the share button.

## How to Use

1. **Upload Image**: Visit the PopularFace.ai website and upload an image of the person you want to identify.
2. **Recognition Process**: The system will process the uploaded image and compare it against a database of popular figures.
3. **Results Display**: Once the recognition process is complete, PopularFace.ai will display the recognized individual's information, including their name, occupation, and a brief description. Additionally, both the recognized individual's photo and the uploaded photo will be displayed for comparison.
4. **Feedback and Sharing**: Users can provide feedback on the recognition results using the like and dislike buttons. They can also share the results with others using the share button.

## Getting Started

To run PopularFace.ai locally, follow these steps:

1. **Clone Repository**: Clone the PopularFace.ai repository to your local machine.
   ```
   git clone https://github.com/titustum/PopularFace.git
   ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using pip.
   ```
   cd PopularFace
   pip install -r requirements.txt
   ```

3. **Run the Application**: Start the Flask server to run the application.
   ```
   python app.py
   ```

4. **Access PopularFace.ai**: Open a web browser and go to `http://localhost:5000` to access the PopularFace.ai web interface.

## Contributing

Contributions to PopularFace.ai are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## Credits

PopularFace.ai is built using the `face_recognition` Python library and the Flask framework. Special thanks to the developers of these tools and libraries.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.