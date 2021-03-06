from . import label_image as li

from django.shortcuts import render
from django import template

# Create your views here.
from django.template import loader

from django.conf import settings
from django.forms.forms import Form
import base64

# model = settings.MODEL

from .forms import ImageForm
from django.core.files.storage import FileSystemStorage

from PIL import Image
from io import BytesIO
from django.http import HttpResponse
import os

def index(request):
    print('index')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            upFile = request.FILES['imagefile']

            fs = FileSystemStorage()
            filename = fs.save(upFile.name, upFile)
            result = handle_uploaded_image(upFile.name)

            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)

            context = {
                'text': result,
                'form': form,
                'img': uploaded_file_url
            }
            print('complete')
            # render(request, 'main/index.html', context)
            # if fs.exists(filename):
            #     fs.delete(filename)
            return render(request, 'main/index.html', context)
    else:
        form = ImageForm()

    return render(request, 'main/index.html', {'form': form})


from fruitclass.util_00 import *
from keras.models import load_model
import numpy as np


def _process_image(im):
    img_width, img_height = get_resize_dimension()
    im_resize = im.resize((img_width, img_height), Image.ANTIALIAS)
    im = np.array(im_resize)
    im = im.reshape(-1, img_width, img_height, 3)
    im = im.astype('float32')
    im /= 255
    return im


def predict_fruit(image):
    # im = _process_image(image)
    # model = 'output_graph.pb'
    result = li.label_image(image)
    # print(result)
    # labels = get_tick_labels()
    # print('results:', result)
    # print('labels:', labels)
    # d = dict(zip(labels, result[0]))
    # print(d)
    # s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # classes = np.argmax(result)
    # print(s)
    # labels = get_tick_labels()
    # #return str(labels[classes])
    # return s
    return result


def handle_uploaded_image(i):
    # resize image
    print('handle_uploaded_image')
    # imagefile = BytesIO(i.read())
    # image = Image.open(imagefile)
    return predict_fruit(i)
