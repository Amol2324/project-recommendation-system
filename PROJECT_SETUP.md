# Project Recommendation System - Complete Setup Guide

## Project Overview
A full-stack web application that recommends projects to students based on their skills. Built with React (Frontend), Python Flask (Backend), and Oracle Database.

## Project Structure
```
Dbms2/
├── backend/                 # Python Flask Backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration file
│   ├── requirements.txt    # Python dependencies
│   ├── database/          # Database scripts
│   │   ├── schema.sql     # Database schema
│   │   └── sample_data.sql # Sample data
│   └── README.md          # Backend documentation
├── src/                    # React Frontend
│   ├── components/        # React components
│   ├── pages/             # Page components
│   ├── services/          # API services
│   └── ...
├── package.json           # Frontend dependencies
└── README.md              # Project documentation
```

## Prerequisites

### Frontend
- Node.js (v16 or higher)
- npm or yarn

### Backend
- Python 3.8 or higher
- Oracle Database (12c or higher)
- Oracle Instant Client

## Setup Instructions

### 1. Database Setup (Oracle)

1. **Install Oracle Database** (if not already installed)
   - Download from Oracle website
   - Install Oracle Database 12c or higher

2. **Create Database User** (optional, or use existing)
   ```sql
   CREATE USER project_recommender IDENTIFIED BY your_password;
   GRANT CONNECT, RESOURCE, DBA TO project_recommender;
   ```

3. **Run Database Scripts**
   - Connect to Oracle Database as the user
   - Run `backend/database/schema.sql` to create tables
   - Run `backend/database/sample_data.sql` to insert sample data

### 2. Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Oracle Instant Client**
   - Download from [Oracle website](https://www.oracle.com/database/technologies/instant-client/downloads.html)
   - Extract and add to PATH (Windows) or set LD_LIBRARY_PATH (Linux/Mac)

5. **Configure environment variables**
   - Create a `.env` file in the `backend` directory:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_DSN=localhost:1521/XE
   ```
   - Adjust DSN format based on your Oracle setup

6. **Run the backend server**
   ```bash
   python app.py
   ```
   - Server will run on `http://localhost:5000`

### 3. Frontend Setup

1. **Navigate to project root**
   ```bash
   cd ..  # if you're in backend directory
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure API URL** (optional)
   - Create `.env` file in project root:
   ```
   VITE_API_URL=http://localhost:5000/api
   ```

4. **Run the frontend**
   ```bash
   npm run dev
   ```
   - Frontend will run on `http://localhost:3000`

## Testing the Application

1. **Check Backend Health**
   - Open browser: `http://localhost:5000/api/health`
   - Should return: `{"status": "healthy", "database": "connected"}`

2. **Access Frontend**
   - Open browser: `http://localhost:3000`
   - You should see the home page

3. **Test Flow**
   - Go to Profile page
   - Add your name, email, and select skills
   - Save profile
   - Go to Recommendations page to see matched projects
   - Browse all projects in Projects page

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Students
- `POST /api/students` - Create student
- `GET /api/students/<id>` - Get student
- `PUT /api/students/<id>` - Update student

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get project details
- `POST /api/projects` - Create project

### Skills
- `GET /api/skills` - Get all skills

### Recommendations
- `GET /api/recommendations/<student_id>` - Get recommendations

## Troubleshooting

### Database Connection Issues
- Verify Oracle Database is running
- Check DSN format: `host:port/service_name`
- Ensure Oracle Instant Client is installed and in PATH
- Verify credentials in `.env` file

### Backend Issues
- Check Python version: `python --version` (should be 3.8+)
- Verify all dependencies: `pip list`
- Check for port conflicts (default: 5000)

### Frontend Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 16+)
- Verify API URL in browser console

## Database Tables

1. **STUDENTS** - Student information
2. **PROJECTS** - Project details
3. **SKILLS** - Available skills
4. **STUDENT_SKILLS** - Student-skill relationships
5. **PROJECT_SKILLS** - Project-skill requirements
6. **RECOMMENDATIONS** (optional) - Recommendation history
7. **PROJECT_CATEGORIES** (optional) - Project categories

## Next Steps

- [ ] Add user authentication
- [ ] Implement project reviews/ratings
- [ ] Add advanced filtering
- [ ] Enhance recommendation algorithm
- [ ] Add project search functionality
- [ ] Implement project saving/favorites

## Support

For issues or questions, refer to:
- Backend README: `backend/README.md`
- Frontend README: `README.md`
- Database Schema: `database_design.md`

