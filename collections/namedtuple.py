from collections import namedtuple

# Create namedtuple
Student = namedtuple("Student", ["roll_no", "name", "marks"])

students = []

while True:
    print("\n--- Student Record System ---")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student by Roll No")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        roll = int(input("Enter roll number: "))
        name = input("Enter name: ")
        marks = float(input("Enter marks: "))

        student = Student(roll, name, marks)
        students.append(student)

        print("Student added successfully.")

    elif choice == "2":
        if students:
            print("\nRoll  Name        Marks")
            print("--------------------------")
            for s in students:
                print(f"{s.roll_no:<5} {s.name:<10} {s.marks}")
        else:
            print("No student records found.")

    elif choice == "3":
        roll = int(input("Enter roll number to search: "))
        found = False

        for s in students:
            if s.roll_no == roll:
                print("\nStudent Found:")
                print("Roll No:", s.roll_no)
                print("Name   :", s.name)
                print("Marks  :", s.marks)
                found = True
                break

        if not found:
            print("Student not found.")

    elif choice == "4":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
