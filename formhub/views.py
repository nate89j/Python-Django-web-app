from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django import forms
import os
import magic
import json
from django.http import JsonResponse
from formhub.models import Projects,FormhubUsers
from datetime import datetime

def search_parameter(request):
    url_parameter = request.GET.get("q")
    if url_parameter:
        project_search = Projects.objects.filter(
            project_name__icontains=url_parameter)
    else:
        project_search = ''
    return project_search

def ajax_search(request,project_search):
        html = render_to_string(
            template_name="search.html",
            context={"project_search": project_search}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
        

@login_required(login_url='login')
def index(request):
    project_search = search_parameter(request)
    if request.is_ajax():
        return ajax_search(request, project_search)
    
    user = User.objects.get(username=request.session['username'])
    username, firstname, lastname = user.username, user.first_name, user.last_name
    projects = Projects.objects.all()
    return render(request, 'admins/index.html', {'firstname': firstname, 'lastname': lastname, 'username': username, 'projects': projects, 'project_search': project_search})


def register(request):
    return render(request, 'admins/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("user found")
            if user.is_active:
                request.session.set_expiry(86400)
                login(request, user)
                request.session['username'] = username
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html')


def logout_user(request):
    del request.session['username']
    logout(request)
    return HttpResponseRedirect("login")


@login_required(login_url='login')
def profile(request, profile_username):
    if request.method == 'GET':
        user = User.objects.get(username=request.session['username'])
        profile_user = User.objects.get(username=profile_username)
        formhub_user = FormhubUsers.objects.get(username=profile_username)
        username, firstname, lastname = user.username, user.first_name, user.last_name
        profile_firstname, profile_lastname, profile_department, profile_skills = profile_user.first_name, profile_user.last_name, formhub_user.department, formhub_user.skills
        projects = Projects.objects.all()
        for project in projects:
            project.project_members = json.loads(project.project_members)
        projectm = []
        for project in projects:
            if profile_username in project.project_members:
                projectm.append(project)

        project_search = search_parameter(request)
        if request.is_ajax():
            return ajax_search(request, project_search)
        
        return render(request, 'admins/profile.html', {'firstname': firstname, 'lastname': lastname, 'username': username,
                                                    'profile_username': profile_username, 'profile_firstname': profile_firstname,
                                                    'profile_lastname': profile_lastname, 'profile_department':profile_department, 'profile_skills':profile_skills, 'projects': projects, 'projectm': projectm, 'project_search':project_search})
    elif request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        FormhubUser = FormhubUsers.objects.get(username=request.session['username'])
        for key in request.POST.keys():
            if key == 'Firstname':
                user.first_name = request.POST.get('Firstname','')
                break;
            elif key == 'Lastname':
                user.last_name = request.POST.get('Lastname','')
                break;
            elif key == 'Department':
                FormhubUser.department = request.POST.get('Department','')
            elif key == 'Skills':
                FormhubUser.skills = request.POST.get('Skills','')

        user.save()
        FormhubUser.save()
        return HttpResponseRedirect('')

def forgot_password(request):
    return render(request, 'admins/forgot-password.html')


@login_required(login_url='login')
def project_add(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.session['username'])
        username, firstname, lastname = user.username, user.first_name, user.last_name
        return render(request, 'admins/project_add.html', {'firstname': firstname, 'lastname': lastname, 'username': username})
    elif request.method == 'POST':
        leader = request.session['username']
        members = json.dumps([request.session['username']])
        date = '{0:%d/%m/%Y }'.format(datetime.now())
        newProject=Projects(project_name = request.POST['inputName'], project_description = request.POST['inputDescription'], 
                            project_status = request.POST['inputStatus'], github_link = request.POST['inputGithub'], 
                            circuit_link = request.POST['inputCircuit'], project_leader = leader, project_members= members, 
                            project_date = date, languages = request.POST['inputLanguages'], estimation = request.POST['inputEstimation'] )
        newProject.save()
        return HttpResponseRedirect('/project_add')
    
@login_required(login_url='login')
def project_detail(request, project):
    user = User.objects.get(username=request.session['username'])
    username, firstname, lastname = user.username, user.first_name, user.last_name
    project = Projects.objects.get(project_name=project)
    project.project_members = json.loads(project.project_members)
    return render(request, 'admins/project_detail.html', {'firstname': firstname, 'lastname': lastname, 'username': username,'project':project})


@login_required(login_url='login')
def projects(request):
    projects = Projects.objects.all()
    # convert project members to list
    for project in projects:
        project.project_members = json.loads(project.project_members)
    user = User.objects.get(username=request.session['username'])
    username, firstname, lastname = user.username, user.first_name, user.last_name
    return render(request, 'admins/projects.html', {'firstname': firstname, 'lastname': lastname, 'username': username, 'projects': projects})

@login_required(login_url='login')
def project_edit(request, project):
    if request.method == 'GET':
        project = Projects.objects.get(project_name=project)
        user = User.objects.get(username=request.session['username'])
        username, firstname, lastname = user.username, user.first_name, user.last_name
        projectl = Projects.objects.filter(project_leader=username) 
        return render(request, 'admins/project_edit.html', {'firstname': firstname, 'lastname': lastname, 'username': username, 'project': project, 'projectl': projectl})
    elif request.method == 'POST':
        project = Projects.objects.get(project_name=project)
        print('project:' + str(project))
        project.project_description = request.POST['inputDescription']
        project.project_status = request.POST['inputStatus']
        project.languages = request.POST['inputLanguages']
        project.estimation = request.POST['inputEstimation']
        project.github_link = request.POST['inputGithub']
        project.circuit_link = request.POST['inputCircuit']
        project.save()
        return HttpResponseRedirect('/project_edit/' + project.project_name)
    
@login_required(login_url='login')
def project_edit_def(request):
    user = User.objects.get(username=request.session['username'])
    username, firstname, lastname = user.username, user.first_name, user.last_name
    projectl = Projects.objects.filter(project_leader=username)
    return render(request, 'admins/project_edit_def.html', {'firstname': firstname, 'lastname': lastname, 'username': username, 'projectl': projectl})
