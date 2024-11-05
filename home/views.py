from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from collections import defaultdict
from .models import Student, Parent, SubjectResult, Attendance, Teacher, TeacherSchedule
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def login_student(request):
    error = None
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        name = request.POST.get('name')
        try:
            student = Student.objects.get(roll_number=roll_number, name=name)
            request.session['student_id'] = student.id
            return redirect('students')
        except Student.DoesNotExist:
            error = "Invalid roll number or name."
    return render(request, 'login_student.html', {'error': error})

def login_parent(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            parent = Parent.objects.get(email=email, password=password)
            return redirect('parents')
        except Parent.DoesNotExist:
            error = "Invalid email or password."
    return render(request, 'login_parents.html', {'error': error})

def parents(request):
    student = None
    attendance_records = {}
    test_results = {}
    error = None

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        try:
            student = Student.objects.get(roll_number=roll_number)

            attendance_qs = Attendance.objects.filter(student=student).order_by('date')
            for record in attendance_qs:
                month_year = record.date.strftime("%B %Y")
                if month_year not in attendance_records:
                    attendance_records[month_year] = []
                attendance_records[month_year].append({
                    'date': record.date,
                    'present': record.present
                })

            results_qs = SubjectResult.objects.filter(student=student).order_by('exam_date')
            for result in results_qs:
                month_year = result.exam_date.strftime("%B %Y")
                if month_year not in test_results:
                    test_results[month_year] = []
                test_results[month_year].append({
                    'subject_name': result.subject_name,
                    'result': result.result,
                    'exam_date': result.exam_date
                })

        except Student.DoesNotExist:
            error = "No student found with this roll number."

    return render(request, 'parents.html', {
        'student': student,
        'attendance_records': attendance_records.items(),
        'test_results': test_results.items(),
        'error': error
    })

def students(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login_student')

    student = get_object_or_404(Student, id=student_id)
    results_by_month = defaultdict(list)
    for result in student.results.all():
        month_year = result.exam_date.strftime("%B %Y")
        results_by_month[month_year].append(result)

    return render(request, 'students.html', {
        'student': student,
        'results_by_month': results_by_month.items(),
    })

def login_teacher(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            teacher = Teacher.objects.get(email=email)
            if teacher.password == password:
                request.session['teacher_id'] = teacher.id
                return redirect('teacher')
            else:
                error = "Invalid email or password."
        except Teacher.DoesNotExist:
            error = "Invalid email or password."
    return render(request, 'login_teacher.html', {'error': error})

def teacher(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('login_teacher')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher.html', {
        'teacher': teacher,
    })

def logout_view(request):
    logout(request)
    return redirect('home')

def teacher_schedule_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedules = TeacherSchedule.objects.filter(teacher=teacher)

    if request.method == 'POST':
        if 'delete' in request.POST:
            schedule_id = request.POST.get('schedule_id')
            schedule_to_delete = get_object_or_404(TeacherSchedule, id=schedule_id)
            schedule_to_delete.delete()
            return redirect('teacher_schedule', teacher_id=teacher_id)
        else:
            day = request.POST['day']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            subject = request.POST['subject']
            new_schedule = TeacherSchedule(teacher=teacher, day=day, start_time=start_time, end_time=end_time, subject=subject)
            new_schedule.save()
            return redirect('teacher_schedule', teacher_id=teacher_id)

    context = {
        'teacher': teacher,
        'schedules': schedules,
    }
    return render(request, 'teacher_schedule.html', context)

def discription(request):
    return render(request, 'discription.html')
