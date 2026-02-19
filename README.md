# Fake Job Detector Version 0.1

## Overview

Fake Job Detector is a prototype application designed to help users identify potentially fraudulent job postings. It consists of a Chrome extension for the user interface and a Python backend server that uses a machine learning model to analyze job descriptions.

## Project Structure

```text
V1/
├── extension/                  # Chrome Extension source code
│   ├── icon.png                # Extension icon
│   ├── manifest.json           # Extension configuration
│   ├── popup.css               # Styles for the popup UI
│   ├── popup.html              # HTML layout for the popup UI
│   └── popup.js                # Extension logic and server communication
│
└── server/                     # Backend Flask Server
    ├── app.py                  # Main Flask application entry point
    ├── requirements.txt        # Python dependencies
    ├── train_model.py          # Script to train the ML model
    └── model/                  # Directory for ML model artifacts
        └── basic_model.pkl     # Serialized machine learning model
```

## detailed Components

### 1. Chrome Extension (`extension/`)

The extension provides the frontend interface for the user.

- **manifest.json**: Defines the extension's permissions and entry points.
- **popup.html/css**: The visual interface shown when clicking the extension icon.
- **popup.js**: Handles user interactions, captures data, and communicates with the backend server.

### 2. Backend Server (`server/`)

The server processes requests from the extension.

- **app.py**: A Flask web server that exposes endpoints for the extension to send job descriptions for analysis.
- **train_model.py**: A utility script used to train and generate the `basic_model.pkl`.
- **model/basic_model.pkl**: The pre-trained Scikit-learn model used for prediction.

## Setup Instructions

### Prerequisites

- Python 3.x installed
- Google Chrome browser

### Backend Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
   The server will typically start on `http://127.0.0.1:5000`.

### Extension Setup

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked**.
4. Select the `extension` folder from this repository.
5. The extension should now appear in your browser toolbar.

## Usage

1. Ensure the backend server is running.
2. Click on the Fake Job Detector icon in Chrome.
3. (Optional) Depending on implementation, it may automatically analyze the current page or require input.
4. View the result in the popup window.
