# Project Recommendation System - Database Design

## Overview
This system helps students find projects based on their skills and other attributes.

## Database Tables Required

### Core Tables (Minimum 5 tables):

1. **STUDENTS**
   - Stores student/user information
   - Columns: student_id (PK), name, email, password_hash, created_at, updated_at

2. **PROJECTS**
   - Stores project information
   - Columns: project_id (PK), title, description, difficulty_level, category, created_by, created_at, updated_at

3. **SKILLS**
   - Stores available skills (React, Python, Oracle DB, etc.)
   - Columns: skill_id (PK), skill_name, skill_type (frontend/backend/database/other), description

4. **STUDENT_SKILLS** (Junction Table)
   - Links students to their skills with proficiency levels
   - Columns: student_id (FK), skill_id (FK), proficiency_level (beginner/intermediate/advanced), years_of_experience

5. **PROJECT_SKILLS** (Junction Table)
   - Links projects to required skills with required proficiency
   - Columns: project_id (FK), skill_id (FK), required_proficiency_level, is_mandatory (Y/N)

### Optional/Enhanced Tables (for better functionality):

6. **PROJECT_CATEGORIES** (Optional)
   - Stores project categories/types
   - Columns: category_id (PK), category_name, description

7. **RECOMMENDATIONS** (Optional)
   - Stores recommendation history and match scores
   - Columns: recommendation_id (PK), student_id (FK), project_id (FK), match_score, recommended_at, viewed, saved

8. **PROJECT_REVIEWS** (Optional)
   - Stores student reviews/ratings for projects
   - Columns: review_id (PK), student_id (FK), project_id (FK), rating, review_text, created_at

## Total Tables: **5-8 tables** (depending on requirements)

### Minimum Required: **5 tables**
### Recommended: **7-8 tables** (for full functionality)

## Relationships:
- One Student can have Many Skills (via STUDENT_SKILLS)
- One Project can require Many Skills (via PROJECT_SKILLS)
- One Skill can be associated with Many Students
- One Skill can be required by Many Projects
- One Student can receive Many Recommendations
- One Project can be recommended to Many Students

