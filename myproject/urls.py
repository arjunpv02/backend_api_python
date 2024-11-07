from django.contrib import admin
from django.urls import path
from .views import StudentList, StudentDetail
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', StudentList.as_view(), name='student-list'),
    path('students/<int:id>/', StudentDetail.as_view(), name='student-detail'),
    path('students/<int:id>/summary/', views.get_student_summary, name='student-summary'),
]
