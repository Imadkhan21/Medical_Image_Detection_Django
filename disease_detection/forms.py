from django import forms
from .models import KidneyDiseaseModel

class KidneyDiseaseForm(forms.ModelForm):
    class Meta:
        model = KidneyDiseaseModel
        exclude = ['p_disease']
        labels = {
            'p_id': "Patient ID",
            'p_name': "Patient Name",
            'p_email': "Patient Email",
            'p_image': "Patient Image",
        }
