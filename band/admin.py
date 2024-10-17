from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

@admin.register(models.FreshowsProfile)
class FreshowsProfileAdmin(admin.ModelAdmin):
    list_display = ['freshows_logo', 'thumbnail', 'slogan','description']
    readonly_fields= ['thumbnail']
    def thumbnail(self, instance):
        if instance.freshows_logo.name != '':
            return format_html(f'<img src="{instance.freshows_logo.url}" class="thumbnail"/>') 
        return ''
 

    class Media:
        css = {
            'all':['band/styles.css']
        }

    
@admin.register(models.MusicDirector)
class MusicDirectorAdmin(admin.ModelAdmin):
    autocomplete_fields = ['assigned_to']
    search_fields = ['notifications', 'assigned_to__artistic_name']
    list_display = ['notifications', 'sound_check_date', 'perfomance_date',\
                     'band_perfomance_details', 'reference_links', 'reference_images', 'thumbnail',\
                          'reference_folders', 'assigned_to']
    
    list_per_page = 10
    readonly_fields= ['thumbnail']
    def thumbnail(self, instance):
        if instance.reference_images.name != '':
            return format_html(f'<img src="{instance.reference_images.url}" class="thumbnail"/>') 
        return '' 
 

    class Media:
        css = {
            'all':['band/styles.css']
        }

    def reference_links(self, instance):
        if instance.reference_links != '':
            return format_html(f'<a href="{instance.reference_links}">{instance.reference_links}</a>')
        return ''
    

    
 

@admin.register(models.Calender)
class CalenderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['music_director']
    list_display = ['current_date', 'music_director', 'music_director_sound_check_date']
    

    def music_director_sound_check_date(self, objects):
        return objects.music_director.sound_check_date


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['first_name','last_name', 'artistic_name','email',\
                    'detailed_Band_Role']
    
    prepopulated_fields = {
        'slug': ['artistic_name']
    }
    
    search_fields = ['user__first_name', 'user__last_name', 'artistic_name']

    list_select_related = ['user', 'contract']
    
    ordering = ['user__first_name', 'user__last_name']

    list_per_page = 10

    


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    autocomplete_fields = ['member']
    list_display = ['title', 'description', 'document', 'member']
    prepopulated_fields = {
        'slug':['title']
    }
    list_select_related= ['member']
    ordering = ['member']
    search_fields = ['title', 'member__artistic_name']

    list_per_page = 10

    @admin.display(ordering='member')
    def member(self, contract):
        url = (
            reverse('admin:band_member_changelist')
            +'?'
            +urlencode({
                'contract__id': str(contract.id)
            }))
        return format_html('<a href="{}">{}</a>', url, contract.member)

    
 

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['first_name','last_name', 'email',\
                        'detailed_occupation']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name','user__last_name']


@admin.register(models.ClientPerformanceDetail)
class ClientPerformanceDetailAdmin(admin.ModelAdmin):
    autocomplete_fields = ['client_issuing']
    list_display = ['show_title', 'description', 'client_issuing','created_at', 'updated_at']
    prepopulated_fields ={
        'slug':['show_title']
    }
    search_fields = ['show_title__istartswith']


@admin.register(models.BandPackage)
class BandPackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'package_price', 'created_at', 'updated_at']
    search_fields = ['title__istartswith']


@admin.register(models.AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['issuing_client']
    list_display = ['title', 'description', 'issuing_client']
    search_fields = ['title__istartswith']
    exclude = ['user']
    prepopulated_fields = {
        'slug': ['title']
    }

    def issuing_client(self, additionalService): 
        url = (
            reverse('admin:band_client_changelist')
            +'?'
            + urlencode({
                'additionalService__id': str(additionalService.id)
            }))           
        return format_html('<a href="{}">{}</a>', url, additionalService.issuing_client)


class AvailableServicesInline(admin.TabularInline):
    autocomplete_fields = ['additional_service', 'band_package']
    min_num = 1
    max_num = 1
    model = models.AvailableService
    extra = 0


@admin.register(models.ServiceOrdering)
class ServiceOrderingAdmin(admin.ModelAdmin): 
    autocomplete_fields = ['client'] 
    inlines = [AvailableServicesInline] 
    list_display = ['id', 'placed_at', 'client', 'payment_status']
    list_editable = ['payment_status']
    search_fields = ['client__user__first_name', 'client__user__last_name']


@admin.register(models.FinalServiceOrderApproval)
class FinalServiceOrderApprovalAdmin(admin.ModelAdmin):
    list_display =['freshows_logo', 'thumbnail', 'performance_title', 'freshow_phone', 'freshow_email',\
                   'service_ordered_detail', 'performance_requirements', 'price_breakdown', 'total_price',\
                    'final_approval_status']
    list_editable = ['final_approval_status']
    search_fields = ['performance_title__istartswith']
    prepopulated_fields = {
        'slug': ['performance_title']
    }
    readonly_fields= ['thumbnail']
    def thumbnail(self, instance):
        if instance.freshows_logo.name != '':
            return format_html(f'<img src="{instance.freshows_logo.url}" class="thumbnail"/>') 
        return ''
 

    class Media:
        css = {
            'all':['band/styles.css']
        }

