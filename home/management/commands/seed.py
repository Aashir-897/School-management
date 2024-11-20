from django.core.management.base import BaseCommand
from home.models import Student  # Replace with your model
import random

class Command(BaseCommand):
    help = 'Seed the database with random data'

    def handle(self, *args, **kwargs):
        data = []
        for _ in range(5000):  # Generate 5000 records
            data.append(Student(
                name=f"Student_{random.randint(1, 10000)}",
                roll_number=random.randint(1, 5000),
                student_class=random.choice(['10th', '9th', '8th'])
            ))
        Student.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS('Successfully added 5000 records!'))
