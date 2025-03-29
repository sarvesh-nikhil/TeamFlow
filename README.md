TeamFlow 🚀

Employee & Project Management System


Overview

TeamFlow is a web application designed to manage employees within a company or organisation and assigning tasks based on required skill set leveraging NLP techniques.


Tech Stack

Frontend: React (inside React/userhub/)
Backend: FastAPI (inside FastAPI/)
Database: MySQL


Containerization: Docker & Docker Compose


Features

✅ Employee Management
✅ Project Assignment Based on Skills
✅ Role-Based Access Control
✅ Interactive UI

Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/sarvesh-nikhil/teamflow.git
cd teamflow

2️⃣ Environment Setup

Create a .env file in the FastAPI/ directory and add necessary environment variables:


3️⃣ Run with Docker

To build and run TeamFlow using Docker:

docker-compose up --build

To stop running containers:

docker-compose down


4️⃣ Manual Setup (Without Docker)

Backend

cd FastAPI
pip install -r requirements.txt
uvicorn main:app --reload

Frontend

cd React/userhub
npm install
npm start


Contributing

Fork the repo

Create a new branch (git checkout -b feature-branch)

Commit chan

ges (git commit -m "Added feature")

Push to branch (git push origin feature-branch)

Open a Pull Request

License

This project is licensed under *** License.