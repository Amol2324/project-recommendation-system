# Project Recommendation System

A web application that helps students find projects based on their skills and preferences. Built with React (Frontend), Python (Backend), and Oracle DB (Database).

## Features

- **Student Profile Management**: Students can create profiles and add their skills with proficiency levels
- **Project Browsing**: Browse through available projects with filtering and search
- **Smart Recommendations**: Get personalized project recommendations based on skill matching
- **Project Details**: View detailed information about each project including required skills and difficulty levels

## Tech Stack

- **Frontend**: React 18, React Router, Vite
- **Backend**: Python (to be implemented)
- **Database**: Oracle DB (to be implemented)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
├── src/
│   ├── components/      # Reusable components
│   │   ├── Navbar.jsx
│   │   └── ProjectCard.jsx
│   ├── pages/          # Page components
│   │   ├── Home.jsx
│   │   ├── StudentProfile.jsx
│   │   ├── Projects.jsx
│   │   ├── ProjectDetails.jsx
│   │   └── Recommendations.jsx
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── package.json
└── vite.config.js
```

## Pages

- **Home**: Landing page with overview and features
- **Profile**: Student profile creation and skill management
- **Projects**: Browse all available projects
- **Recommendations**: Personalized project recommendations
- **Project Details**: Detailed view of individual projects

## Database Design

See `database_design.md` for complete database schema and table structures.

## Future Enhancements

- Backend API integration
- Database connectivity
- User authentication
- Project reviews and ratings
- Advanced recommendation algorithms

