from django.db import models

class Course(models.Model):

    major = models.CharField(max_length = 200, null = True) # 전공
    name = models.CharField(max_length = 200) # 교과목명
    tag = models.CharField(max_length = 200, null = True) # 영역
    grade = models.IntegerField(null = True) # 학년
    classNum = models.IntegerField(null = True) # 반
    classTime = models.CharField(max_length = 200, null = True) # 수업시간
    place = models.CharField(max_length = 200, null = True) # 강의실
    credit = models.IntegerField() # 학점
    professor = models.CharField(max_length = 200, null = True) # 교수

    def __str__(self):
        return f'[{self.pk}] {self.name}'
