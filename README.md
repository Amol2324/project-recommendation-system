The Project Recommendation System is a full-stack web application designed to help students find suitable academic projects based on their skills, interests, and preferred domains. The system uses a content-based filtering approach to match student profiles with relevant project ideas. It includes both student and admin modules, along with a secure authentication system and a well-structured backend API. The project is built using React for the frontend, Flask for the backend, and MySQL as the database.

Key Features

Student login and authentication using JWT.
User-friendly interface for entering skills, domains, and preferences.
Personalized project recommendations generated through a scoring and keyword-matching algorithm.
Admin dashboard to add, update, or delete project records.
Fully integrated REST APIs for smooth communication between frontend and backend.
Error handling, data validation, and responsive UI.

Tech Stack
Frontend: React.js, Axios, React Router
Backend: Python Flask, Flask-CORS, Flask-JWT-Extended
Database: MySQL with normalized schema and foreign keys
Tools: Git, VS Code, Postman

System Architecture
The frontend interacts with the backend through REST API calls. The Flask backend processes incoming requests, applies the recommendation logic, and fetches or updates data in the MySQL database. The system follows a decoupled architecture, ensuring scalability and maintainability.

Setup Instructions

Clone the repository.
Set up and activate the backend environment, then install dependencies.
Start the Flask server.
Set up the frontend by installing npm packages and running the development server.
Import the MySQL schema and seed data.

Recommendation Logic

The recommendation algorithm uses content-based filtering. It compares student skills and domain preferences with project metadata, assigns weighted scores, ranks the projects, and returns the most relevant suggestions.

Testing Conducted

Unit testing for frontend components
API endpoint testing
Database CRUD validation
Authentication and token validation
Recommendation accuracy checks

Deliverables

Fully functional frontend
Flask backend with APIs
MySQL database schema
Admin and student modules
Recommendation algorithm
Documentation and testing records
