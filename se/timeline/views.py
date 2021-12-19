from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Course
from .serializer import CourseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
import json

class CourseListAPI(APIView):

    # GET
    def get(self, request):

        major = request.GET.get('major', None)
        print(major)

        if major is None:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        name = request.GET.get('name', '') 
        tag = request.GET.get('tag', None) 
        grade = request.GET.get('grade', None)
        
        query = Q(major = major) & Q(name__contains = name)

        if tag is not None:
            query = query & Q(tag = tag)
        
        if grade is not None:
            query = query & Q(grade = grade)
            
        q = Course.objects.filter(query)
        ret = CourseSerializer(q, many = True).data

        return Response(ret)

class CourseRecommendAPI(APIView):

    # Post
    '''
    Body로 받을 값
    1. 전공: string/major
    2. 학년: int/grade
    3. 최대 학점: int/max_credit
    4. 최소 학점: int/min_credit
    5. 최소 전공 학점: int/min_major_credit
    6. 포함시킬 전공 과목: id array/major_list
    7. 포함시킬 교양 과목: id array/ge_list
    '''
    def post(self, request):
        
        data = request.data.dict()

        major = data['major']
        grade = data['grade']
        max_credit = data['max_credit']
        min_credit = data['min_credit']
        min_major_credit = data['min_major_credit']
        major_list = data['major_list']
        ge_list = data['ge_list']

        return Response(data)