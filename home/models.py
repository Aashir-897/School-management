from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=128, blank=True)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubjectResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject_name = models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.subject_name}: {self.result} on {self.exam_date}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        if self.student:
            return f"{self.student.name} - {self.date} - {'Present' if self.present else 'Absent'}"
        elif self.teacher:
            return f"{self.teacher.first_name} {self.teacher.last_name} - {self.date} - {'Present' if self.present else 'Absent'}"

class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TeacherSchedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.teacher} - {self.day}: {self.subject} ({self.start_time} - {self.end_time})"
