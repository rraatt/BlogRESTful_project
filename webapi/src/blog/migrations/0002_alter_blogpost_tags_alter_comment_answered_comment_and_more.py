# Generated by Django 4.1.7 on 2023-04-06 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='Tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='answered_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost'),
        ),
    ]
