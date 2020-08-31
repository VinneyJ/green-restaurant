# Generated by Django 3.0.7 on 2020-08-29 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0003_auto_20200828_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('dri', 'Drinks'), ('bev', 'Beverage')], default='food', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], default='P', max_length=2),
            preserve_default=False,
        ),
    ]
