from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('login_student/', views.login_student, name='login_student'),
    path('students/', views.students, name='students'),
    path('logout/', views.logout_view, name='logout'),
    path('login_parents/', views.login_parent, name='login_parent'),
    path('parents/', views.parents, name='parents'),
    path('login_teacher/', views.login_teacher, name='login_teacher'),
    path('teacher/', views.teacher, name='teacher'),
    path('discription/', views.discription, name='discription'),
    path('teacher_schedule/<int:teacher_id>/', views.teacher_schedule_view, name='teacher_schedule'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
