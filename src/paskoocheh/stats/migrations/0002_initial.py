# Generated by Django 3.2.23 on 2024-03-27 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tools', '0001_initial'),
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionreview',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.tool', verbose_name='Tool'),
        ),
        migrations.AddField(
            model_name='versionrating',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.tool', verbose_name='Tool'),
        ),
        migrations.AddField(
            model_name='versiondownload',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.tool', verbose_name='Tool'),
        ),
        migrations.AddField(
            model_name='versioncategoryrating',
            name='rating_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings', to='stats.ratingcategory'),
        ),
        migrations.AddField(
            model_name='versioncategoryrating',
            name='version_review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_ratings', to='stats.versionreview'),
        ),
    ]