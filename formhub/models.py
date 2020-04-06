from django.db import models

# Create your models here.

class Projects(models.Model):
    project_name = models.CharField(max_length=50)
    project_description = models.CharField(max_length=1000)
    project_status = models.CharField(max_length=50)
    github_link = models.CharField(max_length=100)
    circuit_link = models.CharField(max_length=100)
    project_leader = models.CharField(max_length=50)
    project_members = models.CharField(max_length=1000)
    project_date = models.CharField(max_length=50)
    languages = models.CharField(max_length=200)
    estimation = models.IntegerField()

    class Meta:
        db_table = "projects"
        
class FormhubUsers(models.Model):
    department = models.CharField(max_length=50)
    skills = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Users"