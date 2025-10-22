import os
from abc import ABC, abstractmethod

# Abstract Student Class
class Student(ABC):
    def __init__(self, student_id, name, programme, dob, cgpa):
        self.student_id = student_id
        self.name = name
        self.programme = programme
        self._dob = dob
        self._cgpa = cgpa

    @abstractmethod
    def display_info(self): # Displays info
        pass

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Programme: {self.programme}, DOB: {self._dob}, CGPA: {self._cgpa}"


# Subclass: BusinessStudent
class BusinessStudent(Student):
    def display_info(self):
        return f"Business Student - {Student.__str__(self)}"


# Subclass: ComputingStudent
class ComputingStudent(Student):
    def display_info(self):
        return f"Computing Student - {Student.__str__(self)}"


# File to store student records
file_path = "C:\Users\USER\Desktop\students.txt"

# File handling functions
def save_students_to_file(students):
    with open(file_path, "w") as file: 
        for student in students:
            file.write(f"{student.student_id},{student.name},{student.programme},{student._dob},{student._cgpa}\n") # Writes the details of student into the file


def load_students_from_file(): 
    students = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file: 
            for line in file:
                student_id, name, programme, dob, cgpa = line.strip().split(",") 
                if programme == "Computing":
                    students.append(ComputingStudent(student_id, name, programme, dob, float(cgpa))) # Displays computing student details
                else:
                    students.append(BusinessStudent(student_id, name, programme, dob, float(cgpa))) # Displays Business student details
    return students


# Validation Functions
def is_duplicate_student_id(students, student_id):
    return any(student.student_id == student_id for student in students) # Checks if duplicate ID is entered


def validate_student_id(student_id):
    if not student_id.isdigit(): # Checks if ID is in digits
        raise ValueError("Student ID must be numeric.")


def validate_cgpa(cgpa):
    if not (0.0 <= float(cgpa) <= 4.0): # Checks if cgpa is valid
        raise ValueError("CGPA must be between 0.0 and 4.0.")


# Main Menu Functions
def add_student(students):
    try:
        student_id = input("Enter Student ID: ")
        validate_student_id(student_id)

        if is_duplicate_student_id(students, student_id):
            print("Error: Duplicate Student ID. Cannot add this student.")
            return

        name = input("Enter Student Name: ")
        programme = input("Enter Programme (Computing/Business): ").strip()
        if programme not in ["Computing", "Business"]:
            print("Error: Programme must be either 'Computing' or 'Business'.")
            return

        dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        cgpa = input("Enter CGPA: ")
        validate_cgpa(cgpa)

        # Assign student based on the programme
        if programme == "Computing":
            student = ComputingStudent(student_id, name, programme, dob, float(cgpa))
        elif programme == "Business":
            student = BusinessStudent(student_id, name, programme, dob, float(cgpa))
        else:
            print("Error: Invalid programme entered.")
            return

        # Add student to the list
        students.append(student)
        save_students_to_file(students)
        print("Student added successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")



def search_student(students):
    student_id = input("Enter Student ID to search: ")
    for student in students:
        if student.student_id == student_id:
            print(student.display_info()) # Searches for student and displays info
            return
    print("Student not found.")


def delete_student(students):
    student_id = input("Enter Student ID to delete: ")
    for student in students:
        if student.student_id == student_id:
            students.remove(student) # Deletes student if is already exists in the file
            save_students_to_file(students)
            print("Student deleted successfully.")
            return
    print("Student not found.")


def update_student(students):
    student_id = input("Enter Student ID to update: ")
    for student in students:
        if student.student_id == student_id: # Updates student details if already exists in the file
            try:
                name = input("Enter new name (leave blank to keep current): ")
                programme = input("Enter new programme (Computing/Business, leave blank to keep current): ")
                dob = input("Enter new date of birth (YYYY-MM-DD, leave blank to keep current): ")
                cgpa = input("Enter new CGPA (leave blank to keep current): ")

                if name:
                    student.name = name
                if programme:
                    student.programme = programme
                if dob:
                    student.dob = dob
                if cgpa:
                    validate_cgpa(cgpa)
                    student.cgpa = float(cgpa)

                save_students_to_file(students)
                print("Student updated successfully.")
                return
            except ValueError as e:
                print(f"Error: {e}")
                return
    print("Student not found.")


def display_all_students(students): 
    
    if not students:
        print("No students found in the system.") # Prints this message if no students exists in the file
        return

    print("\n--- List of All Students ---")
    for student in students:
        print(student.display_info()) # Displays all the students in the file


def main_menu():
    students = load_students_from_file() # Loads all the student from file

    while True:
        print("\n*****Welcome to MCKL Student Management System*****")
        print(" ")
        print("Please select your option below")
        print('  ')
        print("1. Add Student")
        print("2. Search Student")
        print("3. Delete Student")
        print("4. Update Student")
        print("5. Display All Students")
        print("6. Exit")

        a = input("Enter your choice: ")
        if a == "1":
            add_student(students) # Prompts add_student inputs
        elif a == "2":
            search_student(students) # Prompts search_student inputs
        elif a == "3":
            delete_student(students)# Prompts delete_student inputs
        elif a == "4":
            update_student(students) # Prompts update_student inputs
        elif a == "5": 
            display_all_students(students) # Displays all the students
        elif a == "6":
            print("Exiting the program. Have a nice day!")
            break # Exits and closes the program
        else:
            print("Invalid choice. Please try again.")


# Runs the program
if __name__ == "__main__":
    main_menu()
