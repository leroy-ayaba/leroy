import sqlite3


class GradingDatabase:
    def __init__(self, db_file):
        self.db_conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.db_conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                exam TEXT NOT NULL,
                grade TEXT NOT NULL,
                comment TEXT,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')

        self.db_conn.commit()

    def add_student(self, name):
        cursor = self.db_conn.cursor()

        try:
            cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
            self.db_conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def add_grade(self, student_id, subject, exam, grade, comment):
        cursor = self.db_conn.cursor()

        cursor.execute("INSERT INTO grades (student_id, subject, exam, grade, comment) VALUES (?, ?, ?, ?, ?)",
                       (student_id, subject, exam, grade, comment))

        self.db_conn.commit()

    def close_connection(self):
        self.db_conn.close()