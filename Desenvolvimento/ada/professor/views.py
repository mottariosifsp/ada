from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

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
        print(blockks_images)
    data = {
        'blockks': blockks_images
    }

    return render(request, 'professor/home_professor.html', data)
