# Generated migration for adding user roles

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(
                choices=[('customer', 'Customer'), ('company_member', 'Company Member')],
                default='customer',
                help_text='User role',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='company_name',
            field=models.CharField(
                blank=True,
                help_text='Company name for company members',
                max_length=200,
                null=True,
            ),
        ),
    ]
