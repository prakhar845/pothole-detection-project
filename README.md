# Real-Time Pothole Detection System
A full-stack application for detecting road potholes from video streams using YOLOv8, with a live monitoring dashboard powered by Django Channels and Docker.

## Overview
This project provides an automated solution for road infrastructure monitoring. Traditional methods of identifying potholes rely on slow and inefficient manual reporting. This system uses computer vision to analyze video feeds in real-time, offering a scalable and proactive approach to road maintenance.

The primary goal is to provide municipal authorities, like those in Kanpur, with a tool to quickly identify road damage, enabling faster repairs, improving public safety, and reducing vehicle damage costs.

## Core Features
Real-Time Detection: Employs a YOLOv8 model to identify potholes in live or pre-recorded video streams.

1. **Live Dashboard:** A web interface built with Django that displays the annotated video and a real-time count of detected potholes.

2. **WebSocket Communication:** Utilizes Django Channels and Redis to push data from the server to the client without page refreshes.

3. **Containerized Environment:** Fully containerized with Docker and Docker Compose for easy, consistent setup and deployment.

## Technology Stack

1. **Backend:** Django, Django Channels
2. **AI / Computer Vision:** YOLOv8, PyTorch, OpenCV
3. **Real-Time Layer:** Redis, WebSockets
4. **Containerization:** Docker, Docker Compose
5. **Frontend:** Plain HTML, CSS, and JavaScript

## Getting Started
There are two methods to run this application. The recommended approach is using Docker, as it handles all dependencies and services automatically.

**Method 1:** Run with Docker (Recommended)
Prerequisites:

Docker Desktop installed and running.

(For Windows) WSL 2 installed and configured.

**Instructions:**

**Clone the Repository**

git clone https://github.com/prakhar845/pothole-detection-project.git
cd pothole-detection-project

**Build and Run the Containers**
This command will build the necessary Docker images and start the application in the background.

docker-compose up --build -d

**Access the Application**
Open your web browser and navigate to: http://127.0.0.1:8000/

**Stopping the Application**
To stop all running containers, execute:

docker-compose down

**Method 2:** Local Python Environment Setup
Prerequisites:

Python 3.10+
Redis installed and running on your system.

**Instructions:**

Clone the repository and navigate into the project directory.

Create and Activate a Virtual Environment

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

**Install Dependencies**

pip install -r requirements.txt

Ensure Redis is Running
Start your local Redis server. For WSL, you can use:

sudo service redis-server start

**Run the Application**
From the directory containing manage.py, start the Daphne server:

daphne pothole_project_django.asgi:application

**Access the Application**
Open your web browser and navigate to: http://127.0.0.1:8000/

## Project Structure
.
├── detector/                # Main Django application
│   ├── consumers.py         # WebSocket and video processing logic
│   ├── templates/           # HTML templates
│   ├── urls.py
│   ├── views.py
│   ├── best.pt              # Trained YOLOv8 model
│   └── pothole_video.mp4    # Sample video file
│
├── pothole_project_django/  # Django project settings
│   ├── asgi.py              # ASGI configuration for Channels
│   ├── settings.py
│   └── urls.py
│
├── .gitignore               # Files to be ignored by Git
├── Dockerfile               # Instructions for building the app image
├── docker-compose.yml       # Defines the Docker services (app, redis)
├── manage.py                # Django command-line utility
├── README.md                # This file
└── requirements.txt         # Python package dependencies

## Contributing
Contributions are welcome! If you have suggestions for improvements, new analysis ideas, or bug fixes, please:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature-name).
3. Make your changes and commit them (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a Pull Request.