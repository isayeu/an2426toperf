from django.contrib import admin
from main.models import Airports


class AirportsAdmin(admin.ModelAdmin):
    search_fields = ['ICAO', 'IATA', 'name', 'city']


admin.site.register(Airports, AirportsAdmin)