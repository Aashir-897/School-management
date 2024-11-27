from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, SubjectResult, Parent, Attendance, Teacher

class SubjectResultInline(admin.TabularInline):
    model = SubjectResult
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'student_class')
    inlines = [SubjectResultInline]
    list_per_page = 10 

admin.site.register(Student, StudentAdmin)

class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_per_page = 10

admin.site.register(Parent, ParentAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'date', 'present')
    list_filter = ('present', 'student', 'teacher')
    search_fields = ('student__name', 'teacher__first_name', 'teacher__last_name')
    list_per_page = 10

admin.site.register(Attendance, AttendanceAdmin)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'subject',)
    list_filter = ('is_active', 'department', 'subject')
    search_fields = ('first_name', 'last_name', 'subject', 'department')
    ordering = ('first_name', 'last_name')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'password', 'email', 'phone_number')
        }),
        ('Professional Details', {
            'fields': ('subject', 'department', 'hire_date', 'salary', 'is_active')
        }),
    )
    list_per_page = 10