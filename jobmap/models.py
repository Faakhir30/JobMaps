from django.db import models

# Create your models here.
class Job(models.Model):
    title=models.CharField(max_length=200,null=True,blank=False)
    apply_linkedIn=models.TextField(default='')
    apply=models.TextField(default='')
    discription=models.TextField()
    company=models.CharField(max_length=200,null=True,blank=False,unique=False)
    location=models.CharField(max_length=200,null=True,blank=False)
    time=models.CharField(max_length=200,null=True,blank=False)
    company_linkedIn=models.TextField()

class LastRefreash(models.Model):
    date=models.CharField(max_length=200,blank=False)