## ope-ope

This project is a simple web application built with Flask that allows users to upload images of One Piece card game cards and get information about them. It uses Google's Gemini API to extract text from the images and then searches through a database of card information to find the matching card.

### Installation

1. **Install Poetry:**
   ```bash
   pip install poetry
   ```
2. **Install Dependencies:**
   ```bash
   poetry install
   ```
3. **Create a .env file:**
   ```bash
   cp .env.example .env
   ```
4. **Set your Gemini API key in the .env file:**
   ```bash
   GEMINI_API_KEY=YOUR_API_KEY
   ```

### Usage

1. **Run the application:**
   ```bash
   poetry run python app.py
   ```
2. **Access the application in your browser:**
   ```bash
   http://127.0.0.1:5000/
   ```
3. **Upload an image:**
   - The application will redirect you to the `/images` page, where you can see a list of uploaded images.
   - Click the "Upload Image" button and select the image you want to upload.
   - The image will be uploaded and displayed on the page.
4. **Recognize a card:**
   - The application will automatically try to recognize the card in the uploaded image and will display the results as a JSON object.
   - You can also access the extracted data and search results as a JSON file in the `/data/processing_output` directory.

### Files

- **.env:** Environment variables, including your Gemini API key.
- **.gitignore:** Ignores specific files and directories from version control.
- **README.md:** This file.
- **app.py:** Flask application code.
- **data/extracted_data.json:** JSON file storing the extracted text from a test image.
- **data/merry_cards_data_dump.json:** JSON file containing card data from the One Piece card game.
- **data/processing_output/photo_1729646964902.json:** Example JSON file storing extracted data and search results for a specific image.
- **poetry.lock:** Poetry's lock file, defining the exact versions of dependencies.
- **pyproject.toml:** Poetry's configuration file, defining the project's dependencies and build settings.
- **send_tester.py:** A script to test the image upload functionality.
- **services/card_recognition.py:** Contains code for card recognition using Google's Gemini API.
- **templates/images.html:** HTML template for the image display page.

### Note

- The `create_cache()` function in `services/card_recognition.py` is used to create a cached Gemini model with the card data from the `data/merry_cards_data_dump.json` file. You only need to run this function once to create the cache. The cache will be valid for 1 hour.
- The project uses a basic authentication scheme for the image upload endpoint. You can change the username and password in the `app.py` file.
- You can modify the code to improve card recognition accuracy and expand the database of card information.