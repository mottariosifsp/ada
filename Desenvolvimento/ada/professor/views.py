import json
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core import serializers


from django.utils.decorators import method_decorator
from timetable.models import Timeslot, Timetable_user


def is_not_staff(user):
    return not user.is_staff

@login_required
def home(request):

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