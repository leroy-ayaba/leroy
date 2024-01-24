import tkinter as tk
from tkinter import ttk
from GradingDatabase import GradingDatabase
from tkinter import messagebox

class Student:
    def __init__(self, name, db_file):
        self.name = name
        self.grades = {}
        self.comments = {}
        self.db = GradingDatabase(db_file)
        self.student_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.exam_var = tk.StringVar()
        self.grade_var = tk.StringVar()
        self.comment_var = tk.StringVar()



    def add_grade(self, subject, exam, grade):
        if subject not in self.grades:
                self.grades[subject] = {}
        self.grades[subject][exam] = grade
    def add_comment(self, subject, comment):
        self.comments[subject] = comment


    def get_grade(self, subject, exam):
        if subject in self.grades and exam in self.grades[subject]:
            return self.grades[subject][exam]
        else:
            return None
    def get_comment(self, subject):
        if subject in self.comments:
            return self.comments[subject]
        else:
            return None


class GradingPlatformGUI:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Frame for grading platform
        frame = tk.Frame(self.root, width=400, height=300)
        frame.pack(padx=10, pady=10)

        # Label for header
        lbl_header = ttk.Label(frame, text="Grading Platform", font=("Arial", 16))
        lbl_header.pack(pady=10)

        student_name_label = tk.Label(self.root, text="Student Name")
        student_name_label.pack()

        student_name_entry = tk.Entry(self.root, textvariable=self.student_name_var)
        student_name_entry.pack()

        student_id_label = tk.Label(self.root, text="Student ID")
        student_id_label.pack()

        student_id_entry = tk.Entry(self.root, textvariable=self.student_id_var)
        student_id_entry.pack()

        lbl_student = ttk.Label(frame, text="Select Student:")
        lbl_student.pack()

        cmb_student = tk.StringVar()
        cmb_student.set("Student 1")
        student_dropdown = ttk.OptionMenu(frame, cmb_student, "Student 1", "Student 2", "Student 3")
        student_dropdown.pack()


        lbl_subject = tk.Label(frame, text="Select Subject:")
        lbl_subject.pack()

        cmb_subject = tk.StringVar()
        cmb_subject.set("Math")
        subject_dropdown = ttk.OptionMenu(frame, cmb_subject, "Math", "Science", "English")
        subject_dropdown.pack()

        # Exam Entry
        lbl_exam = tk.Label(frame, text="Exam Name:")
        lbl_exam.pack()

        entry_exam = ttk.Entry(frame)
        entry_exam.pack()


        lbl_grade = ttk.Label(frame, text="Grade:")
        lbl_grade.pack()

        entry_grade = tk.Entry(frame)
        entry_grade.pack()


        lbl_comment = ttk.Label(frame, text="Comment:")
        lbl_comment.pack()

        entry_comment = ttk.Entry(frame)
        entry_comment.pack()

        add_student_button = tk.Button(self.root, text="Add Student", command=self.add_student)
        add_student_button.pack()

        btn_record_grade = ttk.Button(frame, text="Record Grade", command=lambda: self.record_grade(cmb_student.get(), cmb_subject.get(), entry_exam.get(), entry_grade.get(), entry_comment.get()))
        btn_record_grade.pack(pady=10)

        btn_generate_report_card = ttk.Button(frame, text="Generate Report Card", command=self.generate_report_card)
        btn_generate_report_card.pack(padx=10, pady=5)

        btn_generate_transcript = ttk.Button(frame, text="Generate Transcript", command=self.generate_report_card)
        btn_generate_transcript.pack(padx=11, pady=5)



    def get_student_names(self):
     return [student.name for student in self.students]

    def add_student(self):
         student_name = self.student_name_var.get()
         student_id = self.student_id_var.get()

         if not student_name:
             messagebox.showwarning("Missing Information", "Please enter a student name.")
             return

         if not student_id:
             messagebox.showwarning("Missing Information", "Please enter a student ID.")
             return

         student_id = self.db.add_student(student_name, student_id)
         if student_id is None:
             messagebox.showerror("Duplicate Entry", "Student name or ID already exists.")
             return

         messagebox.showinfo("Student Added", "Student added successfully.")

    def get_subjects(self):
     subjects = set()
     for student in self.students:
        subjects.update(student.grades.keys())
        return list(subjects)

    def record_grade(self):
      student_name = self.student_var.get()
      subject = self.subject_var.get()
      exam = self.exam_var.get()
      grade = self.grade_var.get()
      comment = self.comment_var.get()

      if not student_name or not subject or not exam or not grade:
             messagebox.showwarning("Missing Information", "Please fill in all fields.")
             return
      student_id = self.db.add_student(student_name)
      if student_id is None:
          messagebox.showeerror("DuplicateEntry", "student name already exists.")
          return



      self.db.add_grade(student_id,subject,exam,grade,comment)
      messagebox.showinfo("Grade recoeded", "grade recorded successfuly")


    def generate_report_card(self):
        student_name = self.student_var.get()
        if not student_name:
            messagebox.showwarning("Missing Information", "Please select a student.")
            return
        for student in self.students:
            if student.name == student_name:
                report_card = f"Report Card for {student.name}\n\n"
                for subject, grades in student.grades.items():
                    for exam, grade in grades.items():
                        report_card += f"  - {exam}: {grade}\n"
                        report_card += f"\n"
                        messagebox.showinfo("Report Card", report_card)
                        break

    def generate_transcript(self):
        student_name = self.student_var.get()
        if not student_name:
            messagebox.showwarning("Missing Information", "Please select a student.")
            return
        for student in self.students:
            if student.name == student_name:
                transcript = f"Transcript for {student.name}\n\n"
                for subject, grades in student.grades.items():
                    transcript += f"{subject}:\n"
                    transcript += f"{subject}:\n"
                    for exam, grade in grades.items():
                        transcript += f"  - {exam}: {grade}\n"
                        comment = student.get_comment(subject)
                        if comment:
                            transcript += f"  - Comment: {comment}\n"
                            transcript += f"\n"
                            messagebox.showinfo("Transcript", transcript)
                            break



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Grading Platform")
    gui = GradingPlatformGUI(root)
    root.mainloop()