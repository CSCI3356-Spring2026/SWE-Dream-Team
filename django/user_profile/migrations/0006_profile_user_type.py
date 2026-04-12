# Generated manually for Profile.user_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_profile_housing_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('renter', 'Renter'), ('sublettor', 'Sublettor')], default='renter', max_length=10),
        ),
    ]

