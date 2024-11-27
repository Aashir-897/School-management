from django.core.management.base import BaseCommand
from home.models import Student, SubjectResult  # Adjust for your app's name
import random
import string
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed the database with random student data and results'

    def generate_random_string(self, length=8):
        """Generate a random string of fixed length."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def generate_random_date(self):
        """Generate a random date within the last year."""
        start_date = date.today() - timedelta(days=365)
        end_date = date.today()
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    def handle(self, *args, **kwargs):
        students_data = []
        subjects = ['Math', 'English', 'Science', 'History', 'Geography']

        # Create 1000 students
        for _ in range(1000000):
            student_name = f"Student_{random.randint(1, 10000)}"
            roll_number = self.generate_random_string(6)  # Random roll number
            student_class = random.choice(['10', '11', '12'])

            student = Student(
                name=student_name,
                roll_number=roll_number,
                student_class=student_class
            )
            students_data.append(student)

        # Save students to the database first
        saved_students = Student.objects.bulk_create(students_data)

        # Now create results for each student
        subject_results_data = []
        for student in saved_students:
            for subject in subjects:
                subject_result = SubjectResult(
                    student=student,
                    subject_name=subject,
                    result=random.choice(['A', 'B', 'C', 'D', 'F']),  # Random result
                    exam_date=self.generate_random_date(),
                )
                subject_results_data.append(subject_result)

        # Bulk create the subject results after the students are saved
        if subject_results_data:
            SubjectResult.objects.bulk_create(subject_results_data)

        self.stdout.write(self.style.SUCCESS('Successfully added students and subject results!'))
