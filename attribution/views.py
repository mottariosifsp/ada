from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from courses.models import Course
from attribution.models import TeacherCourseSelection, TeacherQueuePosition
from django.utils import timezone

def index(request):
    return render(request, 'attribution/index.html')



@transaction.atomic
def add_teacher_to_queue(teacher):
    queue_size = TeacherQueuePosition.objects.count()
    position = queue_size + 1
    TeacherQueuePosition.objects.create(teacher=teacher, position=position)

@transaction.atomic
def select_course(teacher):
    # pega o 1o prof da lista
    queue_position = TeacherQueuePosition.objects.first()

    if queue_position is None or queue_position.teacher != teacher:
        raise ValueError("Teacher is not in the queue")

    # pega os cursos disponíoveis
    available_courses = Course.objects.filter(
        teacherselection__isnull=True).distinct()

    # mostra os cursos disponiveis
    selected_course = None
    for course in available_courses:
        print(f"{course.id}: {course.name}")
    while not selected_course:
        course_id = input("Select a course ID: ")
        try:
            selected_course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            print("Invalid course ID")

    # ve se selecionou dentro de 1 minutio
    if (timezone.now() - queue_position.timestamp).total_seconds() > 60:
        # se n selecionou vai p final da fila
        queue_position.delete()
        queue_size = TeacherQueuePosition.objects.count()
        position = queue_size + 1
        TeacherQueuePosition.objects.create(teacher=teacher, position=position)
        print("Time's up! You have been moved to the end of the queue.")
    else:
        # salva a seleção do curso
        TeacherCourseSelection.objects.create(teacher=teacher, course=selected_course)
        # deleta o prof da fila
        queue_position.delete()
        print(f"{teacher} selected {selected_course.name}")