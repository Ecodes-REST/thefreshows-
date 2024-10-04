from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from . models import BandPackage, AdditionalService, FinalServiceOrderApproval, FreshowsProfile, MusicDirector, Client, Member, Calender, Contract, ClientPerformanceDetail, ServiceOrdering, AvailableService, Review
from . serializers import BandPackageSerializer, FinalServiceOrderApprovalSerializer, FreshowsProfileSerializer, MusicDirectorSerializer, ClientSerializer, ClientPerformanceDetailSerializer, MemberSerializer, CalenderSerializer, ContractSerializer, AdditionalServiceSerializer, ServiceOrderingSerializer, AvailableServiceSerializer, BandPackageReviewSerializer
from . permissions import IsAdminOrReadOnly, IsClient, IsMember, ViewClientHistoryPermission
# Create your views here.

class FreshowsProfileViewSet(ModelViewSet):
    queryset = FreshowsProfile.objects.all()
    serializer_class = FreshowsProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields= ['detailed_occupation', 'email', 'phone']
    ordering_fields= ['user', 'email']
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewClientHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail= False, methods= ['GET', 'PUT'], permission_classes= [IsClient])
    def me (self, request):
        client = Client.objects.filter(user_id=request.user.id).exclude(detailed_occupation='').first()
        if client is None:
            return Response({'detail': 'You are not registered as a client'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer =  ClientSerializer(client)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ClientSerializer(client, data= request.data)
            serializer.is_valid(raise_exception= True)
            serializer.save() 
            return Response(serializer.data)
          
class MemberViewSet(ModelViewSet):
    queryset= Member.objects.all()
    serializer_class= MemberSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields= ['artistic_name']
    ordering_fields= ['artistic_name']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request == 'GET':
         return [AllowAny()]
        else:
            return[IsAdminOrReadOnly()]
    
    @action(detail= False, methods= ['GET', 'PUT'], permission_classes= [IsAdminOrReadOnly])
    def me (self, request):
        member = Member.objects.filter(user_id=request.user.id).exclude(artistic_name= '').first()
        if member is None:
            return Response({'detail': 'You are not registered as a member'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer =  MemberSerializer(member)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = MemberSerializer(member, data= request.data)
            serializer.is_valid(raise_exception= True)
            serializer.save() 
            return Response(serializer.data) 
           
class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all() 
    serializer_class = ContractSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields= ['title', 'description']
    ordering_fields= ['member', 'title']
    permission_classes= [IsAdminUser]
  
      
class MusicDirectorViewSet(ModelViewSet):
    queryset =MusicDirector.objects.all()
    serializer_class= MusicDirectorSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields= ['notifications', 'sound_check_date', 'band_perfomance_details']
    ordering_fields= ['sound_check_date']
    permission_classes= [IsAdminUser]



class BandPackageViewSet(ModelViewSet):
    queryset = BandPackage.objects.all()
    serializer_class = BandPackageSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields= ['title', 'package_price']
    ordering_fields= ['package_price']
    permission_classes= [IsAdminOrReadOnly]
  

class AdditionalServicesViewSet(ModelViewSet):
    queryset = AdditionalService.objects.all()
    serializer_class = AdditionalServiceSerializer
    filter_backends= [SearchFilter]
    permission_classes= [IsClient]
    search_fields= ['title']


class ClientPerformanceViewSet(ModelViewSet):
    queryset = ClientPerformanceDetail.objects.all()
    serializer_class= ClientPerformanceDetailSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes= [IsClient]
    search_fields= ['show_title']
    ordering_fields= ['show_title', 'created_at']


  

class CalendarViewSet(ModelViewSet):
    queryset = Calender.objects.all()
    serializer_class= CalenderSerializer
    permission_classes= [IsAdminUser]
 

class AvailableServiceViewSet(ModelViewSet):
    queryset = AvailableService.objects.all()
    serializer_class= AvailableServiceSerializer
    permission_classes= [IsClient]


class ServiceOrderingViewSet(ReadOnlyModelViewSet):
    queryset = ServiceOrdering.objects.all()
    serializer_class= ServiceOrderingSerializer
    filter_backends= [ SearchFilter, OrderingFilter]
    permission_classes= [IsClient]

    search_fields= ['client']
    ordering_fields= ['placed_at']


class FinalServiceOrderApprovalViewSet(ModelViewSet):
    queryset = FinalServiceOrderApproval.objects.all()
    serializer_class= FinalServiceOrderApprovalSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [IsClient]
    search_fields= ['performance_title', 'price_breakdown', 'performance_requirements']
    ordering_fields= ['performance_title', 'service_ordered_detail']
    
    def get_permissions(self):
        if self.request == 'GET':
         return [IsClient()]
        else:
            return[IsAuthenticated()]     
    
class BandPackageReviewViewSet(ModelViewSet):  
    serializer_class= BandPackageReviewSerializer
    filter_backends= [SearchFilter]
    permission_classes = [AllowAny]
    search_fields= ['name']
    
    def get_queryset(self):
        band_package_id= self.kwargs['band_package_pk']
        return Review.objects.filter(band_package_id= band_package_id)

    def get_serializer_context(self):
        return {'band_package_id': self.kwargs['band_package_pk']}


 