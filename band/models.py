from django.core.validators import MinValueValidator,FileExtensionValidator
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils import timezone
from .validators import validate_file_size

# Create your models here.

class FreshowsProfile(models.Model):
    freshows_logo = models.ImageField(upload_to='band/freshows_logo', 
                                      validators= [validate_file_size], blank= True)
    slogan = models.CharField(max_length=255)
    description = models.TextField()


class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete = models.CASCADE
    )
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering= 'user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering= 'user__last_name')
    def last_name(self):
        return self.user.last_name
    
    artistic_name = models.CharField(max_length=255)
    slug = models.SlugField()
    phone = models.CharField(max_length= 255)
    email = models.EmailField(unique= True)
    detailed_Band_Role = models.TextField()

    def __str__(self):
        return self.artistic_name
    
    class Meta:
        ordering = ['artistic_name']
    
class MusicDirector(models.Model):
    notifications = models.TextField(blank= True)
    sound_check_date = models.DateField()
    perfomance_date = models.DateField()
    band_perfomance_details = models.TextField()
    reference_links = models.URLField(blank= True)
    reference_images = models.ImageField(upload_to='band/reference_images', 
                                         validators= [validate_file_size], blank= True)
    reference_folders = models.FileField(upload_to= 'band/reference_folders', blank= True)
    assigned_to = models.ForeignKey(Member, on_delete= models.CASCADE)
    update_at = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return self.notifications


class Calender(models.Model):
    current_date = models.DateField( default= timezone.now)
    music_director = models.ForeignKey(MusicDirector, on_delete= models.CASCADE)


class Contract(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    document = models.FileField(
        upload_to= 'band/docs',
        validators= [FileExtensionValidator(allowed_extensions=['pdf'])],
        null= True,
        blank= True
    )
    member= models.OneToOneField(Member, on_delete=models.SET_NULL, null= True)

    def __str__(self) -> str:
        return self.title
        
    class Meta:
        ordering = ['title']

class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete= models.CASCADE
    )
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering= 'user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering= 'user__last_name')
    def last_name(self):
        return self.user.last_name
    
    phone = models.CharField(max_length= 255)
    email = models.EmailField(unique= True, blank= True, null= True)
    detailed_occupation = models.TextField()
    
    class Meta:
        ordering= ['user__first_name', 'user__last_name']
        permissions= [
            ('view_history', 'can view history')
        ]

class ClientPerformanceDetail(models.Model):
    show_title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    client_issuing = models.OneToOneField(Client, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return self.show_title

class BandPackage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    package_price = models.DecimalField(
        max_digits=40, 
        decimal_places=2,
        validators= [MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.title} - price {str(self.package_price)}"

class AdditionalService(models.Model):
    title = models.CharField(max_length=50, verbose_name='Additional Services')
    slug = models.SlugField()
    description = models.TextField(blank= True, null= True)
    issuing_client = models.OneToOneField(Client, on_delete= models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return self.title
    


class ServiceOrdering(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='service_orderings')

    def __str__(self) -> str:
        return f"{self.client.first_name()} {self.client.last_name()}"
    
    
    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]



class AvailableService(models.Model):
    service_ordering = models.ForeignKey(ServiceOrdering, on_delete=models.CASCADE, related_name='services')
    band_package = models.ForeignKey(
        BandPackage, on_delete=models.CASCADE, related_name='availableservices')
    additional_service = models.ForeignKey(
        AdditionalService, on_delete=models.CASCADE, null= True, blank= True, related_name='availableservices'
    )
    additional_service_price = models.DecimalField(max_digits=20, decimal_places=2, null= True, blank= True, default= 0)

class FinalServiceOrderApproval(models.Model):
    freshows_logo = models.ImageField(upload_to='band/freshows_logo', validators= [validate_file_size])
    performance_title = models.CharField(max_length=255)
    slug = models.SlugField()
    freshow_phone = models.CharField(max_length=255)
    freshow_email = models.CharField(max_length=255)
    service_ordered_detail = models.OneToOneField(ServiceOrdering, on_delete= models.CASCADE)
    performance_requirements = models.TextField()
    price_breakdown = models.TextField()
    total_price = models.DecimalField(
        max_digits=50, 
        decimal_places=2,
        validators= [MinValueValidator(1)])
    
    APPROVAL_STATUS_PENDING = 'P'
    APPROVAL_STATUS_APPROVED = 'A'
    APPROVAL_STATUS_NOT_APPROVED= 'F'

    APPROVAL_TYPE_CHOICES = [
        (APPROVAL_STATUS_PENDING, 'Pending...'),
        (APPROVAL_STATUS_APPROVED, 'Approved'),
        (APPROVAL_STATUS_NOT_APPROVED,'Failed'),
    ]
    final_approval_status = models.CharField(max_length=255, default='', choices=APPROVAL_TYPE_CHOICES)


class Review(models.Model):
    band_package= models.ForeignKey(BandPackage, on_delete= models.CASCADE, null=True)
    name= models.CharField(max_length= 255)
    description= models.TextField()
    date= models.DateField(auto_now_add= True)