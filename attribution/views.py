import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from courses.models import Course
from professors.models import Professors
from attribution.models import TeacherCourseSelection, TeacherQueuePosition
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _, get_language, activate, gettext
from django.urls import reverse

startTimeToSelect = timezone.now()

def is_time_left(time):
    global startTimeToSelect
    currentTeacher = TeacherQueuePosition.objects.filter(position=1)
    timeLeft = ((startTimeToSelect + timezone.timedelta(seconds=time)) - timezone.now()).total_seconds()

    if timeLeft <= 0:
        teacherToEndOfQueue(currentTeacher)          
        startTimeToSelect = timezone.now()  

def is_superuser(user):
    return user.is_superuser

@transaction.atomic
def attribution(request):
    global startTimeToSelect

    if request.method == 'POST':
        tabela_data = json.loads(request.POST['tabela_data'])       
        startTimeToSelect = timezone.now()

        for professorInQueue in tabela_data:
            professor_id = professorInQueue[3]
            position = professorInQueue[0]
            professor = Professors.objects.get(id=professor_id)

            if TeacherQueuePosition.objects.filter(teacher=professor).exists():
                TeacherQueuePosition.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue(professor, position)    

    is_next = False
    timeLeft = 0

    if request.method == 'GET':
        is_time_left(40)
        nextTeacher = TeacherQueuePosition.objects.filter(position=1)
        teacher = nextTeacher.get().teacher

        if request.user.is_authenticated and nextTeacher and nextTeacher.get().teacher == request.user:
            timeLeft = ((startTimeToSelect + timezone.timedelta(seconds=40)) - timezone.now()).total_seconds()
            is_next = True

            if timeLeft < 0:
                timeLeft = 0
                teacherToEndOfQueue(teacher, nextTeacher)          
                startTimeToSelect = timezone.now()     

    data = {
        'timeLeft': timeLeft,
        'is_next': is_next,
        'user': request.user,
        'professorsInQueue': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
        'courses': Course.objects.filter(teachercourseselection__isnull=True).distinct()
    }
    return render(request, 'attribution/attribution.html', data)

@user_passes_test(is_superuser)
def queueSetup(request):
    trans = translate(language='en')
    data = {
        'professors': Professors.objects.all(),
        'text': trans
    }
    return render(request, 'attribution/queueSetup.html', data)

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = _('Search')
        text = _('entries')
    finally:
        activate(cur_language)
    return text

@transaction.atomic
def teacherToEndOfQueue(queue_position):
    teacher = queue_position.get().teacher
    queue_position.delete()
    queue_size = TeacherQueuePosition.objects.count()

    for teacherQueuePosition in TeacherQueuePosition.objects.all():
        if teacherQueuePosition.position > 1:
            teacherQueuePosition.position -= 1
            teacherQueuePosition.save()

    position = queue_size + 1
    TeacherQueuePosition.objects.create(teacher=teacher, position=position)

    print("Time's up! You have been moved to the end of the queue.")

@transaction.atomic
def teacherSelectCourse(course_selected, queue_position):
    teacher = queue_position.get().teacher
    selected_course = Course.objects.get(id=course_selected)
    TeacherCourseSelection.objects.create(teacher=teacher, course=selected_course)
    Course.objects.filter(id=selected_course.id).update(teacher=teacher)
    queue_position.delete()

    for teacherQueuePosition in TeacherQueuePosition.objects.all():
        if teacherQueuePosition.position > 1:
            teacherQueuePosition.position -= 1
            teacherQueuePosition.save()

    print(f"{teacher} selected {selected_course.title}")

@transaction.atomic
def selectCourse(request):
    global startTimeToSelect

    if request.method == 'POST':
        course_selected = request.POST.get("SelectCourse")
        teacher = request.user
        queue_position = TeacherQueuePosition.objects.filter(position=1)

        if not queue_position or queue_position.get().teacher != teacher:
            raise ValueError("Teacher is not in the queue")

        data = {
            'course': course_selected,
        }

        if course_selected is None:
            teacherToEndOfQueue(queue_position)
            startTimeToSelect = timezone.now()
            return render(request, 'attribution/selectCourse.html', data)
        else:
            teacherSelectCourse(course_selected, queue_position)
            startTimeToSelect = timezone.now()

        return render(request, 'attribution/selectCourse.html', data)

@transaction.atomic
def add_teacher_to_queue(teacher, position_input):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position)
