from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewsSerializer

class ReviewViewSet(ModelViewSet):
      queryset = Review.objects.all()
      serializer_class = ReviewsSerializer 
      permission_classes = [IsAuthenticatedOrReadOnly]

