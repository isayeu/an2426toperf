from django.db import models


class Airports(models.Model):
    aiirport_id = models.CharField('aiirport_id', max_length=10)
    faa_id = models.CharField('faa_id', max_length=10)
    ICAO = models.CharField('ICAO', max_length=4, blank=True, default='')
    IATA = models.CharField('IATA', max_length=3, blank=True, default='')
    name = models.CharField('name', max_length=100)
    city = models.CharField('city', max_length=10)
    country = models.CharField('country', max_length=4)
    latitude = models.FloatField('Latitude', blank=False)
    longitude = models.FloatField('longitude', blank=False)
    alevation = models.IntegerField('alevation', blank=False)
    timezone_index = models.IntegerField('timezone_index')
    type_index = models.IntegerField('type_index')
    is_towered = models.IntegerField('is_towered')
    objects = models.Manager()

    def __str__(self):
        return self.ICAO if self.ICAO else ''

    class Meta:
        verbose_name = 'Airport'
        verbose_name_plural = 'Airports'
