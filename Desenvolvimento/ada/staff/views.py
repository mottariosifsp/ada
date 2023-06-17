from datetime import datetime, timezone
import json

from django.urls import reverse
from attribution.models import TeacherQueuePosition
# from attribution import task
from attribution.views import schedule_attributtion_deadline_staff
from enums import enum
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.utils import timezone
from timetable.models import Day_combo, Timeslot, Timetable
from .models import Deadline
from area.models import Blockk, Area
from classs.models import Classs
from course.models import Course
from user.models import User, History
from .models import Deadline, Criteria
from django.db.models import F, Sum, Value

from django.contrib.auth.decorators import login_required

tabela_data = ""

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
    if request.method == 'POST':
        blockk = Blockk.objects.get(registration_block_id=request.POST.get('blockk'))
        Deadline.objects.filter(blockk=blockk).delete()  

        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), '%Y-%m-%dT%H:%M')
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), '%Y-%m-%dT%H:%M')
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), '%Y-%m-%dT%H:%M')
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), '%Y-%m-%dT%H:%M')

        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'user_block': blockk,
        }

        save_deadline(data) 
        schedule_attributtion_deadline_staff(startAssignmentDeadline, 'startAssignmentDeadline', blockk.id)       

        return render(request, 'staff/attribution/attribution_configuration_confirm.html', data)
    return render(request, 'staff/attribution/attribution_configuration_confirm.html')

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
        selected_class = Classs.objects.get(registration_class_id__icontains=(request.GET.get('class')))
        if Timetable.objects.filter(classs=selected_class).count() > 0:
            print('já existe')
            url = reverse('edit_timetable') + f'?classs={selected_class.registration_class_id}'
            return redirect(url) 

        selected_courses = Course.objects.filter(area=selected_class.area)

        data = {
            'courses': selected_courses,
            'timeslots': Timeslot.objects.all().order_by('hour_start'),
            'classs': selected_class
        }

        return render(request, 'staff/timetable/register.html', data)
      
    if request.method == 'POST':
        message = ""
        selected_courses = json.loads(request.POST.get('selected_courses'))
        
        try:
            selected_class = Classs.objects.get(registration_class_id__exact=(request.POST.get('selected_class')))
        except Classs.DoesNotExist:
            message = "Selecione uma turma válida"
            return JsonResponse({'erro': True, 'mensagem': message})   
         
        timetable_combo_saver(selected_courses, selected_class)

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
        selected_class = get_object_or_404(Classs, registration_class_id__icontains=(request.GET.get('classs')))

        timetable_combo_saver(selected_courses, selected_class)
        
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
            'classs': selected_class,
        }

    return render(request, 'staff/timetable/show_timetable.html', data)

# def save_timetable(course, timeslot, classs, day):
#     print("'Cause she doesn't get your humor like I do")
#     print(course, timeslot, classs, day)
#     timetable, created = Timetable.objects.get_or_create(
#         day_combo__day=day,
#         day_combo__timeslots=timeslot,
#         classs=classs,
#         defaults={'course': course}
#     )
#     print(timetable, created)

#     if not created:
#         print("I'm in the room, it's a typical Tuesday night")
#         if course is None:
#             timetable.delete()
#         else:
#             print("I'm listening to the kind of music she doesn't like")
#             print(course)
#             timetable.course = course
#             timetable.save()

def save_timetable(course, classs, day_combo):
    if Timetable.objects.filter(course=course, classs=classs).exists():
        print('existe')
        timetable = Timetable.objects.get(course=course, classs=classs)
        timetable.day_combo.add(day_combo)
    else:
        timetable = Timetable.objects.create(course=course, classs=classs)
        # print(f'criado {course} no dia {day_combo.day}')
        timetable.day_combo.add(day_combo)
    
def save_combo_day(day, timeslots, course, classs):
    day_combos = Day_combo.objects.filter(day=day)
    day_combo_valid = Day_combo.objects.none()

    for day_combo in day_combos:
        if list(day_combo.timeslots.all()) == timeslots:
            day_combo_valid = day_combo

    if day_combo_valid:
        save_timetable(course, classs, day_combo_valid)
    else:
        day_combo = Day_combo.objects.create(day=day)
        day_combo.timeslots.set(timeslots)
        save_timetable(course, classs, day_combo)

def timetable_combo_saver(timetable, classs):  
    Timetable.objects.filter(classs=classs).delete()
    
    combo_number_timeslot = []
    current_course = None
    for day_week_number, day_week in enumerate(timetable):
        for timeslot, name_course in enumerate(day_week):
            if name_course:
                if current_course is None and timeslot != len(day_week)-1:
                    current_course = name_course
                    combo_number_timeslot.append(timeslot)
                elif timeslot == len(day_week)-1 and current_course == name_course:
                    combo_number_timeslot.append(timeslot)
                    timeslots = positions_to_timeslots(combo_number_timeslot)
                    print(combo_number_timeslot)
                    print(f'salvado {current_course} no dia {number_to_day_enum(day_week_number)}, nos horários {combo_number_timeslot}')
                    save_combo_day(
                        number_to_day_enum(day_week_number),
                        timeslots, 
                        Course.objects.get(name_course=current_course,area=classs.area), 
                        classs
                        )
                    combo_number_timeslot.clear()
                    current_course = None
                elif current_course is None and timeslot == len(day_week)-1:
                    current_course = name_course
                    combo_number_timeslot.append(timeslot)
                    timeslots = positions_to_timeslots(combo_number_timeslot)
                    save_combo_day(
                        number_to_day_enum(day_week_number),
                        timeslots, 
                        Course.objects.get(name_course=current_course,area=classs.area), 
                        classs
                        )
                    combo_number_timeslot.clear()
                    current_course = None
                elif timeslot == len(day_week)-1 and current_course != name_course:
                    timeslots = positions_to_timeslots(combo_number_timeslot)
                    print(combo_number_timeslot)
                    print(f'salvado {current_course} no dia {number_to_day_enum(day_week_number)}, nos horários {combo_number_timeslot}')
                    save_combo_day(
                        number_to_day_enum(day_week_number),
                        timeslots, 
                        Course.objects.get(name_course=current_course,area=classs.area), 
                        classs
                        )
                    combo_number_timeslot.clear()
                    combo_number_timeslot.append(timeslot)
                    timeslots = positions_to_timeslots(combo_number_timeslot)
                    print(combo_number_timeslot)
                    print(f'salvado {current_course} no dia {number_to_day_enum(day_week_number)}, nos horários {combo_number_timeslot}')
                    save_combo_day(
                        number_to_day_enum(day_week_number),
                        timeslots, 
                        Course.objects.get(name_course=current_course,area=classs.area), 
                        classs
                        )
                    combo_number_timeslot.clear()  
                    current_course = None
                elif current_course == name_course:
                    combo_number_timeslot.append(timeslot)
                else:
                    timeslots = positions_to_timeslots(combo_number_timeslot)
                    print(timeslots)
                    print(f'salvado {current_course} no dia {number_to_day_enum(day_week_number)}, nos horários {combo_number_timeslot}')
                    save_combo_day(
                        number_to_day_enum(day_week_number),
                        timeslots, 
                        Course.objects.get(name_course=current_course,area=classs.area), 
                        classs
                        )
                    combo_number_timeslot.clear()
                    combo_number_timeslot.append(timeslot)
                    current_course = name_course
            elif current_course is not None:
                print(f'salvado {current_course} no dia {number_to_day_enum(day_week_number)}, nos horários {combo_number_timeslot}')
                timeslots = positions_to_timeslots(combo_number_timeslot)
                save_combo_day(
                    number_to_day_enum(day_week_number),
                    timeslots, 
                    Course.objects.get(name_course=current_course,area=classs.area), 
                    classs
                    )
                current_course = None
                combo_number_timeslot.clear()

def positions_to_timeslots(positions):
    timeslot_objects = []
    for position_timeslot in positions:
        position = int(position_timeslot) + 1
        timeslot_object = Timeslot.objects.get(position=position)
        timeslot_objects.append(timeslot_object)
    return timeslot_objects

def number_to_day_enum(day_number):
    day = (
        enum.Day.monday.name,
        enum.Day.tuesday.name,
        enum.Day.wednesday.name,
        enum.Day.thursday.name,
        enum.Day.friday.name,
        enum.Day.saturday.name,
    )

    return day[day_number]


# Seleciona o campo marcado pelo administrador e verifica qual é o atributo correspondente no histórico dos usuários
def get_selected_campo():
    if Criteria.objects.filter(is_select=True).exists():
        valor_numero = Criteria.objects.filter(is_select=True).values('number_criteria').first().get('number_criteria')

        if valor_numero in range(1, 8): # 1-7, exclui o 8
            campos = {
                1: 'birth',
                2: 'date_career',
                3: 'date_campus',
                4: 'date_professor',
                5: 'date_area',
                6: 'date_institute',
                7: 'academic_degrees'
            }

            return campos.get(valor_numero, "campo")
        else:
            return ""
    else:
        return ""

def add_teacher_to_queue(teacher, position_input, blockk):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position, blockk=blockk)
    print(f'professor { teacher.first_name } adicionado na fila com a posição { position } no bloco { blockk }')


# View que leva para a(s) fila(s) já definida pelo admin
@login_required
@user_passes_test(is_staff)
def queue_show(request):
    campo = get_selected_campo()

    teacher_positions = TeacherQueuePosition.objects.order_by('position')

    total_scores = []

    for teacher_position in teacher_positions:
        user = teacher_position.teacher
        history = user.history
        total_score = history.academic_degrees.aggregate(total_score=Sum('punctuation'))['total_score']
        total_scores.append(total_score)

    resultados = teacher_positions.select_related('teacher').order_by('position').all()

    data = {
        'resultados': resultados,
        'total_scores': total_scores,
        'campo': campo,
    }

    return render(request, 'staff/queue/queue_show.html', {'data': data})


# View que leva para a página de definir a fila
@login_required
@user_passes_test(is_staff)
def queue_create(request):
    global tabela_data  # variável utilizada caso a fila já tenha sido definida pelo menos uma vez pelo admin

    if request.method == 'POST':  # adiciona os professores no model TeacherQueuePosition
        tabela_data = json.loads(request.POST['tabela_data'])
        blockk = Blockk.objects.get(registration_block_id=request.POST['blockk_id'])
        campo = get_selected_campo()

        for professorInQueue in tabela_data:
            professor_registration_id = professorInQueue[1]
            position = professorInQueue[0]
            professor = User.objects.get(registration_id=professor_registration_id)

            if TeacherQueuePosition.objects.filter(teacher=professor, blockk=blockk).exists():
                TeacherQueuePosition.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue(professor, position, blockk)

        data = {
            'resultados': TeacherQueuePosition.objects.select_related('teacher').order_by('position').all(),
            'campo': campo,
        }

        return render(request, 'staff/queue/queue_create.html', {'data': data})

    else:  # se a requisição não for POST e for GET sem ter passado a área, ou seja, sem ter atualização no filtro da área, vai cair aqui
        blockk = request.GET.get('blockk')
        print("blocoooooo:", blockk)
        blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))

        if TeacherQueuePosition.objects.filter(
                blockk=blockk).exists():  # se já tiver uma tabela criada para a área selecionada
            campo = get_selected_campo()

            teacher_positions = TeacherQueuePosition.objects.filter(blockk=blockk).order_by('position')

            all_users = User.objects.all()

            missing_users = []

            for user in all_users:
                if not teacher_positions.filter(teacher=user).exists():
                    if user.is_professor:
                        if user.blocks.filter(registration_block_id=blockk.registration_block_id).exists():
                            missing_users.append(user)

                final_list = list(teacher_positions) + missing_users

                usuarios_somados = []

                for item in final_list:
                    if isinstance(item, TeacherQueuePosition):
                        user = item.teacher
                        if user is not None and user.history is not None:
                            total_score = user.history.academic_degrees.aggregate(total_score=Sum('punctuation'))[
                                'total_score']
                        else:
                            total_score = 0
                    else:
                        user = item
                        if user is not None and user.history is not None:

                            total_score = user.history.academic_degrees.aggregate(total_score=Sum('punctuation'))[
                                'total_score']
                        else:
                            total_score = 0
                    user.total_score = total_score
                    usuarios_somados.append(user)
            data = {
                'resultados': final_list,
                'campo': campo,
                'total_score': usuarios_somados,
                'blockk': blockk
            }

            return render(request, 'staff/queue/queue_create.html', {'data': data})

        if Criteria.objects.filter(is_select=True).exists():
            campo = get_selected_campo()

            if campo != "":

                usuarios_ordenados = User.objects.filter(is_professor=True, blocks=blockk).order_by(f'history__{campo}')

                # Faz a soma dos academic degrees para cada usuário
                usuarios_somados = usuarios_ordenados.annotate(
                    total_score=Sum('history__academic_degrees__punctuation'))

                data = {
                    'resultados': usuarios_ordenados,
                    'campo': campo,
                    'total_score': usuarios_somados,
                    'blockk': blockk
                }

                return render(request, 'staff/queue/queue_create.html', {'data': data})

            else:  # se o superadmin selecionou um critério que não tenha relação com nenhum atributo do histórico vai cair aqui
                # fazer exception?

                usuarios_ordenados = User.objects.filter(is_professor=True, blocks=blockk).all()

                usuarios_somados = usuarios_ordenados.annotate(
                    total_score=Sum('history__academic_degrees__punctuation'))
                data = {
                    'resultados': usuarios_ordenados,
                    'campo': campo,
                    'total_score': usuarios_somados,
                    'blockk': blockk
                }

                return render(request, 'staff/queue/queue_create.htmll', {'data': data})

        # se nenhum critério foi selecionado pelo adm e não tiver feito nenhuma lista manual vai cair aqui
        campo = get_selected_campo()

        usuarios_ordenados = User.objects.all()
        usuarios_somados = usuarios_ordenados.annotate(total_score=Sum('history__academic_degrees__punctuation'))

        data = {
            'resultados': usuarios_ordenados,
            'campo': campo,
            'total_score': usuarios_somados,
            'blockk': blockk
        }

        return render(request, 'staff/queue/queue_create.html', {'data': data})

    