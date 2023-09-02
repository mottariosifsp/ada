from datetime import datetime, time, timezone
import json

from django.urls import reverse
from attribution.models import TeacherQueuePosition, TeacherQueuePositionBackup
# from attribution import task
from attribution.views import schedule_attributtion_deadline_staff
from enums.enum import Job, Period, Day
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.utils import timezone
from timetable.models import Day_combo, Timeslot, Timetable, Timetable_user
from area.models import Blockk, Area
from classs.models import Classs
from course.models import Course
from user.models import AcademicDegreeHistory, User, History, AcademicDegree
from .models import Deadline, Criteria
from django.db.models import F, Sum, Value
from staff.models import Deadline
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required

from common.date_utils import day_to_number

def is_staff(user):
    return user.is_staff

# prazos views

@login_required
@user_passes_test(is_staff)
def home(request):
    status = 'not_configured'
    period = {
        'status': status,
        'start_day': '',
        'start_time': '',
        'end_day': '',
        'end_time': ''
    }

    def get_stage_status(stage_name):
        deadlines = Deadline.objects.filter(name=stage_name)

        if not deadlines.exists():
            return 'not_configured'

        now = datetime.today()
        nearest_deadline = None
        nearest_time_difference = timedelta(days=365)  # Set to a large value initially

        for deadline in deadlines:
            if deadline.deadline_start <= now <= deadline.deadline_end:                
                return 'ongoing'
            if now <= deadline.deadline_start:
                time_difference = deadline.deadline_start - now                
                if time_difference < nearest_time_difference:
                    nearest_time_difference = time_difference
                    nearest_deadline = deadline
                

        if nearest_deadline:
            return 'configured_' + stage_name

        return 'finished'

    fpa_status = get_stage_status('STARTFPADEADLINE')
    attribution_status = get_stage_status('STARTASSIGNMENTDEADLINE')
    # enchange_status = get_stage_status('STARTENCHANGEDEADLINE')

    if fpa_status == 'finished' and attribution_status == 'finished':
        status = 'finished'

    print(fpa_status, attribution_status)

    if fpa_status == 'ongoing':
        status = 'fpa'
    elif attribution_status == 'ongoing':
        status = 'attribution'
    # elif enchange_status == 'ongoing':
    #     status = 'enchange'

    if fpa_status.startswith('configured_'):
        status = fpa_status
    elif attribution_status.startswith('configured_'):
        status = attribution_status
    # elif enchange_status.startswith('configured_'):
    #     status = enchange_status

    if status != 'not_configured' and status != 'finished':
        if fpa_status == 'ongoing':
            status = 'fpa'
            fpa_deadline = Deadline.objects.filter(name='STARTFPADEADLINE').first()
            if fpa_deadline:
                period['start_day'] = fpa_deadline.deadline_start.strftime("%d/%m/%Y")
                period['start_time'] = fpa_deadline.deadline_start.strftime("%H:%M")
                period['end_day'] = fpa_deadline.deadline_end.strftime("%d/%m/%Y")
                period['end_time'] = fpa_deadline.deadline_end.strftime("%H:%M")
        elif attribution_status == 'ongoing':
            status = 'attribution'
            attribution_deadline = Deadline.objects.filter(name='STARTASSIGNMENTDEADLINE').first()
            if attribution_deadline:
                period['start_day'] = attribution_deadline.deadline_start.strftime("%d/%m/%Y")
                period['start_time'] = attribution_deadline.deadline_start.strftime("%H:%M")
                period['end_day'] = attribution_deadline.deadline_end.strftime("%d/%m/%Y")
                period['end_time'] = attribution_deadline.deadline_end.strftime("%H:%M")
        # elif enchange_status == 'ongoing':
        #     status = 'enchange'
        #     enchange_deadline = Deadline.objects.filter(name='STARTENCHANGEDEADLINE').first()
        #     if enchange_deadline:
        #         period['start_day'] = enchange_deadline.deadline_start.strftime("%d/%m/%Y")
        #         period['start_time'] = enchange_deadline.deadline_start.strftime("%H:%M")
        #         period['end_day'] = enchange_deadline.deadline_end.strftime("%d/%m/%Y")
        #         period['end_time'] = enchange_deadline.deadline_end.strftime("%H:%M")
        else:
            stage_name = status.split('_')[1]
            nearest_deadline = Deadline.objects.filter(name=stage_name).first()
            if nearest_deadline:
                period['status'] = status
                period['start_day'] = nearest_deadline.deadline_start.strftime("%d/%m/%Y")
                period['start_time'] = nearest_deadline.deadline_start.strftime("%H:%M")
                period['end_day'] = nearest_deadline.deadline_end.strftime("%d/%m/%Y")
                period['end_time'] = nearest_deadline.deadline_end.strftime("%H:%M")

    period['status'] = status
        
    data = {
        'period': period
    }
    return render(request, 'staff/home_staff.html', data)

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
    data = {
        'blockks': blockks_images
    }
    return render(request, 'staff/attribution/attribution_configuration_index.html', data)

@login_required
@user_passes_test(is_staff)
def attribution_configuration(request):

    if request.method == 'GET':
        blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
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

        date_format = "%Y-%m-%dT%H:%M"

        startFPADeadline = datetime.strptime(request.POST.get('startFPADeadline'), date_format)
        endFPADeadline = datetime.strptime(request.POST.get('endFPADeadline'), date_format)
        startAssignmentDeadline = datetime.strptime(request.POST.get('startAssignmentDeadline'), date_format)
        endAssignmentDeadline = datetime.strptime(request.POST.get('endAssignmentDeadline'), date_format)

        print(startFPADeadline)

        data = {
            'startFPADeadline': startFPADeadline,
            'endFPADeadline': endFPADeadline,
            'startAssignmentDeadline': startAssignmentDeadline,
            'endAssignmentDeadline': endAssignmentDeadline,
            'user_block': blockk,
        }
        for time in Timetable_user.objects.all():
            time.user = None
            time.save()

        save_deadline(data) 
        schedule_attributtion_deadline_staff(startAssignmentDeadline, 'startAssignmentDeadline', blockk.id)       


        return render(request, 'staff/attribution/attribution_configuration_confirm.html', data)
    return render(request, 'staff/attribution/attribution_configuration_confirm.html')

@transaction.atomic
def save_deadline(data):
    Deadline.objects.create(
        name="STARTFPADEADLINE",
        deadline_start=data['startFPADeadline'],
        deadline_end=data['endFPADeadline'],
        blockk=data['user_block'],
    )
    Deadline.objects.create(
        name="STARTASSIGNMENTDEADLINE",
        deadline_start=data['startAssignmentDeadline'],
        deadline_end=data['endAssignmentDeadline'],
        blockk=data['user_block'],
    )

# professor views
@login_required
@user_passes_test(is_staff)
def professors_list(request):
    professors = User.objects.filter(is_superuser=False)
    degrees = AcademicDegree.objects.all()
    blockks = Blockk.objects.all()
    data = {
        'professors': professors,
        'degrees': degrees,
        'blockks': blockks
    }

    return render(request, 'staff/professor/professors_list.html', data)


@login_required
@user_passes_test(is_staff)
def add_new_professor(request):
    if request.method == 'POST':
        registration_id = request.POST.get('add_registration_id')
        first_name = request.POST.get('add_first_name')
        last_name = request.POST.get('add_last_name')
        email = request.POST.get('add_email')
        telephone = request.POST.get('add_telephone')
        celphone = request.POST.get('add_celphone')
        birth = request.POST.get('add_birth')
        date_career = request.POST.get('add_date_career')
        date_campus = request.POST.get('add_date_campus')
        date_professor = request.POST.get('add_date_professor')
        date_area = request.POST.get('add_date_area')
        date_institute = request.POST.get('add_date_institute')
        job = request.POST.get('add_job')
        academic_degrees_json = request.POST.get('add_academic_degrees')
        blocks_json = request.POST.get('add_blocks')
        is_professor = request.POST.get('add_is_professor') == 'true'
        is_staff = request.POST.get('add_is_staff') == 'true'
        is_fgfcc = request.POST.get('add_is_fgfcc') == 'true'   
        
        job_obj = Job(job).name

        new_user = User.objects.create(
            registration_id=registration_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            cell_phone=celphone,
            job=job_obj,
            is_professor=is_professor,
            is_staff=is_staff,
            is_fgfcc=is_fgfcc
            )
        
        blocks = json.loads(blocks_json)
        for block in blocks:
            block_obj = Blockk.objects.get(name_block=block)
            new_user.blocks.add(block_obj)
        new_user.save()
        
        if new_user.history is not None:
            academic_degrees = []
            if academic_degrees_json:
                academic_degrees = json.loads(academic_degrees_json)
                for degree_data in academic_degrees:
                    degree_obj = AcademicDegree.objects.get(name=degree_data)
                    AcademicDegreeHistory.objects.create(history=new_user.history, academic_degree=degree_obj)

            new_user.history.update_history(birth=birth, date_career=date_career, date_campus=date_campus,
                                   date_professor=date_professor, date_area=date_area, date_institute=date_institute,
                                   academic_degrees=academic_degrees)

            new_user.history.save()
        else:
            new_user.history = History.objects.create(birth=birth, date_career=date_career, date_campus=date_campus,
                                                  date_professor=date_professor, date_area=date_area,
                                                  date_institute=date_institute)
            academic_degrees = []
            if academic_degrees_json:
                academic_degrees = json.loads(academic_degrees_json)
                for degree_data in academic_degrees:
                    degree_obj = AcademicDegree.objects.get(name=degree_data)
                    AcademicDegreeHistory.objects.create(history=new_user.history, academic_degree=degree_obj)

            new_user.save()
            return JsonResponse({'message': 'Histórico criado com sucesso.'})

@login_required
@user_passes_test(is_staff)
def update_save(request):
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        celphone = request.POST.get('celphone')
        birth = request.POST.get('birth')
        date_career = request.POST.get('date_career')
        date_campus = request.POST.get('date_campus')
        date_professor = request.POST.get('date_professor')
        date_area = request.POST.get('date_area')
        date_institute = request.POST.get('date_institute')
        job = request.POST.get('job')
        academic_degrees_json = request.POST.get('academic_degrees')
        blocks_json = request.POST.get('blocks')
        is_professor = request.POST.get('is_professor') == 'true'
        is_staff = request.POST.get('is_staff')  == 'true'
        is_fgfcc = request.POST.get('is_fgfcc')  == 'true'

        
        # User = get_user_model()
        job_obj = Job(job).name

        user = User.objects.get(registration_id=registration_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.telephone = telephone
        user.cell_phone = celphone
        user.job = job_obj
        user.is_professor = is_professor
        user.is_staff = is_staff
        user.is_fgfcc = is_fgfcc

        blocks = json.loads(blocks_json)
        for block in blocks:
            block_obj = Blockk.objects.get(name_block=block)
            user.blocks.add(block_obj)
        user.save()

        history = user.history
        
        history.academic_degrees.clear()
        if history is not None:
            academic_degrees = []
            if academic_degrees_json:
                academic_degrees = json.loads(academic_degrees_json)
                for degree_data in academic_degrees:
                    print('adicionando: ', degree_data, ' ao historico')
                    degree_obj = AcademicDegree.objects.get(name=degree_data)
                    AcademicDegreeHistory.objects.create(history=history, academic_degree=degree_obj)

            history.update_history(birth=birth, date_career=date_career, date_campus=date_campus,
                                   date_professor=date_professor, date_area=date_area, date_institute=date_institute)

            history.save()
        else:
            user.history = History.objects.create(birth=birth, date_career=date_career, date_campus=date_campus,
                                                  date_professor=date_professor, date_area=date_area,
                                                  date_institute=date_institute)
            academic_degrees = []
            if academic_degrees_json:
                academic_degrees = json.loads(academic_degrees_json)
                for degree_data in academic_degrees:
                    degree_obj = AcademicDegree.objects.get(name=degree_data)
                    history.academic_degrees.add(degree_obj)

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
        for period in Period
    ]
    return render(request, 'staff/classs/classes_list.html', {'classes': classes, 'periods': periods, 'areas': areas})

# ERRO - TODO
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

# Erro - TODO
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

# Erro - TODO
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
    user_blocks = request.user.blocks.all()
    blockk = Blockk.objects.get(registration_block_id=registration_block_id)
    area = blockk.areas.first()
    courses = Course.objects.filter(blockk=blockk)
    print("Materia", courses)
    data = {
        'user_blocks': user_blocks,
        'blockk': blockk, 
        'area': area, 
        'courses': courses
    }

    return render(request, 'staff/blockk/block_detail.html', data)

# course views
@login_required
@user_passes_test(is_staff)
def course_create(request):
    user_blocks = request.user.blocks.all()
    if request.method == 'POST':
        registration_course_id = request.POST.get('registration_course_id')
        name_course = request.POST.get('name_course')
        acronym = request.POST.get('acronym')
        area_id = request.POST.get('areaId')
        block_id = request.POST.get('blockId')

        area = Area.objects.get(id=area_id)
        blockk = Blockk.objects.get(id=block_id)
        if blockk in user_blocks:

            course = Course.objects.create(registration_course_id=registration_course_id, name_course=name_course, acronym=acronym, area=area, blockk=blockk)
            course.save()

            return JsonResponse({'message': 'Disciplina criada com sucesso.'})
        else:
            return JsonResponse({'message': 'Você não tem permissão para criar disciplinas nesse bloco.'})

@login_required
@user_passes_test(is_staff)
def course_update_save(request):
    if request.method == 'POST':
        course_id = request.POST.get('id')
        registration_course_id = request.POST.get('registration_course_id')
        name_course = request.POST.get('name_course')
        acronym = request.POST.get('acronym')

        course = Course.objects.get(id=course_id)
        blockk = course.blockk

        if blockk in request.user.blocks.all():
            course.update_course(registration_course_id=registration_course_id, name_course=name_course, acronym=acronym)

            return JsonResponse({'message': 'Disciplina atualizada com sucesso.'})
        else:
            return JsonResponse({'message': 'Você não tem permissão para editar disciplinas nesse bloco.'})

@login_required
@user_passes_test(is_staff)
def course_delete(request):
    if request.method == 'POST':
        course_id = request.POST.get('id')
        try:
            course = Course.objects.get(id=course_id)
            if course.blockk in request.user.blocks.all():
                course.delete()
                return JsonResponse({'message': 'Disciplina deletado com sucesso.'})
            else:
                return JsonResponse({'message': 'Você não tem permissão para deletar disciplinas nesse bloco.'})
        except Course.DoesNotExist:
            return JsonResponse({'message': 'O disciplina não existe.'}, status=404)

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
        timeslots = {
            'morning': Timeslot.objects.filter(hour_start__gte=time(6, 0, 0), hour_end__lte=time(12, 0, 0)).order_by('hour_start'),
            'afternoon': Timeslot.objects.filter(hour_start__gte=time(12, 0, 0), hour_end__lte=time(18, 0, 0)).order_by('hour_start'),
            'night': Timeslot.objects.filter(hour_start__gte=time(18, 0, 0), hour_end__lte=time(23, 59, 59)).order_by('hour_start'),
        }
        data = {
            'courses': selected_courses,
            'timeslots': timeslots,
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
        

        for day_week in selected_courses:
            for course_name in day_week:
                if(course_name == ''):
                    continue
                try:
                    course = Course.objects.get(registration_course_id=course_name)
                    course_name=course
                except Course.DoesNotExist:
                    message = "Selecione uma disciplina válida"
                    return JsonResponse({'erro': True, 'mensagem': message})

        timetable_combo_saver(selected_courses, selected_class)

        return JsonResponse({'erro': False, 'mensagem': message})
    
@login_required
@user_passes_test(is_staff)
def edit_timetable(request):
    print(request)
    if request.method == 'GET':
        selected_class = Classs.objects.get(registration_class_id__icontains=(request.GET.get('class')))
        selected_courses = Course.objects.filter(area=selected_class.area)

        timetables = Timetable.objects.filter(classs=selected_class)
        timeslots = Timeslot.objects.all().order_by('hour_start')

        timetable_complete = []

        for timetable in timetables:
            day_combos = timetable.day_combo.all()
            for day_combo in day_combos:
                day = day_to_number(day_combo.day)
                timeslots = day_combo.timeslots.all()

                for timeslot in timeslots:

                    position = timeslot.position
                    timetable_professor = {
                        "cord": f'{position}-{day}',
                        "course": timetable.course.name_course,
                        "acronym": timetable.course.acronym,
                        "id": timetable.course.registration_course_id,
                    }
                    timetable_complete.append(timetable_professor)

        timetable_complete_json = json.dumps(timetable_complete, ensure_ascii=False).encode('utf8').decode()

        print(timetable_complete)
        # print(selected_courses)
        data = {
            'courses': selected_courses,
            'timeslots': Timeslot.objects.all().order_by('hour_start'),
            'timetable': timetable_complete_json,
            'classs': selected_class,
        }
        return render(request, 'staff/timetable/edit_timetable.html', data)

    elif request.method == 'POST':
        message = ""
        selected_courses = json.loads(request.POST.get('selected_courses'))
        
        try:
            selected_class = Classs.objects.get(registration_class_id__exact=(request.POST.get('selected_class')))
        except Classs.DoesNotExist:
            message = "Selecione uma turma válida"
            return JsonResponse({'erro': True, 'mensagem': message})   
        

        for day_week in selected_courses:
            for course_name in day_week:
                if(course_name == ''):
                    continue
                try:
                    course = Course.objects.get(registration_course_id=course_name)
                    course_name=course
                except Course.DoesNotExist:
                    message = "Selecione uma disciplina válida"
                    return JsonResponse({'erro': True, 'mensagem': message})

        timetable_combo_saver(selected_courses, selected_class)

        return JsonResponse({'erro': False, 'mensagem': message})

@login_required
@user_passes_test(is_staff)
def show_timetable(request):
    if request.method == 'GET':
        selected_class = Classs.objects.get(registration_class_id__exact=(request.GET.get('class')))
        timetables = Timetable.objects.filter(classs=selected_class).all()
        
        timeslots = Timeslot.objects.all().order_by('hour_start')

        timetable_complete = []

        for timetable in timetables:
            day_combos = timetable.day_combo.all()
            for day_combo in day_combos:
                day = day_to_number(day_combo.day)
                timeslots = day_combo.timeslots.all()

                for timeslot in timeslots:

                    position = timeslot.position
                    timetable_professor = {
                        "cord": f'{position}-{day}',
                        "course": timetable.course.name_course,
                        "acronym": timetable.course.acronym,
                    }
                    timetable_complete.append(timetable_professor)

        timetable_complete_json = json.dumps(timetable_complete, ensure_ascii=False).encode('utf8').decode()

        data = {
            'timeslots': Timeslot.objects.all().order_by('hour_start'),
            'timetables': timetable_complete_json,
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

def enum_to_day_number(day):
    day_number = (
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',        
    )
    return day_number.index(day)

def save_timetable(course, classs, day_combo):
    if Timetable.objects.filter(course=course, classs=classs).exists():
        print('existe')
        timetable = Timetable.objects.get(course=course, classs=classs)
        timetable.day_combo.add(day_combo)
    else:
        timetable = Timetable.objects.create(course=course, classs=classs)
        # print(f'criado {course} no dia {day_combo.day}')
        timetable.day_combo.add(day_combo)
        Timetable_user.objects.create(timetable=timetable, user=None)
        
    
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
                        Course.objects.get(registration_course_id=current_course,area=classs.area),
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
                        Course.objects.get(registration_course_id=current_course,area=classs.area), 
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
                        Course.objects.get(registration_course_id=current_course,area=classs.area), 
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
                        Course.objects.get(registration_course_id=current_course,area=classs.area), 
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
                        Course.objects.get(registration_course_id=current_course,area=classs.area), 
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
                    Course.objects.get(registration_course_id=current_course,area=classs.area), 
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
        Day.monday.name,
        Day.tuesday.name,
        Day.wednesday.name,
        Day.thursday.name,
        Day.friday.name,
        Day.saturday.name,
    )

    return day[day_number]


# Seleciona o campo marcado pelo administrador e verifica qual é o atributo correspondente no histórico dos usuários
def get_selected_field():
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

# método para deixar separado no html
def get_string_field(campo):
    campos = {
        'birth': 'Data de nascimento',
        'date_career': 'Data de carreira',
        'date_campus': 'Data no campus',
        'date_professor': 'Data como professor',
        'date_area': 'Data na área',
        'date_institute': 'Data no instituto',
        'academic_degrees': 'Pontuação de titulação',
        '':''
    }

    return campos.get(campo, "campo")

def calculate_total_score(user, is_in_teacher_queue):
    if is_in_teacher_queue:
        if user.teacher.history and user.teacher.history.academic_degrees.exists():
            return user.teacher.history.academic_degrees.aggregate(Sum('punctuation'))['punctuation__sum']
        else:
            return 0
    else:
        if user.history and user.history.academic_degrees.exists():
            return user.history.academic_degrees.aggregate(Sum('punctuation'))['punctuation__sum']
        else:
            return 0

def add_teacher_to_queue(teacher, position_input, blockk):
    position = position_input
    TeacherQueuePosition.objects.create(teacher=teacher, position=position, blockk=blockk)
    print(f'professor { teacher.first_name } adicionado na fila com a posição { position } no bloco { blockk }')

def add_teacher_to_queue_backup(teacher, position_input, blockk):
    position = position_input
    TeacherQueuePositionBackup.objects.create(teacher=teacher, position=position, blockk=blockk)
    print(f'professor { teacher.first_name } adicionado na fila de backup com a posição { position } no bloco { blockk }')

# View que leva para a(s) fila(s) já definida pelo admin
@login_required
@user_passes_test(is_staff)
def queue_show(request):
    blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))
    teacher_positions = TeacherQueuePositionBackup.objects.filter(blockk=blockk).order_by('position').all()

    total_scores = []

    for teacher_position in teacher_positions:
        user = teacher_position.teacher
        history = user.history

        if history is not None:
            if history.academic_degrees is not None:
                total_score = history.academic_degrees.aggregate(total_score=Sum('punctuation'))['total_score']
                total_scores.append(total_score)

    results = teacher_positions.select_related('teacher').order_by('position').all()

    data = {
        'results': results,
        'total_scores': total_scores,
    }

    return render(request, 'staff/queue/queue_show.html', {'data': data})


# View que leva para a página de definir a fila
@login_required
@user_passes_test(is_staff)
def queue_create(request):
    table_data = []  # variável utilizada caso a fila já tenha sido definida pelo menos uma vez pelo admin

    if request.method == 'POST':  # adiciona os professores no model TeacherQueuePosition
        table_data = json.loads(request.POST['table_data'])

        blockk = Blockk.objects.get(registration_block_id=request.POST['blockk_id'])
        field = get_selected_field()

        for professor_in_queue in table_data:
            professor_registration_id = professor_in_queue[1]
            position = professor_in_queue[0]
            professor = User.objects.get(registration_id=professor_registration_id)

            if TeacherQueuePositionBackup.objects.filter(teacher=professor, blockk=blockk).exists():
                TeacherQueuePositionBackup.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue_backup(professor, position, blockk)

            if TeacherQueuePosition.objects.filter(teacher=professor, blockk=blockk).exists():
                TeacherQueuePosition.objects.filter(teacher=professor).update(position=position)
            else:
                add_teacher_to_queue(professor, position, blockk)

        data = {
            'results': TeacherQueuePositionBackup.objects.select_related('teacher').order_by('position').all(),
            'field': get_string_field(field),
        }

        return render(request, 'staff/queue/queue_create.html', {'data': data})

    else:
        blockk = request.GET.get('blockk')
        blockk = Blockk.objects.get(registration_block_id=request.GET.get('blockk'))

        if TeacherQueuePositionBackup.objects.filter(
                blockk=blockk).exists():  # se já tiver uma fila de professores criada
            field = get_selected_field()

            teacher_positions = TeacherQueuePositionBackup.objects.filter(blockk=blockk).order_by('position')

            all_users = User.objects.all()

            missing_users = []

            for user in all_users:
                if not TeacherQueuePositionBackup.objects.filter(teacher=user).exists():
                    if user.is_professor:
                        if user.blocks.filter(registration_block_id=blockk.registration_block_id).exists():
                            missing_users.append(user)

            final_list = list(teacher_positions) + missing_users
            summed_users = []

            for item in final_list:
                if isinstance(item, TeacherQueuePositionBackup):
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
                summed_users.append(user)

            scores_users = []
            for user in final_list:
                user_score = calculate_total_score(user, True)
                scores_users.append(user_score)

            data = {
                'results': final_list,
                'field': get_string_field(field),
                'total_score': scores_users,
                'blockk': blockk,
                'recover_queue': True
            }

            return render(request, 'staff/queue/queue_create.html', {'data': data})

        if Criteria.objects.filter(is_select=True).exists():
            field = get_selected_field()

            if field != "":
                if field != "academic_degrees":

                    users_ordered = User.objects.filter(is_professor=True, blocks=blockk).order_by(
                        F(f'history__{field}').asc(nulls_last=True))

                else:
                    users_ordered_by_certificate = User.objects.filter(is_professor=True, blocks=blockk)
                    is_in_teacher_queue = False
                    users_ordered = sorted(users_ordered_by_certificate,
                                           key=lambda user: calculate_total_score(user, is_in_teacher_queue),
                                           reverse=True)

                scores_users = []
                for user in users_ordered:
                    user_score = calculate_total_score(user, False)
                    scores_users.append(user_score)

                data = {
                    'results': users_ordered,
                    'field': get_string_field(field),
                    'total_score': scores_users,
                    'blockk': blockk
                }

                return render(request, 'staff/queue/queue_create.html', {'data': data})

            else:  # se o superadmin selecionou um critério que não tenha relação com nenhum atributo do histórico vai cair aqui
                users_ordered = User.objects.filter(is_professor=True, blocks=blockk).order_by(
                    F('history__birth').asc(nulls_last=True))

                scores_users = []
                for user in users_ordered:
                    user_score = calculate_total_score(user, False)
                    scores_users.append(user_score)

                data = {
                    'results': users_ordered,
                    'field': get_string_field("birth"),
                    'error_field': True,
                    'total_score': scores_users,
                    'blockk': blockk
                }

                return render(request, 'staff/queue/queue_create.html', {'data': data})

        # se nenhum critério foi selecionado pelo adm e não tiver feito nenhuma lista manual vai cair aqui
        users_ordered = User.objects.filter(is_professor=True, blocks=blockk).order_by(
            F('history__birth').asc(nulls_last=True))

        scores_users = []
        for user in users_ordered:
            user_score = calculate_total_score(user, False)
            scores_users.append(user_score)

        data = {
            'results': users_ordered,
            'field': get_string_field("birth"),
            'error_field': True,
            'total_score': scores_users,
            'blockk': blockk
        }

        return render(request, 'staff/queue/queue_create.html', {'data': data})
