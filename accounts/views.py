from django.views.generic import TemplateView
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.models import UserProfile, CoursesOffered, TutorProfile, StudentProfile, ClassRequest
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.forms import (RegistrationForm, UserInfoForm, CourseSelectionForm, LoginForm,
CourseSearchForm, TutorSearchForm, EditTutorProfileForm, EditStudentProfileForm, ClassRequestForm)


selected = ''
PRIMARY_CHOICES = ['Mathematics', 'English', 'Bangla', 'Science',]
SECONDARY_CHOICES = ['Mathematics', 'Physics',  'Chemistry', 'Biology', 'Social', 'English', 'Bangla']
HIGH_CHOICES = ['Mathematics', 'Physics',  'Chemistry', 'Biology', 'ICT', 'English', 'Bangla']


def user_logout(request):
    logout(request)
    template_name = 'accounts/logout.html'
    return render(request, template_name)


def user_login(request):
    template_name = 'accounts/login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:login_success')
        else:
            messages.error(request,'Invalid username or password')
    else:
        form = LoginForm()
    args = {'form': form}
    return render(request, template_name, args)

def student_messages(request):
    template_name = 'accounts/student-messages.html'
    user = request.user
    reqs = ClassRequest.objects.filter(req_to=user)
    args = {'reqs':reqs}
    return render(request, template_name, args)


def tutor_messages(request):
    template_name = 'accounts/tutor-messages.html'
    user = request.user
    reqs = ClassRequest.objects.filter(req_to=user)
    args = {'reqs':reqs}
    return render(request, template_name, args)



def class_request(request, pk):
    template_name = 'accounts/class-request.html'
    form = ClassRequestForm()
    msg_to = User.objects.get(pk=pk)
    reciever = msg_to.userprofile.full_name
    if request.method == 'POST':
        form = ClassRequestForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.req_to = msg_to
            t.user = request.user
            t.save()
            messages.success(request, 'Message sent')
        else:
            print (form.errors)
    args = {'form':form, 'reciever':reciever, 'sender':request.user.userprofile.full_name, 'msg_to':msg_to}
    return render(request, template_name, args)


def course_selection(request, subject = None):
    template_name = 'accounts/courses-selection.html'
    if request.method == 'POST' and 'searchBtn' in request.POST:
        form = CourseSearchForm(request.POST)
        if form.is_valid():
            global selected
            selected = form.cleaned_data['study_level']
            if(selected == 'Primary'): SUB_CHOICE = PRIMARY_CHOICES
            elif (selected == 'Secondary'): SUB_CHOICE = SECONDARY_CHOICES
            elif(selected == 'High School'): SUB_CHOICE = HIGH_CHOICES
        else: print(form.errors)
        args = {'form': form, 'subList': SUB_CHOICE}
        return render(request, template_name, args)
    if subject:
        trig = False
        check = CoursesOffered.objects.filter(study_level=selected, subject=subject)
        for e in check:
            if(str(e) == str(request.user)):
                trig = True
                break
        if not trig:
            temp = CoursesOffered()
            temp.city = request.user.userprofile.city
            temp.study_level = selected
            temp.subject = subject
            temp.user = request.user
            temp.save()
        return redirect('accounts:course_selection_view')
    else:
        form = CourseSearchForm()
        args = {'form': form, }
    return render(request, template_name, args)


def tutor_search(request, subject = None):
    template_name = 'accounts/tutor-search.html'
    if request.method == 'POST' and 'searchBtn' in request.POST:
        form = TutorSearchForm(request.POST)
        if form.is_valid():
            global selected
            selected = form.cleaned_data['study_level']
            if(selected == 'Primary'): SUB_CHOICE = PRIMARY_CHOICES
            elif (selected == 'Secondary'): SUB_CHOICE = SECONDARY_CHOICES
            elif(selected == 'High School'): SUB_CHOICE = HIGH_CHOICES
        else: print(form.errors)
        args = {'form': form, 'subList': SUB_CHOICE}
        return render(request, template_name, args)
    if subject:
        sub = subject
        city = request.user.userprofile.city
        stLevel = selected
        tutorList = CoursesOffered.objects.filter(city=city, study_level=stLevel, subject=sub)
        print(tutorList)
        form = TutorSearchForm()
        args = {'form': form, 'tutorList': tutorList, 'subject':sub, 'stlevel':stLevel}
        return render(request, template_name, args)
    else:
        form = TutorSearchForm()
        args = {'form': form, }
    return render(request, template_name, args)


def regprofile(request):
    template_name = 'accounts/regprofile.html'
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('accounts:login_success')
        else:
            print(form.errors)
    else:
        form = UserInfoForm()
    return render(request, template_name, {'form': form})


def student_profile(request, pk = None):
    if pk:
        user = User.objects.get(pk=pk)
        args = {'user':user}
        template_name = 'accounts/studentinfo.html'
    else:
        template_name = 'accounts/studentprofile.html'
        user = request.user
        args = {'user':user, 'st':True}
    return render(request, template_name, args)


def tutor_profile(request, pk = None):
    if(pk):
        user = User.objects.get(pk=pk)
        args = {'user':user}
        template_name = 'accounts/tutorinfo.html'
    else:
        user = request.user
        args = {'user':user,}
        template_name = 'accounts/tutorprofile.html'
    return render(request, template_name, args)


def edit_tutor_profile(request):
    template_name = 'accounts/edit-tutorprofile.html'
    if request.method == 'POST':
        form = EditTutorProfileForm(request.POST, request.FILES)
        if not TutorProfile.objects.filter(user=request.user).exists():
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                temp.save()
                messages.success(request, 'Changes Saved')
                #return redirect('accounts:tutor_profile_view')
            else:
                print(form.errors)
        else:
            if form.is_valid():
                temp = TutorProfile.objects.get(user=request.user)
                temp.edu_qualification = form.cleaned_data['edu_qualification']
                temp.expertise = form.cleaned_data['expertise']
                temp.tutor_image = form.cleaned_data['tutor_image']
                temp.description = form.cleaned_data['description']
                temp.charge_hr = form.cleaned_data['charge_hr']
                temp.save()
                messages.success(request, 'Changes Saved')
            else:
                print(form.errors)
    else:
        form = EditTutorProfileForm()
    args = {'form': form}
    return render(request, template_name, args)


def edit_student_profile(request):
    template_name = 'accounts/edit-studentprofile.html'
    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, request.FILES)
        if not StudentProfile.objects.filter(user=request.user).exists():
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                temp.save()
                messages.success(request, 'Changes Saved')
                #return redirect('accounts:tutor_profile_view')
            else:
                print(form.errors)
        else:
            if form.is_valid():
                temp = StudentProfile.objects.get(user=request.user)
                temp.school = form.cleaned_data['school']
                temp.grade = form.cleaned_data['grade']
                temp.student_image = form.cleaned_data['student_image']
                temp.description = form.cleaned_data['description']
                temp.fav_subjects = form.cleaned_data['fav_subjects']
                temp.save()
                messages.success(request, 'Changes Saved')
            else:
                print(form.errors)
    else:
        form = EditStudentProfileForm()
    args = {'form': form}
    return render(request, template_name, args)


def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('accounts:login_view'))
    else:
        form = RegistrationForm()
    return render(request, template_name, {'form': form,})

def login_success(request):
    userName = request.user.username
    st = False
    tu = False

    for e in UserProfile.objects.filter(user_type='Student'):
        if(str(e) == userName):
            st = True
            break
    if (st == False):
        for e in UserProfile.objects.filter(user_type='Tutor'):
            if(str(e) == userName):
                tu = True
                break

    if (st == True and tu == False):
        return redirect('accounts:student_profile_view')
    if (tu == True and st == False):
        return redirect('accounts:tutor_profile_view')
    if (tu == False and st == False):
        return redirect('accounts:user_info_view')


def home(request):
    return redirect('accounts:login_view')
