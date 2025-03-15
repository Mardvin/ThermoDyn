from django.urls import path
from thermo import views

urlpatterns = [
    path('', views.ThermoHome.as_view(), name='heat_power_home'),
    path('heat_power/create/', views.CreateHome.as_view(), name='heat_power_create'),
    path('heat_power/edit/<int:pk>/', views.UpdateHome.as_view(), name='edit_home'),
    path('heat_power/delete/<int:pk>/', views.DeleteHome.as_view(), name='delete_home'),

    path('electricity_costs/', views.ElectricityCosts.as_view(), name='electricity_costs'),
    path('electricity_costs/create/', views.CreateElectricity.as_view(), name='create_electricity'),
    path('electricity_costs/edit/<int:pk>/', views.UpdateElectricity.as_view(), name='edit_electricity'),
    path('electricity_costs/delete/<int:pk>/', views.DeleteElectricity.as_view(), name='delete_electricity'),
]



