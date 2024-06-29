from django.db import models

# Model for Kidney Disease
class KidneyDiseaseModel(models.Model):
    p_id = models.CharField(max_length=100)
    p_name = models.CharField(max_length=100)
    p_email = models.EmailField(max_length=100)
    p_image = models.ImageField(upload_to="posts", null=True)
    p_disease = models.CharField(max_length=100, default="Not determined")
