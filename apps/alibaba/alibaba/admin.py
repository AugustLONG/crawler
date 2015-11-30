# encoding:utf-8
from django.contrib import admin

from alibaba.models import City, Country, Location, Zone, Province


class CountryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'chart', 'latitude', 'longitude')
    search_fields = ('name', 'chart')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'chart', 'latitude', 'longitude')
    search_fields = ('name', 'chart')


class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'chart', 'latitude', 'longitude')
    search_fields = ('name', 'chart')


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'chart', 'latitude', 'longitude')
    search_fields = ('name', 'chart')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'chart', 'latitude', 'longitude')
    search_fields = ('name', 'chart')


admin.site.register(Country, CountryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Province, ProvinceAdmin)
