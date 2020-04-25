from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from home.forms import (
    RegistrationForm,
    EditProfileForm,
    AnswerForm,
    AskQuestionForm,
)
from django.contrib.auth.models import User
from home.models import Question,Answer
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
'''
def index(request):
    my_dict={'insert_me':"Hello I am from home/index.html!"}
    return render(request,'home/index.html',context=my_dict)
'''
def welcome(request):
    return render(request,'home/homepage.html')

#def login(request):
#    return render(request,'home/login.html')

def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login')
        else:
            redirect('/account/register')
    else:
        form = RegistrationForm()

        args={'form':form}
        return render(request, 'home/register.html', args)

def about(request):
    return render(request, 'home/about.html')

class testpage(TemplateView):
    template_name='home/dashboard.html'


class testpage2(TemplateView):
    template_name='home/homepage.html'

@login_required
def view_profile(request):
    args= {'user': request.user}
    return render(request, 'home/profile.html',args)

@login_required
def edit_profile(request):
    if request.method== 'POST':
        form= EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')
        else:
            return redirect('/account/profile/edit')

    else:
        form= EditProfileForm( instance=request.user)
        args = {'form': form}
        return render(request, 'home/edit_profile.html', args)

@login_required
def change_password(request):
    if request.method=="POST":
        form= PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/profile/edit/change-password')
    else:
        form= PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'home/change_password.html', args)


def redirect_password(request):
    return redirect('/account/profile/edit/change-password')

#
# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/account/feed')
#     else:
#         form = DocumentForm()
#     return render(request, 'home/model_form_upload.html', {
#         'form': form
#     })
def list_of_questions(request):
    question=Question.objects.all()
    paginator=Paginator(question, 3)
    page = request.GET.get('page')
    try:
        questions=paginator.page(page)
    except PageNotAnInteger:
        questions=paginator.page(1)
    except EmptyPage:
        questions=paginator.page(paginator.num_pages)
    return render(request, 'home/dashboard.html', {'questions':questions, 'page':page} )

def view_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    args={'question':question}
    return render(request, 'home/view_question.html', args)

def add_answer(request,slug):
    question=get_object_or_404(Question, slug=slug)
    if request.method== 'POST':
        form=AnswerForm(request.POST)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.user=request.user
            answer.email=request.user.email
            answer.question=question
            answer.save()
            return redirect('home:view_question',slug=question.slug)
    else:
        form=AnswerForm()
        return render(request, 'home/add_answer.html', {'form':form, 'question':question} )

def ask_question(request):
    if request.method == "POST":
        form= AskQuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.save()
            return redirect('home:view_question', slug=question.slug)
    else:
        form = AskQuestionForm()
        args = {'form': form}
        return render(request, 'home/ask_question.html', args)
