from datetime import datetime, timezone
import json
from attribution.models import TeacherQueuePosition

from enums import enum
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from attribution.views import queueSetup, queue
from django.utils import timezone
from timetable.models import Day_combo, Timeslot, Timetable
from .models import Deadline
from area.models import Blockk, Area
from classs.models import Classs
from course.models import Course
from user.models import User, History
from .models import Deadline

from django.contrib.auth.decorators import login_required

def is_staff(user):
    return user.is_staff


# prazos views

@login_required
@user_passes_test(is_staff)
def home(request):
    return render(request, 'staff/home_staff.html')

@login_required
@user_passes_test(is_staff)
def attribution_configuration_index(request):
   
    blockks = request.user.blocks.all()
    blockks_images = []

    for blockk in blockks:
        blockk_images = {
            "block": blockk,
            "image": None
        }
        if blockk.registration_block_id == "721165":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117328326533595207/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "776291":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117321570101248030/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "776293":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117321528380489789/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "776294":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1116866399952961586/dan-cristian-padure-h3kuhYUCE9A-unsplash.jpg?width=710&height=473"
        elif blockk.registration_block_id == "776295":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1116866399671951441/roonz-nl-2xEQDxB0ss4-unsplash.jpg?width=842&height=473"
        elif blockk.registration_block_id == "776292":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117348338254233680/image.png"
        blockks_images.append(blockk_images)
        print(blockks_images)
    data = {
        'blockks': blockks_images
    }
    return render(request, 'staff/attribution/attribution_configuration_index.html', data)

@login_required
@user_passes_test(is_staff)
def attribution_configuration(request):

    if request.method == 'GET':
        blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
        print(request.GET.get('blockk'))
        queue = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position')

        data = {
            'blockk': blockk,
            'queue': queue,
        }

        return render(request, 'staff/attribution/attribution_configuration.html', data)

@login_required
@user_passes_test(is_staff)
def attribution_configuration_confirm(request):
    return render(request, 'staff/attribution/attribution_configuration_confirm.html')

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
        blockk = request.POST.get('block')

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
    return render(request, 'staff/deadline/confirm_deadline_configuration.html')


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

@login_required
@user_passes_test(is_staff)
def professors_list(request):
    professors = User.objects.filter(is_superuser=False)
    return render(request, 'staff/professor/professors_list.html', {'professors': professors})

@login_required
@user_passes_test(is_staff)
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

@login_required
@user_passes_test(is_staff)
def classes_list(request):
    classes = Classs.objects.all()
    areas = Area.objects.all()
    periods = [
        {'value': period.name, 'label': period.value}
        for period in enum.Period
    ]
    return render(request, 'staff/classs/classes_list.html', {'classes': classes, 'periods': periods, 'areas': areas})

@login_required
@user_passes_test(is_staff)
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

@login_required
@user_passes_test(is_staff)
def class_create(request):
    if request.method == 'POST':
        print("funcionou o if")
        registration_class_id = request.POST.get('registration_class_id')
        period = request.POST.get('period')
        semester = request.POST.get('semester')
        area_id = request.POST.get('area')

        area = get_object_or_404(Area, id=area_id)

        classs = Classs.objects.create(registration_class_id=registration_class_id, period=period, semester=semester, area=area)
        classs.save()

        return JsonResponse({'message': 'Turma criada com sucesso.'})
    
@login_required
@user_passes_test(is_staff)
def class_delete(request):
    if request.method == 'POST':
        print("funcionou o if")
        print('id')
        print(request.POST.get('id'))
        class_id = request.POST.get('id')
        try:
            classs = Classs.objects.get(id=class_id)
            classs.delete()
            return JsonResponse({'message': 'Turma deletada com sucesso!'})
        except Course.DoesNotExist:
            return JsonResponse({'message': 'A turma não existe.'}, status=404)


# block views

@login_required
@user_passes_test(is_staff)
def blocks_list(request):
    blocks = Blockk.objects.all()

    return render(request, 'staff/blockk/blocks_list.html', {'blocks': blocks})

@login_required
@user_passes_test(is_staff)
def block_detail(request, registration_block_id):
    blockk = Blockk.objects.get(registration_block_id=registration_block_id)
    area = blockk.areas.first()
    courses = Course.objects.filter(blockk=blockk)
    print("Materia", courses)
    data = {'blockk': blockk, 'area': area, 'courses': courses}

    return render(request, 'staff/blockk/block_detail.html', data)


# course views

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
        blockk = Blockk.objects.get(id=block_id)

        course = Course.objects.create(registration_course_id=registration_course_id, name_course=name_course, acronym=acronym, area=area, blockk=blockk)
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


# fila view

@login_required
@user_passes_test(is_staff)
def queue_create(request):
    response = queueSetup(request)

    if hasattr(response, 'render') and callable(response.render):

        return response.render()

    return response

@login_required
@user_passes_test(is_staff)
def queue_show(request):
    response = queue(request)

    if hasattr(response, 'render') and callable(response.render):

        return response.render()

    return response


# timetable views

@login_required
@user_passes_test(is_staff)
def timetables(request):
    timetables = Timetable.objects.all()
    user_blocks = []
    if request.user.is_authenticated:
        user_blocks = request.user.blocks.all()
    
    user_areas = Area.objects.none()
    for user_block in user_blocks:
        area = Area.objects.filter(blocks=user_block)
        user_areas = user_areas.union(area)
    print(user_areas)
    
    classes = Classs.objects.none()
    for user_area in user_areas:
        classs = Classs.objects.filter(area=user_area)
        classes = classes.union(classs)
    print(classes)

    return render(request, 'staff/timetable/timetables.html', {'timetables': timetables, 'user_blocks': user_blocks, 'classes': classes})


@login_required
@user_passes_test(is_staff)
def create_timetable(request):
    if request.method == 'GET':
        if request.GET.get('class'):
            selected_class = Classs.objects.get(registration_class_id__icontains=(request.GET.get('class')))
            try:
                timetable = Timetable.objects.get(classs=selected_class)
            except Timetable.DoesNotExist:
                timetable = None
            selected_courses = Course.objects.filter(area=selected_class.area)
        else:
            selected_class = Classs.objects.all()
            timetable = None
            selected_courses = Course.objects.all()

        data = {
            'courses': selected_courses,
            'timeslots': Timeslot.objects.all().order_by('hour_start'),
            'classes': Classs.objects.all(),
            'timetable': timetable,
        }
        return render(request, 'staff/timetable/register.html', data)
      
    if request.method == 'POST':
        message = ""
        selected_courses = json.loads(request.POST.get('selected_courses'))
        print(selected_courses)
        bobesponja(selected_courses)
        
        try:
            selected_class = Classs.objects.get(registration_class_id__exact=(json.loads(request.POST.get('selected_class'))))
        except Classs.DoesNotExist:
            message = "Selecione uma turma válida"
            return JsonResponse({'erro': True, 'mensagem': message})    
        
        if selected_class is None:
            message = "Selecione uma turma"
            return JsonResponse({'erro': True, 'mensagem': message})
        for courses in selected_courses:
            for name_course in courses:
                if name_course:     
                    if not Course.objects.filter(name_course=name_course).exists():
                        message = "Selecione uma matéria válida"
                        return JsonResponse({'erro': True, 'mensagem': message})                    
        
        for day_number, courses in enumerate(selected_courses):
            for position, name_course in enumerate(courses):
                timeslot = Timeslot.objects.get(position=position+1)
                course = None
                day = None
                if(day_number==0):
                    day = enum.Day.monday.name
                elif(day_number==1):
                    day = enum.Day.tuesday.name
                elif(day_number==2):
                    day = enum.Day.wednesday.name
                elif(day_number==3):
                    day = enum.Day.thursday.name
                elif(day_number==4):
                    day = enum.Day.friday.name
                elif(day_number==5):
                    day = enum.Day.saturday.name              
                if name_course:                
                    course = Course.objects.get(name_course=name_course)
                    save_timetable(course, timeslot, selected_class, day)
                    print("You're on the phone with your girlfriend, she's upset")
                else:
                    save_timetable(None, timeslot, selected_class, day)
                    print("She's going off about something that you said")
        return JsonResponse({'erro': False, 'mensagem': message})
    
@login_required
@user_passes_test(is_staff)
def edit_timetable(request):
    print(request)
    if request.method == 'GET':
        if request.GET.get('classs'):
            # selected_class = Classs.objects.get(registration_class_id__icontains=(request.GET.get('classs')))
            selected_class = get_object_or_404(Classs, registration_class_id__icontains=(request.GET.get('classs')))
            try:
                timetable = Timetable.objects.get(classs=selected_class)
                selected_courses = [timetable.course] if timetable.course else []
            except Timetable.DoesNotExist:
                timetable = None
                selected_courses = Course.objects.filter(area=selected_class.area)
            
            data = {
                'courses': selected_courses,
                'timeslots': Timeslot.objects.all().order_by('hour_start'),
                'classs': selected_class,
                'timetable': timetable,
            }            
    
    elif request.method == 'POST':
        message = ""
        selected_courses = json.loads(request.POST.get('selected_courses'))
        print(selected_courses)
        bobesponja(selected_courses)
        
        for courses in selected_courses:
            for name_course in courses:
                if name_course and not Course.objects.filter(name_course=name_course).exists():
                        message = "Selecione uma matéria válida"
                        return JsonResponse({'erro': True, 'mensagem': message})                    
        
        for day_number, courses in enumerate(selected_courses):
            for position, name_course in enumerate(courses):
                timeslot = Timeslot.objects.get(position=position+1)
                course = None
                day = None
                if(day_number==0):
                    day = enum.Day.monday.name
                elif(day_number==1):
                    day = enum.Day.tuesday.name
                elif(day_number==2):
                    day = enum.Day.wednesday.name
                elif(day_number==3):
                    day = enum.Day.thursday.name
                elif(day_number==4):
                    day = enum.Day.friday.name
                elif(day_number==5):
                    day = enum.Day.saturday.name              
                if name_course:                
                    course = Course.objects.get(name_course=name_course)
                    save_timetable(course, timeslot, selected_class, day)
                    print("Want you to make me feel like I'm the only girl in the world")
                else:
                    save_timetable(None, timeslot, selected_class, day)
                    print("Like I'm the only one that you'll ever love")
        return JsonResponse({'erro': False, 'mensagem': message})
    return render(request, 'staff/timetable/show_timetable.html', data)

@login_required
@user_passes_test(is_staff)
def show_timetable(request):
    if request.method == 'GET':
        selected_class = Classs.objects.get(registration_class_id__exact=(request.GET.get('class')))
        timetables = Timetable.objects.filter(classs=selected_class).all()
        day_combos = Day_combo.objects.all() # .filter(classs=selected_class)

        data = {
            'timetables': timetables,
            'timeslots': Timeslot.objects.all().order_by('hour_start'),
            'day_combos': day_combos,
        }

    return render(request, 'staff/timetable/show_timetable.html', data)

def save_timetable(course, timeslot, classs, day):
    print("'Cause she doesn't get your humor like I do")
    print(course, timeslot, classs, day)
    timetable, created = Timetable.objects.get_or_create(
        day_combo__day=day,
        day_combo__timeslots=timeslot,
        classs=classs,
        defaults={'course': course}
    )
    print(timetable, created)

    if not created:
        print("I'm in the room, it's a typical Tuesday night")
        if course is None:
            timetable.delete()
        else:
            print("I'm listening to the kind of music she doesn't like")
            print(course)
            timetable.course = course
            timetable.save()


def save_combo_day(day, timeslots):
    day_combo, created = Day_combo.objects.get_or_create(day=day)
    day_combo.timeslots.set(timeslots)
    print("But she wears short skirts")
    print(day_combo, created)

def bobesponja(timetable):
    Day_combo.objects.all().delete()
    timetable_clear = []
    for element in timetable:
        if not element == '':
            timetable_clear.append(element)

    print("Time table clear", timetable_clear)
    combo_timeslot = []
    current_course = None
    for day_week_number, day_week in enumerate(timetable):
        print("dayywekk", day_week)
        for timeslot, name_course in enumerate(day_week):
            if current_course is None:
                current_course = name_course
                combo_timeslot.append(timeslot)
            elif current_course == name_course:
                combo_timeslot.append(timeslot)
            elif current_course != name_course or len(day_week-1):

                queryset_timeslots = []
                print("Tipo do combo time slot", type(combo_timeslot))
                print(" combo time slot", combo_timeslot)
                for position_timeslot in combo_timeslot:
                    position = combo_timeslot.index(position_timeslot)
                    print("Posiçãoooooooooooooooooooo oooooooooooooooooo:", position)
                    print(" combo time slot dentro do for", combo_timeslot)
                    timeslot = Timeslot.objects.get(position=position + 1)
                    queryset_timeslots.append(timeslot)
                    print("Query set", queryset_timeslots)
                print(f'salvado {current_course} no dia {number_to_day_enum(day_week_number)}, nos horários {combo_timeslot}')
                save_combo_day(number_to_day_enum(day_week_number), queryset_timeslots)

                combo_timeslot = []
                combo_timeslot.append(timeslot)
                current_course = None

def number_to_day_enum(day_number):
    if(day_number==0):
        return enum.Day.monday.name
    elif(day_number==1):
        return enum.Day.tuesday.name
    elif(day_number==2):
        return enum.Day.wednesday.name
    elif(day_number==3):
        return enum.Day.thursday.name
    elif(day_number==4):
        return enum.Day.friday.name
    elif(day_number==5):
        return enum.Day.saturday.name        

    

