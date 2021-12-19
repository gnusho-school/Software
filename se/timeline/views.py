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
    
        data = request.data
        major = data['major']
        grade = data['grade']
        max_credit = data['max_credit']
        min_credit = data['min_credit']
        min_major_credit = data['min_major_credit']
        major_list = data['major_list'] #id list
        ge_list = data['ge_list'] #id list

        credits = 0
        major_credits = 0
        must = []
        # major_list 처리
        for id in major_list:
            tmp = Course.objects.filter(Q(id = id))[0]
            must.append({
                'id' : tmp.id,
                'name' : tmp.name,
                'session' : make_time(tmp),
                'place' : tmp.place,
                'credit' : tmp.credit,
            })
            major_credits += tmp.credit
            credits += tmp.credit

        # ge_list 처리
        for id in ge_list:
            tmp = Course.objects.filter(Q(id = id))[0]
            must.append({
                'id' : tmp.id,
                'name' : tmp.name,
                'session' : make_time(tmp),
                'place' : tmp.place,
                'credit' : tmp.credit,
            })
            credits += m.credit

        major_course = Course.objects.filter(
            Q(major = major) & Q(grade = grade)
        )

        ge_course = Course.objects.filter(
            Q(major = "서울 교양 전체")
        )

        major = {}

        for m in major_course:
            if "시간미지정강좌" in m.classTime: continue
            tmp = make_time(m)
            major[m.id] = {
                'id': m.id,
                'name': m.name,
                'session': tmp,
                'place': m.place,
                'credit': m.credit,
            }

        recommends = get_recommmend(major, max_credit, min_credit, min_major_credit, must, major_credits, credits)

        return Response(recommends)

def get_recommmend(major, max_credit, min_credit, min_major_credit, must, major_credits, credits):

    major_c = []
    major_check = [False for key,val in major.items()]
    
    mmm = list(major.values())
    tmp = [x['id'] for x in must]
    for i in range(len(mmm)):
        if mmm[i]['id'] in tmp: major_check[i] = True
    
    major_dfs(major_check, list(major.values()), 0, credits, major_credits, max_credit, min_credit, min_major_credit, major_c, must)

    return major_c


def major_dfs(check, major, now_place, credits, major_credits, max_credit, min_credit, min_major_credit, major_c, must):

    if len(major_c) >= 3: return

    if credits >= min_credit and credits <= max_credit and major_credits >= min_major_credit:
        tmp = [major[i] for i in range(len(check)) if check[i] == True]
        #for x in must: tmp.append(x)
        major_c.append(tmp)
    
    if len(major) < now_place: return
    
    for i in range(now_place, len(major)):
        
        course = major[i]
        if credits + course['credit'] > max_credit: continue

        overlap = False

        for j in range(len(check)):
            if check[j] == False: continue
            if major[j]['name'] == course['name']:
                overlap = True
                break

            for t in major[j]['session']:
                for tt in course['session']:
                    if t[0] != tt[0]: continue
                    if tt[1][0] < t[1][0] and tt[1][1] < t[1][0]: continue
                    if tt[1][0] > t[1][1] and tt[1][1] > t[1][1]: continue
                    overlap = True
                    break
            if overlap == True: break

        for mu in must:
            print(mu)
                
        if overlap == True: continue
        
        check[i] = True
        major_dfs(check, major, i + 1, credits + course['credit'], major_credits + course['credit'], max_credit, min_credit, min_major_credit, major_c, must)
        check[i] = False
        

def ge_dfs(check, ge, now_place, credits, max_credit, min_credit, ge_c):
    print("in dfs")



def make_time(string):
    tmp = string.classTime.split(')')[:-1]
    ret = [x.split('(') for x in tmp]

    for r in ret:
        r[1] = r[1].split("-")
        r[1][0] = datetime.strptime(r[1][0], '%H:%M')
        r[1][1] = datetime.strptime(r[1][1], '%H:%M')

    return ret