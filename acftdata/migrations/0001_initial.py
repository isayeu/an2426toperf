# Generated by Django 4.2.7 on 2023-12-14 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acfts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_acft', models.CharField(max_length=10)),
                ('acft_id', models.CharField(max_length=10)),
                ('emty_w', models.IntegerField()),
                ('emty_cg', models.IntegerField()),
            ],
        ),
    ]
