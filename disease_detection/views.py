from django.shortcuts import render
from django.conf import settings
import os
import cv2
import numpy as np
from .models import KidneyDiseaseModel
from keras.models import load_model
from .forms import KidneyDiseaseForm

# Load the kidney disease model
kidney_model = load_model(os.path.join(settings.BASE_DIR, 'disease_detection/models/final_model.h5'))

def process(image_obj):
    # Read image data from the file object
    img_data = image_obj.read()
    # Convert the image data to a numpy array
    nparr = np.frombuffer(img_data, np.uint8)
    # Decode the numpy array into an image
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)  # Use IMREAD_GRAYSCALE to convert to grayscale
    # Resize the image to 225x225
    img = cv2.resize(img, (225, 225))
    # Normalize the image data to [0, 1]
    img = img / 255.0
    # Expand dimensions to match the input shape for the model (1, 225, 225, 1)
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)
    return img

def kidney_disease(pred_list):
    x = np.argmax(pred_list)
    if x == 0:
        output = "Disease: Cyst"
    elif x == 1:
        output = "Normal"
    elif x == 2:
        output = "Disease: Stone"
    elif x == 3:
        output = "Disease Tumor"
    return output

def kidney_disease_model_detection(img):
    pred = kidney_model.predict(img)
    output = kidney_disease(pred)
    print(output)
    return output

def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def info(request):
    kidney_disease_data = KidneyDiseaseModel.objects.all()
    return render(request, 'info.html', {'kidney_disease_data': kidney_disease_data})

def detection(request):
    return render(request, 'detection.html')

def kidney_disease_detect(request):
    if request.method == 'POST':
        form = KidneyDiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['p_image']
            image = process(image)
            output = kidney_disease_model_detection(image)
            instance = form.save(commit=False)
            instance.p_disease = output
            instance.save()
            return render(request, 'kidney_disease_detect.html', {'form': form, 'result': output})
    else:
        form = KidneyDiseaseForm()
    return render(request, 'kidney_disease_detect.html', {'form': form})
