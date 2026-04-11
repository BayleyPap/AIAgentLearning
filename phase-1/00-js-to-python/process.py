import json
from pathlib import Path

student_records = [
    {"name": "Alice", "score": 82, "subject": "maths"},
    {"name": "Bob", "score": 45, "subject": "english"},
    {"name": "Carol", "score": 60, "subject": "maths"},
    {"name": "Dave", "score": 73, "subject": "english"},
    {"name": "Eve", "score": 91, "subject": "maths"},
    {"name": "Frank", "score": 38, "subject": "english"},
    {"name": "Grace", "score": 67, "subject": "english"},
    {"name": "Hiro", "score": 55, "subject": "maths"},
]

passing_student = []
for student in student_records:
    if student["score"] >= 60:
        passing_student.append(student)

print("Student records:")
print(student_records)
print("Passing students:")
print(passing_student)

passing_student_sorted = sorted(
    passing_student, key=lambda student: student["score"], reverse=True
)

print("Passing students sorted:")
print(passing_student_sorted)


grouped_by_subject = {"maths": [], "english": []}
for student in passing_student_sorted:
    if student["subject"] == "maths":
        grouped_by_subject["maths"].append(student)
    elif student["subject"] == "english":
        grouped_by_subject["english"].append(student)

print("Grouped by subject:")
print(grouped_by_subject)

Path("output.json").write_text(json.dumps(grouped_by_subject, indent=2))

print("===SUMMARY===")
print(
    f"Total students = {len(student_records)}"
)  # Assuming a student cant take both classes
print(f"Passsing students: {len(passing_student)}")
print(
    f"Top scorer: {passing_student_sorted[0]['name']} with {passing_student_sorted[0]['score']} in {passing_student_sorted[0]['subject']}"
)
