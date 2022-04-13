from genericpath import exists
from ipaddress import ip_address
import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from matplotlib.style import context
from .helper import getResult, percentageFIX
from os.path import exists
import cv2
from monitoring.models import Suhu
from PIL import Image
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
host = '192.168.43.197:80'

def index(request):
    # set img to hsv
    img = cv2.imread('monitoring/static/image/data.jpg')

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    weight = getResult(img_hsv)
    percentage = percentageFIX(weight)
    hasil = max(weight, key=weight.get)

    context = {
        'host': host,
        'hasil':hasil, 
        'bobot':weight,
        'persentase':percentage,}
    return render(request, 'monitoring/index.html', context)

def grafik(request):
    img = cv2.imread('monitoring/static/image/data.jpg')

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    weight = getResult(img_hsv)
    percentage = percentageFIX(weight)
    context = {'percentage':percentage,'host': host,}
    return render(request, 'monitoring/grafik.html', context)

def suhu(request):
    data = Suhu.objects.all().count()
    if data > 0:
        Suhu.objects.all().delete()
    val = request.GET.get('suhu')
    suhu = Suhu(suhu = val)
    suhu.save()
    return HttpResponse(val)

def suhuapi(request):
    suhu = Suhu.objects.all().values('suhu')
    res = list(suhu)
    return JsonResponse(res[0], safe=False)

@csrf_exempt
def upload(request):
    BASE_DIR_UPLOAD = 'monitoring/static/image/'
    if request.method == 'POST' and request.FILES['imageFile']:
        file = request.FILES['imageFile']
        fs = FileSystemStorage()
        # check file exists 
        if exists(BASE_DIR_UPLOAD + 'data.jpg'):
            os.remove(BASE_DIR_UPLOAD + 'data.jpg')
        # save img
        # fs.save(BASE_DIR_UPLOAD + 'data.jpg', file)

        # resize img
        image = Image.open(file)
        image.thumbnail((400, 300))
        image.save(BASE_DIR_UPLOAD + 'data.jpg')
        # read img
        img = cv2.imread(BASE_DIR_UPLOAD + 'data.jpg')
        # color detection
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        weight = getResult(img_hsv)
        percentage = percentageFIX(weight)
        hasil = max(weight, key=weight.get)
        return render(request, 'monitoring/index.html', {
            'host':host,
            'hasil':hasil, 
            'bobot':weight,
            'persentase':percentage,})
    return render(request, 'monitoring/upload.html')