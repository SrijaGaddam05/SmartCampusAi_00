"""
Database Seeder utility for SmartCampusAI.
Populates JSON files with default demo data for testing.
"""
import sys
import os
import datetime
import uuid

# Add parent directory to path to enable local module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import save_json
from utils.security import hash_password

def seed_database():
    print("Seeding database JSON data...")
    
    # 1. Hash passwords
    admin_pw = hash_password("admin123")
    student_pw = hash_password("student123")
    faculty_pw = hash_password("faculty123")
    
    # 2. Seed Users
    users = [
        {
            "id": "admin-uuid-1",
            "name": "Campus Administrator",
            "username": "admin",
            "email": "admin@university.edu",
            "password": admin_pw,
            "role": "Admin",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": "student-uuid-1",
            "name": "Alice Smith",
            "username": "alice",
            "email": "alice@university.edu",
            "password": student_pw,
            "role": "Student",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": "faculty-uuid-1",
            "name": "Dr. Alan Turing",
            "username": "turing",
            "email": "turing@university.edu",
            "password": faculty_pw,
            "role": "Faculty",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    save_json("users", users)
    
    # 3. Seed Students
    students = [
        {"id": "student-uuid-1", "name": "Alice Smith", "email": "alice@university.edu", "username": "alice", "department": "Computer Science", "enrollment_date": "2024-09-01", "status": "Active"},
        {"id": "student-uuid-2", "name": "Bob Jones", "email": "bob@university.edu", "username": "bob", "department": "Computer Science", "enrollment_date": "2024-09-01", "status": "Active"},
        {"id": "student-uuid-3", "name": "Charlie Brown", "email": "charlie@university.edu", "username": "charlie", "department": "Electrical Eng.", "enrollment_date": "2024-09-01", "status": "Active"},
        {"id": "student-uuid-4", "name": "Diana Prince", "email": "diana@university.edu", "username": "diana", "department": "Electrical Eng.", "enrollment_date": "2024-09-01", "status": "Inactive"},
        {"id": "student-uuid-5", "name": "Ethan Hunt", "email": "ethan@university.edu", "username": "ethan", "department": "Business Admin", "enrollment_date": "2024-09-01", "status": "Active"}
    ]
    save_json("students", students)
    
    # 4. Seed Faculty
    faculty = [
        {"id": "faculty-uuid-1", "name": "Dr. Alan Turing", "email": "turing@university.edu", "username": "turing", "department": "Computer Science", "designation": "Professor", "status": "Active"},
        {"id": "faculty-uuid-2", "name": "Dr. Grace Hopper", "email": "hopper@university.edu", "username": "hopper", "department": "Computer Science", "designation": "Associate Professor", "status": "Active"},
        {"id": "faculty-uuid-3", "name": "Prof. Nikola Tesla", "email": "tesla@university.edu", "username": "tesla", "department": "Electrical Eng.", "designation": "Professor", "status": "Active"}
    ]
    save_json("faculty", faculty)
    
    # 5. Seed Attendance
    today = datetime.date.today().strftime("%Y-%m-%d")
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    attendance = [
        {"id": "att-1", "student_id": "student-uuid-1", "student_name": "Alice Smith", "department": "Computer Science", "date": today, "status": "Present", "marked_by": "admin"},
        {"id": "att-2", "student_id": "student-uuid-2", "student_name": "Bob Jones", "department": "Computer Science", "date": today, "status": "Present", "marked_by": "admin"},
        {"id": "att-3", "student_id": "student-uuid-1", "student_name": "Alice Smith", "department": "Computer Science", "date": yesterday, "status": "Present", "marked_by": "admin"},
        {"id": "att-4", "student_id": "student-uuid-2", "student_name": "Bob Jones", "department": "Computer Science", "date": yesterday, "status": "Absent", "marked_by": "admin"}
    ]
    save_json("attendance", attendance)
    
    # 6. Seed Timetable
    timetable = [
        {"id": "t1", "department": "Computer Science", "semester": "Semester 1", "day": "Monday", "time": "09:00 AM - 10:30 AM", "subject": "Intro to Programming", "instructor": "Dr. Alan Turing", "room": "Lab 101"},
        {"id": "t2", "department": "Computer Science", "semester": "Semester 1", "day": "Tuesday", "time": "11:00 AM - 12:30 PM", "subject": "Discrete Mathematics", "instructor": "Dr. Grace Hopper", "room": "Room 305"},
        {"id": "t3", "department": "Computer Science", "semester": "Semester 1", "day": "Wednesday", "time": "02:00 PM - 03:30 PM", "subject": "Database Systems", "instructor": "Dr. Grace Hopper", "room": "Lab 102"},
        {"id": "t4", "department": "Computer Science", "semester": "Semester 1", "day": "Thursday", "time": "09:00 AM - 10:30 AM", "subject": "Computer Architecture", "instructor": "Dr. Alan Turing", "room": "Room 201"},
        {"id": "t5", "department": "Electrical Eng.", "semester": "Semester 1", "day": "Monday", "time": "10:30 AM - 12:00 PM", "subject": "Basic Circuit Theory", "instructor": "Prof. Nikola Tesla", "room": "Room 204"}
    ]
    save_json("timetable", timetable)
    
    # 7. Seed System Settings
    settings = {
        "theme": "Dark",
        "notifications_enabled": True,
        "maintenance_mode": False,
        "system_name": "SmartCampusAI"
    }
    save_json("settings", settings)
    
    # 8. Seed Activity Log
    activity = [
        {
            "id": "act-1",
            "username": "system",
            "action": "Database Seeded",
            "details": "Demo database records successfully initialized.",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    save_json("activity", activity)
    
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_database()
