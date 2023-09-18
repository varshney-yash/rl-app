from django.urls import path
from django.views.generic import RedirectView
from .views import register,profile,upload_image,ProfileDetailView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='blog-home', permanent=False)),
    path('register/', register, name='register'),
    path('profile/',profile,name='profile'),
    path('profile/<int:pk>/',ProfileDetailView.as_view(),name='anon-profile'),
    path('test-upload',upload_image)
]