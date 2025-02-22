from django.urls import path
from thermo import views

urlpatterns = [
    path('', views.ThermoHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.add_data_about_home, name='add_data_about_home'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post, name='post'),



    # Проект
    path('result/', views.result_calculation, name='result'),
    path('heat_power/', views.HeatPower.as_view(), name='heat_power'),
    path('heat_power/edit/<int:pk>/', views.UpdateHome.as_view(), name='edit_home'),
    path('heat_power/delete/<int:pk>/', views.DeleteHome.as_view(), name='delete_home'),
    path('losses_insulation/', views.losses_insulation, name='losses_insulation'),

]



