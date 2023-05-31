from datetime import datetime
from enums import enum
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .models import Deadline
from _class.models import Class
from area.models import Block, Area
from course.models import Course
from user.models import User, History
from django.utils import timezone


def is_staff(user):
    return user.is_staff


# prazos

@user_passes_test(is_staff)
def home(request):
    return render(request, 'staff/home.html')


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
        block = request.POST.get('block')

        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'startExchangeDeadline': startExchangeDeadline,
            'endExchangeDeadline': endExchangeDeadline,
            'user_block': Block.objects.get(id=block)
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
        block=data['user_block'],
    )
    Deadline.objects.create(
        name="startAssignmentDeadline",
        deadline_start=data['startAssignmentDeadline'],
        deadline_end=data['endAssignmentDeadline'],
        block=data['user_block'],
    )
    Deadline.objects.create(
        name="startExchangeDeadline",
        deadline_start=data['startExchangeDeadline'],
        deadline_end=data['endExchangeDeadline'],
        block=data['user_block'],
    )


# professor views

@user_passes_test(is_staff)
def professors_list(request):
    professors = User.objects.filter(is_superuser=False)
    return render(request, 'staff/professors_list.html', {'professors': professors})


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
    classes = Class.objects.all()
    areas = Area.objects.all()
    periods = [
        {'value': period.name, 'label': period.value}
        for period in enum.Period
    ]
    return render(request, 'staff/classes_list.html', {'classes': classes, 'periods': periods, 'areas': areas})

def classes_list_saved(request):
    if request.method == 'POST':
        print("funcionou o if")
        registration_class_id = request.POST.get('registration_class_id')
        period = request.POST.get('period')
        semester = request.POST.get('semester')
        area = request.POST.get('area')
        print(area)

        Class = get_user_model()
        _class = Class.objects.all()
        print("funcionou o get user")
        if _class is not None:
            _class.update_class(registration_class_id=registration_class_id, period=period, semester=semester, area=area)
            _class.save()
            print("funcionou o history")
        else:            
            _class = Class.objects.create(registration_class_id=registration_class_id, period=period, semester=semester, area=area)
            _class.save()
            return JsonResponse({'message': 'Turma salva com sucesso.'})
        
        # _class = Class.objects.all()
        # print("funcionou o get user")
        # if _class.exists():
        #     _class.update_class(registration_class_id=registration_class_id, period=period, semester=semester, area=area)
        #     print("funcionou o history")
        # else:            
        #     _class = Class.objects.create(registration_class_id=registration_class_id, period=period, semester=semester, area=area)
        #     return JsonResponse({'message': 'Turma salva com sucesso.'})

        return JsonResponse({'message': 'Alterações salvas com sucesso.'})
    
    return JsonResponse({'error': 'Método inválido'}, status=400)

# block views
@user_passes_test(is_staff)
def blocks_list(request):
    blocks = request.user.blocks.all()
    return render(request, 'staff/block/blocks_list.html', {'blocks': blocks})


@user_passes_test(is_staff)
def block_detail(request, registration_block_id):
    block = Block.objects.get(registration_block_id=registration_block_id)
    area = block.areas.first()
    courses = Course.objects.filter(block=block)
    print("Materia", courses)
    data = {'block': block, 'area': area, 'courses': courses}
    return render(request, 'staff/block/block_detail.html', data)


def course_update_save(request):
    if request.method == 'POST':
        course_id = request.POST.get('id')
        print("idd", course_id)
        registration_course_id = request.POST.get('registration_course_id')
        name_course = request.POST.get('name_course')
        acronym = request.POST.get('acronym')

        course = Course.objects.get(id=course_id)
        print("cursos", course)
        course.update_course(registration_course_id=registration_course_id, name_course=name_course, acronym=acronym)
        print("cursos", course)

        return JsonResponse({'message': 'Matéria atualizada com sucesso.'})
