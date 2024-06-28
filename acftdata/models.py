from django.db import models


class Acfts(models.Model):
    type_acft = models.CharField('Тип ВС', max_length=10, blank=False)
    acft_id = models.CharField('Бортовой номер', max_length=10, blank=False)
    emty_w = models.FloatField('Масса пустого ВС', blank=False)
    emty_cg = models.FloatField('Центровка пустого ВС', blank=False)
    mtow_ivpp = models.IntegerField('MTOW ИВПП', blank=False)
    mtow_gvpp = models.IntegerField('MTOW ГВПП', blank=False)
    objects = models.Manager()

    def __str__(self):
        return self.acft_id

    class Meta:
        verbose_name = 'Aircraft'
        verbose_name_plural = 'Aircraft'


class An24rv_F15_Atm(models.Model):
    pr_alt = models.IntegerField()
    t00 = models.IntegerField()
    t05 = models.IntegerField()
    t10 = models.IntegerField()
    t15 = models.IntegerField()
    t20 = models.IntegerField()
    t25 = models.IntegerField()
    t30 = models.IntegerField()
    t35 = models.IntegerField()
    t40 = models.IntegerField()
    t45 = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.pr_alt)

    class Meta:
        verbose_name = 'AN24RV F15 ATM'
        verbose_name_plural = 'AN24RV F15 ATM'


class An24rv_F05_Atm(models.Model):
    pr_alt = models.IntegerField()
    t00 = models.IntegerField()
    t05 = models.IntegerField()
    t10 = models.IntegerField()
    t15 = models.IntegerField()
    t20 = models.IntegerField()
    t25 = models.IntegerField()
    t30 = models.IntegerField()
    t35 = models.IntegerField()
    t40 = models.IntegerField()
    t45 = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.pr_alt)

    class Meta:
        verbose_name = 'AN24RV F05 ATM'
        verbose_name_plural = 'AN24RV F05 ATM'


class An24rv_F15_asda(models.Model):
    asda = models.IntegerField()
    slope_2 = models.IntegerField()
    slope_0 = models.IntegerField()
    slope_m2 = models.IntegerField()
    wind_h20 = models.IntegerField()
    wind_h15 = models.IntegerField()
    wind_h10 = models.IntegerField()
    wind_h05 = models.IntegerField()
    wind_00 = models.IntegerField()
    wind_t05 = models.IntegerField()
    wind_t10 = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.asda)

    class Meta:
        verbose_name = 'AN24RV F15 ASDA'
        verbose_name_plural = 'AN24RV F15 ASDA'


class An24rv_F15_tora(models.Model):
    tora = models.IntegerField()
    slope_p2 = models.IntegerField()
    slope_p1 = models.IntegerField()
    slope_0 = models.IntegerField()
    slope_m1 = models.IntegerField()
    slope_m2 = models.IntegerField()
    wind_h20 = models.IntegerField()
    wind_h15 = models.IntegerField()
    wind_h10 = models.IntegerField()
    wind_h05 = models.IntegerField()
    wind_00 = models.IntegerField()
    wind_t05 = models.IntegerField()
    wind_t10 = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.tora)

    class Meta:
        verbose_name = 'AN24RV F15 TORA'
        verbose_name_plural = 'AN24RV F15 TORA'
