from datetime import datetime, timezone
from enums import enum
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model

from timetable.models import Timeslot
from .models import Deadline
from area.models import Blockk, Area
from classs.models import Classs
from course.models import Course
from user.models import User, History
from .models import Deadline


def is_staff(user):
    return user.is_staff


# prazos
@login_required
@user_passes_test(is_staff)
def home(request):
    return render(request, 'staff/home_staff.html')


@login_required
@user_passes_test(is_staff)
def deadline_configuration(request):
    user_blocks = request.user.blocks.all()

    data = {
        'user_blocks': user_blocks
    }

    return render(request, 'staff/deadline/deadline_configuration.html', data)


def confirm_deadline_configuration(request):
    if request.method == 'POST':
        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), '%Y-%m-%dT%H:%M')
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), '%Y-%m-%dT%H:%M')
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        startExchangeDeadline = datetime.strptime(request.POST.get('startExchangeDeadline'), '%Y-%m-%dT%H:%M')
        endExchangeDeadline = datetime.strptime(request.POST.get('endExchangeDeadline'), '%Y-%m-%dT%H:%M')
        blockk = request.POST.get('blockk')

        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'startExchangeDeadline': startExchangeDeadline,
            'endExchangeDeadline': endExchangeDeadline,
            'user_block': Blockk.objects.get(id=blockk)
        }

        save_deadline(data)

    return render(request, 'staff/deadline/confirm_deadline_configuration.html', data)


def show_current_deadline(request):
    deadlines = Deadline.objects.all()
    now = timezone.now()

    if (deadlines.get(name="startFPADeadline").deadline_start <= now and deadlines.get(
            name="startFPADeadline").deadline_end >= now):
        actualDeadline = "FPA"
    elif (deadlines.get(name="startAssignmentDeadline").deadline_start <= now and deadlines.get(
            name="startAssignmentDeadline").deadline_end >= now):
        actualDeadline = "Assignment"
    elif (deadlines.get(name="startExchangeDeadline").deadline_start <= now and deadlines.get(
            name="startExchangeDeadline").deadline_end >= now):
        actualDeadline = "Exchange"
    else:
        actualDeadline = "none"

    data = {
        'actualDeadline': actualDeadline
    }

    return render(request, 'staff/deadline/show_current_deadline.html', data)


@transaction.atomic
def save_deadline(data):
    Deadline.objects.all().delete()
    Deadline.objects.create(
        name="startFPADeadline",
        deadline_start=data['startFPADeadline'],
        deadline_end=data['endFPADeadline'],
        blockk=data['user_block'],
    )
    Deadline.objects.create(
        name="startAssignmentDeadline",
        deadline_start=data['startAssignmentDeadline'],
        deadline_end=data['endAssignmentDeadline'],
        blockk=data['user_block'],
    )
    Deadline.objects.create(
        name="startExchangeDeadline",
        deadline_start=data['startExchangeDeadline'],
        deadline_end=data['endExchangeDeadline'],
        blockk=data['user_block'],
    )


# professor views

@user_passes_test(is_staff)
def professors_list(request):
    professors = User.objects.filter(is_superuser=False)
    return render(request, 'staff/professor/professors_list.html', {'professors': professors})


def update_save(request):
    if request.method == 'POST':
        print("funcionou o if")
        registration_id = request.POST.get('registration_id')
        birth = request.POST.get('birth')
        date_career = request.POST.get('date_career')
        date_campus = request.POST.get('date_campus')
        date_professor = request.POST.get('date_professor')
        date_area = request.POST.get('date_area')
        date_institute = request.POST.get('date_institute')
        print(birth)

        User = get_user_model()
        user = User.objects.get(registration_id=registration_id)
        history = user.history
        print("funcionou o get user")
        if history is not None:
            history.update_history(birth=birth, date_career=date_career, date_campus=date_campus,
                                   date_professor=date_professor, date_area=date_area, date_institute=date_institute)
            history.save()
            print("funcionou o history")
        else:
            user.history = History.objects.create(birth=birth, date_career=date_career, date_campus=date_campus,
                                                  date_professor=date_professor, date_area=date_area,
                                                  date_institute=date_institute)
            user.save()
            return JsonResponse({'message': 'Histórico criado com sucesso.'})

        return JsonResponse({'message': 'Alterações salvas com sucesso.'})


# class views
@user_passes_test(is_staff)
def classes_list(request):
    classes = Classs.objects.all()
    areas = Area.objects.all()
    periods = [
        {'value': period.name, 'label': period.value}
        for period in enum.Period
    ]
    return render(request, 'staff/classs/classes_list.html', {'classes': classes, 'periods': periods, 'areas': areas})


def classes_list_saved(request):
    if request.method == 'POST':
        print("funcionou o if")
        registration_class_id = request.POST.get('registration_class_id')
        period = request.POST.get('period')
        semester = request.POST.get('semester')
        area = request.POST.get('area')
        print(area)
        print(registration_class_id)

        classs = Classs.objects.filter(registration_class_id=registration_class_id).all()
        print(classs)
        if classs is not None:
            classs.update(registration_class_id=registration_class_id, period=period, semester=semester, area=area)
            print("funcionou o history")
        else:
            classs = Classs.objects.create(registration_class_id=registration_class_id, period=period,
                                           semester=semester, area=area)
            classs.save()
            return JsonResponse({'message': 'Turma salva com sucesso.'})

        return JsonResponse({'message': 'Alterações salvas com sucesso.'})


# block views
@login_required
@user_passes_test(is_staff)
def blocks_list(request):
    blocks = request.user.blocks.all()
    return render(request, 'staff/blockk/blocks_list.html', {'blocks': blocks})

@user_passes_test(is_staff)
@user_passes_test(is_staff)
def block_detail(request, registration_block_id):
    blockk = Blockk.objects.get(registration_block_id=registration_block_id)
    area = blockk.areas.first()
    courses = Course.objects.filter(blockk=blockk)
    print("Materia", courses)
    data = {'blockk': blockk, 'area': area, 'courses': courses}

    return render(request, 'staff/blockk/block_detail.html', data)

@login_required
@user_passes_test(is_staff)
def course_create(request):
    if request.method == 'POST':
        registration_course_id = request.POST.get('registration_course_id')
        name_course = request.POST.get('name_course')
        acronym = request.POST.get('acronym')
        area_id = request.POST.get('areaId')
        block_id = request.POST.get('blockId')

        area = Area.objects.get(id=area_id)
        block = Blockk.objects.get(id=block_id)

        course = Course.objects.create(registration_course_id=registration_course_id, name_course=name_course, acronym=acronym, area=area, blockk=block)
        course.save()

        return JsonResponse({'message': 'Matéria criada com sucesso.'})

@login_required
@user_passes_test(is_staff)
def course_update_save(request):
    if request.method == 'POST':
        course_id = request.POST.get('id')
        registration_course_id = request.POST.get('registration_course_id')
        name_course = request.POST.get('name_course')
        acronym = request.POST.get('acronym')

        course = Course.objects.get(id=course_id)
        course.update_course(registration_course_id=registration_course_id, name_course=name_course, acronym=acronym)

        return JsonResponse({'message': 'Matéria atualizada com sucesso.'})

@login_required
@user_passes_test(is_staff)
def course_delete(request):
    if request.method == 'POST':
        course_id = request.POST.get('id')
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return JsonResponse({'message': 'Curso deletado com sucesso.'})
        except Course.DoesNotExist:
            return JsonResponse({'message': 'O curso não existe.'}, status=404)



@user_passes_test(is_staff)
def create_timetable(request):
    if request.method == 'GET':
        if request.GET.get('class'):
            selected_class = Classs.objects.get(registration_class_id__icontains=(request.GET.get('class')))
        else:
            selected_class = Classs.objects.all()

        selected_courses = Course.objects.filter(area=selected_class.area)

        data = {
            'courses': selected_courses,
            'timeslots': Timeslot.objects.all(),
        }

        return render(request, 'staff/timetable/cadastrar.html', data)
