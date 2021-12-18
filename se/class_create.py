import json, os, sys, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "se.settings")
django.setup()

from timeline.models import Course
from django.db.models import Q

class_set = set()

with open('class.json') as f:
    data = json.load(f)
    classList = data["classList"]

    for c in classList:
        print(c)
        class_set.add(c)
    
'''
{
    "grade/학년": None,
    "classNum/반": None,
    "tag/영역": "영역없음",
    "name/교과목명": "Introductory Korean (Level 1)",
    "professor/교강사": "김정훈",
    "credit/학점": "3",
    "time/수업시간": "집중수업",
    "place/강의실": None
}
'''