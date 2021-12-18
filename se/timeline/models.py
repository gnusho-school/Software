from django.db import models

class Course(models.Model):
    name = models.CharField(max_length = 20) # 교과목명
    tag = models.CharField(max_length = 20) # 영역
    grade = models.IntegerField() # 학년
    classNum = models.IntegerField(null = True) # 반
    classTime = models.CharField(max_length = 20) # 수업시간
    place = models.CharField(max_length = 20, null = True) # 강의실
    credit = models.IntegerField() # 학점

    def __str__(self):
        return f'[{self.pk}] {self.name}'
