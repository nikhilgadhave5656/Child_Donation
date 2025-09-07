# myapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('about-us/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),
    path('child/<int:child_id>/pay/', views.create_payment, name='create_payment'),
    path('payment-tracker/', views.payment_tracker, name='payment_tracker'),
    
]



