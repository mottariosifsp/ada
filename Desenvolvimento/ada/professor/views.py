import json
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core import serializers


from django.utils.decorators import method_decorator
from timetable.models import Timeslot, Timetable_user
from staff.models import Deadline, Alert
from datetime import datetime, timedelta

from user.models import User
from django.core.mail import send_mail, EmailMessage


def is_not_staff(user):
    return not user.is_staff

def register(request):
    professors_inactive = User.objects.filter(is_professor=True, is_active=False).all()

    for professor in professors_inactive:
        send_email(professor)


def send_email(professor):
    subject = 'Ação requerida: Cadastre-se'

    nome = professor.first_name
    email = professor.email

    current_path = os.getcwd()
    with open(current_path + '\\templates\static\email\professor_register_message.html', 'r', encoding='utf-8') as file:
        message = file.read()
        message = message.format(nome=nome)

    email = EmailMessage(
        subject,
        message,
        'ada.ifsp@gmail.com',
        [email],
    )

    email.content_subtype = "html"

    email.send()



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
            blockk_images["image"] = "https://media.discordapp.net/attachments/1081682716531118151/1117348338254233680/image.png"
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
    print(timetables_professor_json)

    data = {
        'professor': professor,
        'timeslots': timeslots_all,
        'timetables_professor': timetables_professor_json   
    }

    return render(request, 'professor/profile.html', data)

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