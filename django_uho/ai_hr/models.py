from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    cv = models.FileField(upload_to='cvs/')

class JobCriteria(models.Model):
    job_title = models.CharField(max_length=100)
    skills = models.JSONField()  # ['skill_a', 'skill_b', 'skill_c']
    
class InterviewStage(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    stage = models.CharField(max_length=100)
    score = models.FloatField(null=True, blank=True)  # Score based on smart CV reading or interview