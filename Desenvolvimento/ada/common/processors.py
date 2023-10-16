# gource
def sort_by_time(model):
    count = 1
    for object in model.objects.all().order_by('hour_start'):
        object.position = count
        count += 1 
        object.save()
    print(model.objects.order_by('hour_start')[0].position)
