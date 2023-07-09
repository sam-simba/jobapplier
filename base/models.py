from django.db import models
from django.contrib.auth.models import User

class Field(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=500)
    hiring_mgr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=False, blank=False)
    applicants = models.ManyToManyField(User, related_name='applicants', blank=True)
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted']
    
    def __str__(self):
        return self.name
    
class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    interest = models.TextField()
    applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied']
    
    def __str__(self):
        return self.interest
    
        # return  str(self.applicant).capitalize() + ': ' + self.job.name[:29] + '... : Reason for applying, "'+ self.interest[:40] +'"'
    