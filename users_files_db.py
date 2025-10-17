import sqlite3
from datetime import datetime
import pandas as pd
from io import BytesIO
from telegram import InputFile,Update

#USERS DATA
user_conn = sqlite3.connect("users_data.db")
user_cursor = user_conn.cursor()

#create the table
def create_users_table():
    user_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            user_type TEXT DEFAULT 'normel',
            joined_at TEXT
        )
    """)
    user_conn.commit()

#add new user
def add_user(user_id, username, full_name, user_type="normel"):
    joined_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, full_name, user_type, joined_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, full_name, user_type, joined_at))
    user_conn.commit()


#update the user info
def update_user_info(user_id, new_full_name=None, new_user_type=None):
    if new_full_name:
        user_cursor.execute("UPDATE users SET full_name = ? WHERE user_id = ?", (new_full_name, user_id))
    if new_user_type:
        user_cursor.execute("UPDATE users SET user_type = ? WHERE user_id = ?", (new_user_type, user_id))
    user_conn.commit()
    
    
#send the data as excel file
async def send_users_excel(update : Update):
    user_cursor.execute("SELECT user_id, username, full_name, user_type, joined_at FROM users")
    rows = user_cursor.fetchall()
    df = pd.DataFrame(rows, columns=["User ID", "Username", "Full Name", "User Type", "Joined At"])
    df = df.sort_values(by=["User Type"])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0) 
    await update.message.reply_document(document=InputFile(buffer, filename="users.xlsx"))
    
    
    
    
#FILES DATA

file_conn = sqlite3.connect("files_data.db")
file_cursor = file_conn.cursor()


#create the table
def create_files_table():
    file_cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            course_name TEXT,
            semester TEXT,
            year TEXT,
            type TEXT,
            uploaded_at TEXT
        )
    """)
    file_conn.commit()


#add new file
def add_file(file_name, course_name, type,semester, year):
    uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_cursor.execute("""
        INSERT INTO files (file_name, course_name, type , semester, year, uploaded_at)
        VALUES (?, ?, ?, ?, ? ,?)
    """, (file_name, course_name, type, semester, year, uploaded_at))
    file_conn.commit()


#remove file
def remove_file(file_name, course_name, type, semester, year):
    file_cursor.execute("""
        SELECT COUNT(*) FROM files
        WHERE file_name = ? AND course_name = ? AND type = ? AND semester = ? AND year = ?
    """, (file_name, course_name, type, semester, year))
    count = file_cursor.fetchone()[0]
    if count == 0:
        return
    file_cursor.execute("""
        DELETE FROM files
        WHERE file_name = ? AND course_name = ? AND type = ? AND semester = ? AND year = ?
    """, (file_name, course_name, type, semester, year))
    file_conn.commit()
    


#send the data as excel file
async def send_files_excel(update: Update):
    file_cursor.execute("SELECT file_name, course_name, type, semester, year, uploaded_at FROM files")
    rows = file_cursor.fetchall()
    df = pd.DataFrame(rows, columns=["file_name", "course_name", "type", "semester", "year", "uploaded_at"])
    df = df.sort_values(by=["year", "semester", "type", "course_name", "file_name"])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    await update.message.reply_document(document=InputFile(buffer, filename="files.xlsx"))


