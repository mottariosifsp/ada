import json
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth import get_user_model

from django.utils.decorators import method_decorator
from timetable.models import Timeslot, Timetable_user, Timetable
from attribution_preference.models import Attribution_preference
from staff.models import Deadline, Alert
from area.models import Area, Blockk
from datetime import datetime, timedelta
from classs.models import Classs
from course.models import Course

from user.models import User
from django.core.mail import send_mail, EmailMessage

def is_not_staff(user):
    return not user.is_staff

@login_required
def home(request):
    blockks = request.user.blocks.all()
    blockks_images = []

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
    user = request.user

    user_blocks = user.blocks.all()

    # escreva o codigo onde voce quer que o professor receba os alertas de seus blocos
    user_alerts = []
    for block in user_blocks:
        alerts = Alert.objects.filter(name_alert='ALERT', blockk=block)
        if alerts:
            for alert in alerts:
                alert = {
                    'id': alert.id,
                    'title': alert.title,
                    'description': alert.description,
                    'blockk': alert.blockk
                }
                user_alerts.append(alert)

    links = Alert.objects.filter(name_alert='LINK')
    user_links = []
    for link in links:
        link = {
            'id': link.id,
            'title': link.title,
            'created_by': link.created_by,
            'description': link.description
        }
        user_links.append(link)


    for blockk in blockks:
        blockk_images = {
            "block": blockk,
            "image": None
        }
        if blockk.registration_block_id == "CNA.151515":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117328326533595207/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "HUM.141414":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117321570101248030/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "LNG.161616":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117321528380489789/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "MAT.131313":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1116866399952961586/dan-cristian-padure-h3kuhYUCE9A-unsplash.jpg?width=710&height=473"
        elif blockk.registration_block_id == "TEC.121212":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1116866399671951441/roonz-nl-2xEQDxB0ss4-unsplash.jpg?width=842&height=473"
        elif blockk.registration_block_id == "776292":
            blockk_images[
                "image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117348338254233680/image.png"
        blockks_images.append(blockk_images)


    count = {
        'alerts': len(user_alerts),
        'links': len(user_links)
    }

    data = {
        'count': count,
        'alerts': user_alerts,
        'links': user_links,
        'blockks': blockks_images,
        'period': period
    }

    print(data)

    return render(request, 'professor/home_professor.html', data)

@login_required
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

@login_required
def terms_and_conditions (request):
    return render(request, 'terms_and_conditions.html')

def profile(request):
    professor = request.user
    timeslots_all = Timeslot.objects.all()
    timetables_user = Timetable_user.objects.filter(user=professor)

    timetables_professor = []

    for timetable_user in timetables_user:
        day_combos = timetable_user.timetable.day_combo.all()
        for day_combo in day_combos:
            day = day_to_number(day_combo.day)
            timeslots = day_combo.timeslots.all()

            for timeslot in timeslots:
                position = timeslot.position

                timetable_professor = {
                    "cord": f'{position}-{day}',
                    "course": timetable_user.timetable.course.name_course,
                    "acronym": timetable_user.timetable.course.acronym,
                }
                timetables_professor.append(timetable_professor)
    timetables_professor_json = json.dumps(timetables_professor, ensure_ascii=False).encode('utf8').decode()
    # print(timetables_professor_json)

    user = request.user
    user_blocks = user.blocks.all()

    fpa_history = []
    for atrribution_user in Attribution_preference.objects.filter(user=user):
        year = atrribution_user.year
        fpa_history.append(year)

    data = {
        'fpas': fpa_history,
        'user_blocks': user_blocks,
        'professor': professor,
        'timeslots': timeslots_all,
        'timetables_professor': timetables_professor_json
    }
    print(data)

    return render(request, 'professor/profile.html', data)


@login_required
def show_assignment(request):
    classs = Classs.objects.get(registration_class_id=request.GET.get('registration_class_id'))

    timetables = Timetable.objects.filter(classs=classs).all()
    timeslots_all = Timeslot.objects.all()
    timetables_user = Timetable_user.objects.filter(timetable__in=timetables).all()  # vai buscar apenas da atribuição final definitiva

    timetables_professor = []

    for timetable_user in timetables_user:
        day_combos = timetable_user.timetable.day_combo.all()
        for day_combo in day_combos:
            day = day_to_number(day_combo.day)
            timeslots = day_combo.timeslots.all()

            if timetable_user.user is not None:
                professor = timetable_user.user.first_name

            else:
                professor = "-"

            for timeslot in timeslots:
                position = timeslot.position
                print("timetable user", timetable_user.user)
                timetable_professor = {
                    "cord": f'{position}-{day}',
                    "course": timetable_user.timetable.course.name_course,
                    "acronym": timetable_user.timetable.course.acronym,
                    "professor": professor,
                    "class_area": timetable_user.timetable.classs.registration_class_id
                }
                timetables_professor.append(timetable_professor)
                # print("Timetable professorr",timetables_professor ) #Ok, só pega o professor D
                timetables_professor_json = json.dumps(timetables_professor, ensure_ascii=False).encode(
                    'utf8').decode()  # junção de todos

                data = {
                    'timeslots': timeslots_all,
                    'timetables_professor': timetables_professor_json,
                    'classs': classs
                }

    return render(request, 'professor/show_assignment.html', data)
@login_required
def assignments(request):
    blockks = request.user.blocks.all()
    blockks_images = []

    for blockk in blockks:
        blockk_images = {
            "block": blockk,
            "image": None
        }

        if blockk.registration_block_id == "CNA.151515":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117328326533595207/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "HUM.141414":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117321570101248030/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "LNG.161616":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117321528380489789/OIG.png?width=473&height=473"
        elif blockk.registration_block_id == "MAT.131313":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1116866399952961586/dan-cristian-padure-h3kuhYUCE9A-unsplash.jpg?width=710&height=473"
        elif blockk.registration_block_id == "TEC.121212":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1116866399671951441/roonz-nl-2xEQDxB0ss4-unsplash.jpg?width=842&height=473"
        elif blockk.registration_block_id == "776292":
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117348338254233680/image.png"
        blockks_images.append(blockk_images)

    return render(request, 'professor/assignments.html', {'blockks': blockks_images})


@login_required
def assignments_classs_list(request, name_block):
    blockk = Blockk.objects.get(name_block=name_block)

    areas_associadas = Area.objects.filter(blocks=blockk)

    timetable_data = []
    all_classes = []
    timetables_professor = []

    for area in areas_associadas:
        classes_da_area = Classs.objects.filter(area=area)

        for classe in classes_da_area:
            all_classes.append({
                "id": classe.id,
                "registration_class_id": classe.registration_class_id,
                "period": classe.period,
                "semester": classe.semester,
                "registration_area_id": classe.area.registration_area_id,
            })

    all_classes = json.dumps(all_classes)

    data = {
        'areas': areas_associadas,
        'json_data': all_classes,
    }

    return render(request, 'professor/assignments_classs_list.html', data)

@login_required
def professor_blocks_list(request):
    blocks = request.user.blocks.all()
    return render(request, 'professor/blockk/blocks_list.html', {'blocks': blocks})

@login_required
def professor_block_detail(request, registration_block_id):
    user_blocks = request.user.blocks.all()
    blockk = Blockk.objects.get(registration_block_id=registration_block_id)
    area = blockk.areas.values_list('name_area', flat=True)
    courses = Course.objects.filter(blockk=blockk)
    data = {
        'user_blocks': user_blocks,
        'blockk': blockk,
        'areas': list(area),
        'courses': courses
    }

    return render(request, 'professor/blockk/block_detail.html', data)

def day_to_number(day):
    number = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
    }
    return number[day]