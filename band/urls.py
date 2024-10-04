from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('freshows_profile', views.FreshowsProfileViewSet)
router.register('client', views.ClientViewSet)
router.register('member', views.MemberViewSet)
router.register('contract', views.ContractViewSet)
router.register('music_director', views.MusicDirectorViewSet)
router.register('band_package', views.BandPackageViewSet)
router.register('additional_services', views.AdditionalServicesViewSet)
router.register('client_performance', views.ClientPerformanceViewSet)
router.register('calendar', views.CalendarViewSet)
router.register('available_service', views.AvailableServiceViewSet)
router.register('service_ordering', views.ServiceOrderingViewSet)
router.register('final_service_order_approval', views.FinalServiceOrderApprovalViewSet)


band_package_router= routers.NestedDefaultRouter(router, 'band_package', lookup= 'band_package')
band_package_router.register('reviews', views.BandPackageReviewViewSet, basename= 'band_package_reviews')

urlpatterns = router.urls + band_package_router.urls 
