from django.contrib import admin
from .models import Home

# Register your models here.

# admin.site.register(Home)



@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('street_name', 'numbers', 'construction_volume', 'indoor_air_temperature', 'construction_year',
                    'heating_characteristic')
    ordering = ['numbers']
    search_fields = ['street_name', 'numbers']