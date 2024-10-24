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

### Features

- Image upload functionality.
- Card recognition using Google's Gemini API.
- Search for matching cards in a database.
- Display of card information in a JSON format.

### Running with Docker

1. **Build the Docker image:**
   ```bash
   docker-compose build
   ```
2. **Start the application:**
   ```bash
   docker-compose up -d
   ```
3. **Access the application in your browser:**
   ```bash
   http://127.0.0.1:5000/
   ```
