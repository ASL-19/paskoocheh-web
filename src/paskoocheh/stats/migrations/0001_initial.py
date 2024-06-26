# Generated by Django 3.2.23 on 2024-03-27 19:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified time')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='User Name')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Subject')),
                ('text', models.CharField(blank=True, max_length=512, null=True, verbose_name='Message')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel', models.CharField(choices=[('BOT', 'Telegram Bot'), ('EMAIL', 'Email Auto Responder'), ('ANDROID', 'Android App'), ('WEB', 'Website')], max_length=32)),
                ('channel_version', models.CharField(max_length=128, verbose_name='Channel Version')),
                ('platform_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Platform Name')),
                ('platform_version', models.CharField(blank=True, max_length=128, null=True, verbose_name='Platform Version')),
                ('status', models.CharField(choices=[('0', 'New'), ('1', 'Read'), ('2', 'Purged')], default='0', max_length=2, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='RatingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_fa', models.CharField(max_length=100)),
                ('name_ar', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Rating Categories',
            },
        ),
        migrations.CreateModel(
            name='StatsLastRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download_last', models.IntegerField(default=0)),
                ('failed_last', models.IntegerField(default=0)),
                ('install_last', models.IntegerField(default=0)),
                ('update_last', models.IntegerField(default=0)),
                ('feedback_last', models.IntegerField(default=0)),
                ('rating_last', models.IntegerField(default=0)),
                ('review_last', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VersionCategoryRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rating', models.DecimalField(decimal_places=1, default=2.5, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Star Rating')),
            ],
        ),
        migrations.CreateModel(
            name='VersionDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified time')),
                ('tool_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tool name')),
                ('platform_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Platform Name')),
                ('download_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VersionRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified time')),
                ('tool_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tool name')),
                ('platform_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Platform Name')),
                ('star_rating', models.DecimalField(decimal_places=1, default=2.5, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Star Rating')),
                ('rating_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VersionReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified time')),
                ('tool_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tool name')),
                ('platform_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Platform Name')),
                ('subject', models.CharField(blank=True, max_length=256, null=True, verbose_name='Subject')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='User Name')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('username', models.CharField(blank=True, max_length=256, null=True, verbose_name='User Name')),
                ('rating', models.DecimalField(decimal_places=1, default=2.5, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Star Rating')),
                ('checked', models.BooleanField(default=True, verbose_name='Checked')),
                ('tool_version', models.CharField(blank=True, max_length=256, null=True, verbose_name='Tool Version')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('language', models.CharField(choices=[('en', 'English'), ('fa', 'Persian'), ('ar', 'Arabic')], default='fa', max_length=2, verbose_name='Language')),
                ('pask_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VersionReviewVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.CharField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')], max_length=8)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='stats.versionreview')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
