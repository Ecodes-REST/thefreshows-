# Generated by Django 4.2.16 on 2024-10-17 04:35

import band.validators
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
            name='AdditionalService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Additional Services')),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BandPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('package_price', models.DecimalField(decimal_places=2, max_digits=40, validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('detailed_occupation', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
                'permissions': [('view_history', 'can view history')],
            },
        ),
        migrations.CreateModel(
            name='FreshowsProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freshows_logo', models.ImageField(blank=True, upload_to='band/freshows_logo', validators=[band.validators.validate_file_size])),
                ('slogan', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artistic_name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('phone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('detailed_Band_Role', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['artistic_name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceOrdering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_orderings', to='band.client')),
            ],
            options={
                'permissions': [('cancel_order', 'Can cancel order')],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('band_package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='band.bandpackage')),
            ],
        ),
        migrations.CreateModel(
            name='MusicDirector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notifications', models.TextField(blank=True)),
                ('sound_check_date', models.DateField()),
                ('perfomance_date', models.DateField()),
                ('band_perfomance_details', models.TextField()),
                ('reference_links', models.URLField(blank=True)),
                ('reference_images', models.ImageField(blank=True, upload_to='band/reference_images', validators=[band.validators.validate_file_size])),
                ('reference_folders', models.FileField(blank=True, upload_to='band/reference_folders')),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='band.member')),
            ],
        ),
        migrations.CreateModel(
            name='FinalServiceOrderApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freshows_logo', models.ImageField(upload_to='band/freshows_logo', validators=[band.validators.validate_file_size])),
                ('performance_title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('freshow_phone', models.CharField(max_length=255)),
                ('freshow_email', models.CharField(max_length=255)),
                ('performance_requirements', models.TextField()),
                ('price_breakdown', models.TextField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=50, validators=[django.core.validators.MinValueValidator(1)])),
                ('final_approval_status', models.CharField(choices=[('P', 'Pending...'), ('A', 'Approved'), ('F', 'Failed')], default='', max_length=255)),
                ('service_ordered_detail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='band.serviceordering')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('document', models.FileField(blank=True, null=True, upload_to='band/docs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('member', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='band.member')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ClientPerformanceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_issuing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='band.client')),
            ],
        ),
        migrations.CreateModel(
            name='Calender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField(default=django.utils.timezone.now)),
                ('music_director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='band.musicdirector')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_service_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('additional_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='availableservices', to='band.additionalservice')),
                ('band_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availableservices', to='band.bandpackage')),
                ('service_ordering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='band.serviceordering')),
            ],
        ),
        migrations.AddField(
            model_name='additionalservice',
            name='issuing_client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='band.client'),
        ),
        migrations.AddField(
            model_name='additionalservice',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
