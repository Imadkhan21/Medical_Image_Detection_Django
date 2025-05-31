# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     # path('', views.kidney_disease_detect, name='home'),


#     path('about-us/', views.about_us, name='about_us'),
#     path('info/', views.info, name='info'),
#     path('detection/', views.detection, name='detection'),
#     path('kidney-disease/', views.kidney_disease_detect, name='kidney_disease_detect'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('info/', views.info, name='info'),
    path('detection/', views.detection, name='detection'),
    path('kidney-disease/', views.kidney_disease_detect, name='kidney_disease_detect'),
]

