# Generated by Django 4.0 on 2021-12-18 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0005_alter_course_classtime_alter_course_major_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='classTime',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='major',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='place',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='professor',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(max_length=100, null=True),
        ),
    ]