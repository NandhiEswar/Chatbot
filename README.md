# Chatbot Using Hugging Face, Selenium, Flask, and React

This project implements a chatbot that extracts data from the web and summarizes it using the Hugging Face model. The bot scrapes search results from Google using Selenium and provides both a summarized text and named entity recognition (NER) using the Hugging Face transformers pipeline. The backend is built with Flask, while the frontend is powered by React.

## Table of Contents

- [Installation](#installation)
- [Backend](#backend)
  - [Flask Setup](#flask-setup)
  - [Selenium Setup](#selenium-setup)
  - [Hugging Face Integration](#hugging-face-integration)
- [Frontend](#frontend)
  - [React Setup](#react-setup)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to get the project running on your local machine.

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/NandhiEswar/Chatbot.git
   cd Chatbot
Create a Python virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required dependencies:
pip install -r requirements.txt
Dependencies in requirements.txt:

Flask
Flask-Cors
selenium
transformers
torch
huggingface_hub
webdriver_manager
Download and install ChromeDriver (for Selenium) using webdriver_manager, or install it manually.
Set up Hugging Face authentication:
Run huggingface-cli login and follow the instructions to authenticate.
Start the Flask server:
python app.py
Your Flask backend should now be running on http://127.0.0.1:5000.
Frontend Setup (React)
Navigate to the frontend directory:
cd frontend
Install the required npm dependencies:
npm install
Start the React development server:
npm start
Your React frontend should now be running on http://localhost:3000.
How It Works

Backend
Selenium is used to perform a Google search based on the query provided by the user and extract data from the resulting pages.
Hugging Face Transformers (specifically, BART) is used to summarize the extracted data.
Named Entity Recognition (NER) is performed to identify entities like people, organizations, locations, etc.
Frontend
The frontend is built using React, which allows users to input a query, send it to the Flask backend, and display the summarized response along with any recognized entities.
Usage

Type a query (e.g., "Python programming") in the input field in the React app.
The query is sent to the Flask backend, which scrapes search results from Google using Selenium.
The backend then summarizes the extracted content and performs NER.
The frontend displays the summary and recognized entities to the user.
Example Interaction

User: "Python programming"
Bot: Summarized text about Python programming and named entities like "Python" and "programming".
Contributing

If you'd like to contribute to this project:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add feature').
Push to your branch (git push origin feature-branch).
Create a pull request.
