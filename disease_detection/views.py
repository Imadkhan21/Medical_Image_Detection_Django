from django.shortcuts import render
from django.conf import settings
import os
import cv2
import numpy as np
from .models import KidneyDiseaseModel
from keras.models import load_model
from .forms import KidneyDiseaseForm
from django.http import JsonResponse



# Load the kidney disease model
kidney_model = load_model(os.path.join(settings.BASE_DIR, 'disease_detection/models/final_model.h5'))

# Preprocess the image
def process(image_obj):
    img_data = image_obj.read()
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (225, 225))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)
    return img

# Convert prediction to label and extract confidence
def kidney_disease_with_confidence(pred_list):
    x = np.argmax(pred_list)
    confidence = float(np.max(pred_list)) * 100  # Convert to percentage

    labels = ["Disease: Cyst", "Normal", "Disease: Stone", "Disease: Tumor"]
    label = labels[x]

    return label, round(confidence, 2)

# Predict disease with confidence
def kidney_disease_model_detection(img):
    pred = kidney_model.predict(img)
    label, confidence = kidney_disease_with_confidence(pred)
    print(f"{label} (Confidence: {confidence}%)")
    return label, confidence




# Views
def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def info(request):
    kidney_disease_data = KidneyDiseaseModel.objects.all()
    return render(request, 'info.html', {'kidney_disease_data': kidney_disease_data})

def detection(request):
    return render(request, 'detection.html')

# # Main detection view (AJAX compatible)
def kidney_disease_detect(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = KidneyDiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['p_image']
            processed_image = process(image)
            output, confidence = kidney_disease_model_detection(processed_image)

            instance = form.save(commit=False)
            instance.p_disease = output
            instance.save()

            return JsonResponse({
                'result': output,
                'confidence': confidence,
                'uploaded_image_url': instance.p_image.url
                
            })
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = KidneyDiseaseForm()
        return render(request, 'kidney_disease_detect.html', {'form': form})


