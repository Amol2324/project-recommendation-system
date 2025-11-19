from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '@yush2004'),
    'database': os.getenv('DB_NAME', 'project_recommender')
}

def get_db_connection():
    """Create and return MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        return connection
    except Error as e:
        print(f"Database connection error: {str(e)}")
        return None

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Sign up a new user with Full Name, email, and password"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        # Validation
        if not name or not email or not password:
            return jsonify({'error': 'Full Name, email, and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("""
            SELECT student_id FROM STUDENTS WHERE email = %s
        """, (email,))
        
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Email already registered. Please login instead.'}), 400
        
        # Insert student (store password as plain text)
        cursor.execute("""
            INSERT INTO STUDENTS (name, email, password_hash)
            VALUES (%s, %s, %s)
        """, (name, email, password))
        
        student_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Account created successfully',
            'student_id': student_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with email and password"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get student by email
        cursor.execute("""
            SELECT student_id, name, email, password_hash
            FROM STUDENTS
            WHERE email = %s
        """, (email,))
        
        student_row = cursor.fetchone()
        if not student_row:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        student_id, name, db_email, stored_password = student_row
        
        # Verify password (plain text comparison)
        if not stored_password or stored_password != password:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Get student skills
        cursor.execute("""
            SELECT s.skill_id, s.skill_name, ss.proficiency_level, ss.years_of_experience
            FROM STUDENT_SKILLS ss
            JOIN SKILLS s ON ss.skill_id = s.skill_id
            WHERE ss.student_id = %s
        """, (student_id,))
        
        skills = []
        for row in cursor.fetchall():
            skills.append({
                'skill_id': row[0],
                'skill_name': row[1],
                'proficiency_level': row[2],
                'years_of_experience': row[3]
            })
        
        student = {
            'student_id': student_id,
            'name': name,
            'email': db_email,
            'skills': skills
        }
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Login successful',
            'student': student
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== STUDENT ROUTES ====================

@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student profile"""
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Insert student
        cursor.execute("""
            INSERT INTO STUDENTS (name, email)
            VALUES (%s, %s)
        """, (data.get('name'), data.get('email')))
        
        student_id = cursor.lastrowid
        
        # Insert student skills
        if 'skills' in data and data['skills']:
            for skill in data['skills']:
                cursor.execute("""
                    INSERT INTO STUDENT_SKILLS (student_id, skill_id, proficiency_level, years_of_experience)
                    VALUES (%s, %s, %s, %s)
                """, (
                    student_id,
                    skill.get('skill_id'),
                    skill.get('proficiency_level', 'Beginner'),
                    skill.get('years_of_experience', 0)
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Student created successfully',
            'student_id': student_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get student profile with skills"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get student info
        cursor.execute("""
            SELECT student_id, name, email, created_at, updated_at
            FROM STUDENTS
            WHERE student_id = %s
        """, (student_id,))
        
        student_row = cursor.fetchone()
        if not student_row:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Student not found'}), 404
        
        student = {
            'student_id': student_row[0],
            'name': student_row[1],
            'email': student_row[2],
            'created_at': student_row[3].isoformat() if student_row[3] else None,
            'updated_at': student_row[4].isoformat() if student_row[4] else None
        }
        
        # Get student skills
        cursor.execute("""
            SELECT s.skill_id, s.skill_name, ss.proficiency_level, ss.years_of_experience
            FROM STUDENT_SKILLS ss
            JOIN SKILLS s ON ss.skill_id = s.skill_id
            WHERE ss.student_id = %s
        """, (student_id,))
        
        skills = []
        for row in cursor.fetchall():
            skills.append({
                'skill_id': row[0],
                'skill_name': row[1],
                'proficiency_level': row[2],
                'years_of_experience': row[3]
            })
        
        student['skills'] = skills
        
        cursor.close()
        conn.close()
        
        return jsonify(student), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update student profile and skills"""
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Update student info
        cursor.execute("""
            UPDATE STUDENTS
            SET name = %s, email = %s
            WHERE student_id = %s
        """, (data.get('name'), data.get('email'), student_id))
        
        # Delete existing skills
        cursor.execute("""
            DELETE FROM STUDENT_SKILLS WHERE student_id = %s
        """, (student_id,))
        
        # Insert new skills
        if 'skills' in data and data['skills']:
            for skill in data['skills']:
                cursor.execute("""
                    INSERT INTO STUDENT_SKILLS (student_id, skill_id, proficiency_level, years_of_experience)
                    VALUES (%s, %s, %s, %s)
                """, (
                    student_id,
                    skill.get('skill_id'),
                    skill.get('proficiency_level', 'Beginner'),
                    skill.get('years_of_experience', 0)
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Student updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PROJECT ROUTES ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects with optional filters"""
    try:
        difficulty = request.args.get('difficulty')
        category = request.args.get('category')
        search = request.args.get('search', '')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Build query with filters
        query = """
            SELECT DISTINCT p.project_id, p.title, p.description, 
                   p.difficulty_level, p.category, p.created_at
            FROM PROJECTS p
            WHERE 1=1
        """
        params = []
        
        if difficulty:
            query += " AND UPPER(p.difficulty_level) = UPPER(%s)"
            params.append(difficulty)
        
        if category:
            query += " AND UPPER(p.category) = UPPER(%s)"
            params.append(category)
        
        if search:
            query += " AND (UPPER(p.title) LIKE UPPER(%s) OR UPPER(p.description) LIKE UPPER(%s))"
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += " ORDER BY p.created_at DESC"
        
        cursor.execute(query, tuple(params))
        
        projects = []
        for row in cursor.fetchall():
            project = {
                'project_id': row[0],
                'title': row[1],
                'description': row[2],
                'difficulty_level': row[3],
                'category': row[4],
                'created_at': row[5].isoformat() if row[5] else None
            }
            
            # Get project skills
            cursor.execute("""
                SELECT s.skill_id, s.skill_name, ps.required_proficiency_level, ps.is_mandatory
                FROM PROJECT_SKILLS ps
                JOIN SKILLS s ON ps.skill_id = s.skill_id
                WHERE ps.project_id = %s
            """, (row[0],))
            
            skills = []
            for skill_row in cursor.fetchall():
                skills.append({
                    'skill_id': skill_row[0],
                    'skill_name': skill_row[1],
                    'required_proficiency_level': skill_row[2],
                    'is_mandatory': skill_row[3]
                })
            
            project['skills'] = skills
            projects.append(project)
        
        cursor.close()
        conn.close()
        
        return jsonify(projects), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get project details by ID"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT project_id, title, description, difficulty_level, 
                   category, created_at, created_by
            FROM PROJECTS
            WHERE project_id = %s
        """, (project_id,))
        
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Project not found'}), 404
        
        project = {
            'project_id': row[0],
            'title': row[1],
            'description': row[2],
            'difficulty_level': row[3],
            'category': row[4],
            'created_at': row[5].isoformat() if row[5] else None,
            'created_by': row[6]
        }
        
        # Get project skills
        cursor.execute("""
            SELECT s.skill_id, s.skill_name, s.skill_type, 
                   ps.required_proficiency_level, ps.is_mandatory
            FROM PROJECT_SKILLS ps
            JOIN SKILLS s ON ps.skill_id = s.skill_id
            WHERE ps.project_id = %s
        """, (project_id,))
        
        skills = []
        for skill_row in cursor.fetchall():
            skills.append({
                'skill_id': skill_row[0],
                'skill_name': skill_row[1],
                'skill_type': skill_row[2],
                'required_proficiency_level': skill_row[3],
                'is_mandatory': skill_row[4]
            })
        
        project['skills'] = skills
        
        cursor.close()
        conn.close()
        
        return jsonify(project), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.json
        title = data.get('title', '').strip()
        
        if not title:
            return jsonify({'error': 'Project title is required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Check if project with same title already exists
        cursor.execute("""
            SELECT project_id FROM PROJECTS WHERE UPPER(title) = UPPER(%s)
        """, (title,))
        
        existing_project = cursor.fetchone()
        if existing_project:
            cursor.close()
            conn.close()
            return jsonify({
                'error': 'A project with this title already exists',
                'project_id': existing_project[0]
            }), 409
        
        # Insert project
        cursor.execute("""
            INSERT INTO PROJECTS (title, description, difficulty_level, category, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            title,
            data.get('description'),
            data.get('difficulty_level', 'Beginner'),
            data.get('category'),
            data.get('created_by', 'Admin')
        ))
        
        project_id = cursor.lastrowid
        
        # Insert project skills
        if 'skills' in data and data['skills']:
            for skill in data['skills']:
                cursor.execute("""
                    INSERT INTO PROJECT_SKILLS (project_id, skill_id, required_proficiency_level, is_mandatory)
                    VALUES (%s, %s, %s, %s)
                """, (
                    project_id,
                    skill.get('skill_id'),
                    skill.get('required_proficiency_level', 'Beginner'),
                    skill.get('is_mandatory', 'Y')
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Project created successfully',
            'project_id': project_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SKILLS ROUTES ====================

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all available skills"""
    try:
        skill_type = request.args.get('type')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        if skill_type:
            cursor.execute("""
                SELECT skill_id, skill_name, skill_type, description
                FROM SKILLS
                WHERE UPPER(skill_type) = UPPER(%s)
                ORDER BY skill_name
            """, (skill_type,))
        else:
            cursor.execute("""
                SELECT skill_id, skill_name, skill_type, description
                FROM SKILLS
                ORDER BY skill_type, skill_name
            """)
        
        skills = []
        for row in cursor.fetchall():
            skills.append({
                'skill_id': row[0],
                'skill_name': row[1],
                'skill_type': row[2],
                'description': row[3]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(skills), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RECOMMENDATIONS ROUTE ====================

@app.route('/api/recommendations/<int:student_id>', methods=['GET'])
def get_recommendations(student_id):
    """Get personalized project recommendations for a student"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get student skills
        cursor.execute("""
            SELECT s.skill_id, s.skill_name, ss.proficiency_level
            FROM STUDENT_SKILLS ss
            JOIN SKILLS s ON ss.skill_id = s.skill_id
            WHERE ss.student_id = %s
        """, (student_id,))
        
        student_skills = {}
        for row in cursor.fetchall():
            student_skills[row[0]] = {
                'skill_name': row[1],
                'proficiency_level': row[2]
            }
        
        if not student_skills:
            cursor.close()
            conn.close()
            return jsonify({
                'message': 'No skills found. Please add skills to your profile.',
                'recommendations': []
            }), 200
        
        # Get all projects
        cursor.execute("""
            SELECT project_id, title, description, difficulty_level, category
            FROM PROJECTS
            ORDER BY created_at DESC
        """)
        
        projects = []
        for row in cursor.fetchall():
            project_id = row[0]
            
            # Get project required skills
            cursor.execute("""
                SELECT s.skill_id, s.skill_name, ps.required_proficiency_level, ps.is_mandatory
                FROM PROJECT_SKILLS ps
                JOIN SKILLS s ON ps.skill_id = s.skill_id
                WHERE ps.project_id = %s
            """, (project_id,))
            
            project_skills = []
            for skill_row in cursor.fetchall():
                project_skills.append({
                    'skill_id': skill_row[0],
                    'skill_name': skill_row[1],
                    'required_proficiency_level': skill_row[2],
                    'is_mandatory': skill_row[3]
                })
            
            # Calculate match score
            match_score = calculate_match_score(student_skills, project_skills)
            
            projects.append({
                'project_id': project_id,
                'title': row[1],
                'description': row[2],
                'difficulty_level': row[3],
                'category': row[4],
                'skills': project_skills,
                'match_score': match_score
            })
        
        # Sort by match score (descending)
        projects.sort(key=lambda x: x['match_score'], reverse=True)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'student_id': student_id,
            'recommendations': projects
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_match_score(student_skills, project_skills):
    """Calculate match score between student skills and project requirements"""
    if not project_skills:
        return 50  # Default score if no skills required
    
    total_skills = len(project_skills)
    matched_skills = 0
    proficiency_bonus = 0
    
    proficiency_levels = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
    
    for project_skill in project_skills:
        skill_id = project_skill['skill_id']
        
        if skill_id in student_skills:
            matched_skills += 1
            
            # Check proficiency match
            student_prof = student_skills[skill_id]['proficiency_level']
            required_prof = project_skill.get('required_proficiency_level', 'Beginner')
            
            student_level = proficiency_levels.get(student_prof, 1)
            required_level = proficiency_levels.get(required_prof, 1)
            
            if student_level >= required_level:
                proficiency_bonus += 10  # Bonus for meeting or exceeding requirement
            elif student_level >= required_level - 1:
                proficiency_bonus += 5   # Partial bonus
    
    # Base score: percentage of matched skills
    base_score = (matched_skills / total_skills) * 100
    
    # Add proficiency bonus (capped at 20% of total)
    bonus = min(proficiency_bonus, total_skills * 10)
    
    # Final score (max 100)
    final_score = min(base_score + bonus, 100)
    
    return round(final_score, 2)

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({
                'status': 'healthy',
                'database': 'connected'
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected'
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
