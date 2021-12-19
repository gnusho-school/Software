import json, os, sys, django, re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "se.settings")
django.setup()

from timeline.models import Course
from django.db.models import Q

path = '/home/ubuntu/classlist-crawling/class_scheduler/프로젝트파일/'
file_list = os.listdir(path)
M = -1
Ms = None
major_set = set()
tag_set = set()
professor_set = set()
grade_set = set()

for f in file_list:
    
    with open(path + f) as ff:
        x = ff.read()
        x = re.sub('null', 'None', x)
        data_string = eval(x)['classList']
        
        tmp = set()

        for k in data_string: tmp.add(k)

        data = [eval(xx) for xx in tmp]
        major = f[:-5]
        major_set.add(major)
        
        for d in data:
            name = d['교과목명']
            tag = d['영역']
            grade = d['학년']
            classNum = d['반']
            classTime = d['수업시간']
            place = d['강의실']
            credit = d['학점']
            professor = d['교강사']

            tag_set.add(tag)
            professor_set.add(professor)
            grade_set.add(grade)

            if tag is None: tag = ''

            course = {
                'name': name,
                'tag': tag,
                'grade': grade,
                'classNum': classNum,
                'classTime': classTime,
                'place': place,
                'credit': credit,
                'professor': professor,
                'major': major
            }

            if place is None: continue
            M = max(M, len(place))
            if M == len(place): Ms = place

            if grade is None: grade = 0

            '''
            Course(
                name= name,
                tag= tag,
                grade= grade,
                classNum= classNum,
                classTime= classTime,
                place= place,
                credit= credit,
                professor= professor,
                major= major
            ).save()
            '''
print(major_set, tag_set, grade_set)      
'''
{
    1"grade/학년": None,
    2"classNum/반": None,
    3"tag/영역": "영역없음",
    4"name/교과목명": "Introductory Korean (Level 1)",
    5"professor/교강사": "김정훈",
    6"credit/학점": "3",
    7"time/수업시간": "집중수업",
    8"place/강의실": None,
    9"major/전공": None
}
'''