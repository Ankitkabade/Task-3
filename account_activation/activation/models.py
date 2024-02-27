from django.db import models



class Student(models.Model):
    roll_no =models.IntegerField()
    f_name = models.CharField(max_length=45)
    l_name= models.CharField(max_length=45)
    emial = models.EmailField()
    address = models.TextField()

