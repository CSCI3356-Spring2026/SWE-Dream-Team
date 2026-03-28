# Generated manually for roommate preference fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_profile_housing_match_profile_roommate_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ideal_housing_vibe',
            field=models.CharField(
                choices=[
                    ('quiet_studious', 'Quiet & Studious'),
                    ('chill_low_key', 'Chill & Low-Key'),
                    ('social_balanced', 'Social but Balanced'),
                    ('very_social', 'Very Social / Going Out Often'),
                    ('independent', 'Independent / Keep to Myself'),
                ],
                default='quiet_studious',
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='roommate_dealbreakers',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='profile',
            name='cleanliness',
            field=models.CharField(
                choices=[
                    ('very_messy', 'Very messy'),
                    ('somewhat_messy', 'Somewhat messy'),
                    ('neutral', 'Neutral'),
                    ('somewhat_clean', 'Somewhat clean'),
                    ('very_clean', 'Very clean'),
                ],
                default='neutral',
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='weekend_bedtime',
            field=models.CharField(
                choices=[
                    ('20:00', '8:00 PM'),
                    ('21:00', '9:00 PM'),
                    ('22:00', '10:00 PM'),
                    ('23:00', '11:00 PM'),
                    ('00:00', '12:00 AM (midnight)'),
                    ('01:00', '1:00 AM'),
                    ('02:00', '2:00 AM'),
                ],
                default='23:00',
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='weeknight_bedtime',
            field=models.CharField(
                choices=[
                    ('20:00', '8:00 PM'),
                    ('21:00', '9:00 PM'),
                    ('22:00', '10:00 PM'),
                    ('23:00', '11:00 PM'),
                    ('00:00', '12:00 AM (midnight)'),
                    ('01:00', '1:00 AM'),
                    ('02:00', '2:00 AM'),
                ],
                default='23:00',
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='social_level',
            field=models.CharField(
                choices=[
                    ('very_social', 'Very social'),
                    ('moderately_social', 'Moderately social'),
                    ('balanced', 'Balanced'),
                    ('mostly_independent', 'Mostly independent'),
                    ('extremely_independent', 'Extremely independent'),
                ],
                default='balanced',
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='live_opposite_sex',
            field=models.CharField(
                choices=[('yes', 'Yes'), ('no', 'No')],
                default='no',
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='share_double',
            field=models.CharField(
                choices=[('yes', 'Yes'), ('no', 'No')],
                default='no',
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='okay_smoking',
            field=models.CharField(
                choices=[('yes', 'Yes'), ('no', 'No')],
                default='no',
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='okay_alcohol',
            field=models.CharField(
                choices=[('yes', 'Yes'), ('no', 'No')],
                default='no',
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='okay_overnight',
            field=models.CharField(
                choices=[('yes', 'Yes'), ('no', 'No')],
                default='no',
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='okay_pets',
            field=models.CharField(
                choices=[('yes', 'Yes'), ('no', 'No')],
                default='no',
                max_length=3,
            ),
        ),
    ]
