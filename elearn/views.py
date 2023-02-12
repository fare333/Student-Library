from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
# from .models import Customer, Profile
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.core import serializers
from django.conf import settings
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, date
from django.core.exceptions import ValidationError
import operator
import itertools
from django.db.models import Avg, Count, Sum
from django.forms import inlineformset_factory
from .models import TakenQuiz, Profile, Quiz, Question, Answer, Learner, User, Course, Tutorial, Notes, Announcement
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)

from django.contrib.auth import update_session_auth_hash                                       


from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def services(request):
    return render(request,'services.html')

def sing_out(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request,user)
            if user.is_superuser or user.is_admin:
                return redirect("dashboard")
            elif user.is_instructor:
                return redirect("instructor")
            elif user.is_learner:
                return redirect("/")
    return render(request,'login.html')

def profile_management(request):
    user = request.user
    profile=Profile.objects.get(user=user)
    context = {'user':profile}
    return render(request,'dashboard/admin/profile_management.html',context)

def profile_update(request):
    user = request.user
    profile=Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()           
            return redirect('profile')
        
    context = {"form":form}
    return render(request,'dashboard/admin/profile_update.html',context)

#Admin views

def admin_dashboard(request):
    learners = User.objects.filter(is_learner=True).count()
    instructors = User.objects.filter(is_instructor=True).count() 
    courses = Course.objects.all().count()
    users = User.objects.all().count()
    context = {
        'learner': learners, 'instructor': instructors, 'course': courses, 'users': users
        }
    return render(request,'dashboard/admin/home.html',context)

def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request,'dashboard/admin/user_list.html',context)
    
def user_delete(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('users')

def add_instructor(request):
    form = InstructorSignUpForm
    if request.method == "POST":
        form = InstructorSignUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_instructor = True
            instance.save()
            return redirect('users')
    
    context = {"form":form}
    return render(request,'dashboard/admin/add_instructor.html',context)        

def make_course(request):
    if request.method == "POST":
        name = request.POST.get("name")
        color = request.POST.get("color")    
        new_course = Course(name=name,color=color)
        new_course.save()
        return redirect('dashboard')
    
    return render(request,'dashboard/admin/make_course.html')



def announcement_list(request):
    posts = Announcement.objects.all().order_by("-posted_at",)
    
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('announcement_list')

    context = {'posts': posts,"form":form}
    return render(request,'dashboard/admin/announcement_list.html',context)

def delete_ann(request,pk):
    post = Announcement.objects.get(id=pk)
    post.delete()
    return redirect('announcement_list')

#Learner views

def LearnerSignUp(request):
    form = LearnerSignUpForm()
    if request.method == "POST":
        form = LearnerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')    
    context = {"form":form}
    return render(request,'signup_form.html',context)
    
    
#Instructor views

def instructor_dashboard(request):
    learners = User.objects.filter(is_learner=True).count()
    instructors = User.objects.filter(is_instructor=True).count() 
    courses = Course.objects.all().count()
    users = User.objects.all().count()
    context = {"learners":learners,"instructors":instructors,"courses":courses,"users":users}
    return render(request,'dashboard/instructor/home.html',context)


def make_quiz(request):
    form = QuizForm()
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('quiz_list')
    context = {"form":form}
    return render(request,'dashboard/instructor/make_quiz.html',context)

def update_quiz(request,pk):
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz=quiz)
    form = QuizForm(instance=quiz)
    if request.method == "POST":
        form = QuizForm(request.POST,instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
        
    context = {"quiz":quiz,"form":form,"questions":questions}
    return render(request,'dashboard/instructor/update_quiz.html',context)

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by("-id",)
    taken = TakenQuiz.objects.filter(learner=request.user.learner)
    context = {"quizzes":quizzes,"taken":taken}
    return render(request,'dashboard/instructor/quiz_list.html',context)

def quiz_questions(request,pk):
    quiz = Quiz.objects.get(id=pk)
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.quiz = quiz
            instance.save()
            return redirect('quiz_questions',pk=pk)
    context = {"form":form,"quiz":quiz}
    return render(request,'dashboard/instructor/quiz_questions.html',context)

def question_delete(request,quiz_pk,question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)
    
    question.delete()
    return redirect('update_quiz',pk=quiz_pk)

def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)



    AnswerFormatSet = inlineformset_factory (
        Question,
        Answer,
        formset = BaseAnswerInlineFormSet,
        fields = ('text', 'is_correct'),
        min_num = 2,
        validate_min = True,
        max_num = 10,
        validate_max = True
        )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormatSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                formset.save()
                formset.save()
            messages.success(request, 'Question And Answers Saved Successfully')
            return redirect('update_quiz', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormatSet(instance=question)
    return render(request, 'dashboard/instructor/question_change.html', {
        'quiz':quiz,
        'question':question,
        'form':form,
        'formset':formset
        })        

def make_tutorial(request):
    form = TutorialForm()
    if request.method == "POST":
        form = TutorialForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('instructor')
    context = {"form":form}
    return render(request,'dashboard/instructor/make_tutorial.html',context)

def tutorial_list(request):
    tutorials = Tutorial.objects.all().order_by("-id",)
    context = {"tutorials":tutorials}
    return render(request,'dashboard/instructor/tutorial_list.html',context)

def tutorial_details(request,pk):
    tutorial = Tutorial.objects.get(id=pk)
    context = {"object":tutorial}
    return render(request,'dashboard/instructor/tutorial_details.html',context)

def notes(request):
    notes = Notes.objects.filter(user=request.user).order_by("-id",)
    context = {"notes":notes}
    return render(request,'dashboard/instructor/notes.html',context)

def add_notes(request):
    form = NoteForm()
    if request.method == "POST":
        form = NoteForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('notes')
    context = {"form":form}
    return render(request,'dashboard/instructor/add_notes.html',context)

def update_notes(request,pk):
    note = Notes.objects.get(id=pk)
    form = NoteForm(instance=note)
    if request.method == "POST":
        form = NoteForm(request.POST,request.FILES,instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes')
        
    context = {"form":form,"note":note}
    return render(request,'dashboard/instructor/notes_update.html',context)

#Learner views

def learner(request):
    learners = User.objects.filter(is_learner=True).count()
    instructors = User.objects.filter(is_instructor=True).count() 
    courses = Course.objects.all().count()
    users = User.objects.all().count()
    context = {"learners":learners,"instructors":instructors,"courses":courses,"users":users}
    return render(request,'dashboard/learner/home.html',context)

def quiz_results(request,pk):
    quiz = Quiz.objects.get(id=pk)
    taken_quizzes =quiz.taken_quizzes.select_related('learner__user').order_by('-date')
    results = QuizResults.objects.filter(user=request.user,quiz=quiz)
    context = {"results":results,"quiz":quiz,"taken_quizzes":taken_quizzes}
    return render(request,'dashboard/instructor/quiz_results.html',context)

def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    learner = request.user.learner

    if learner.quizzes.filter(pk=pk).exists():
        return redirect('quiz_results', quiz.pk)

    total_questions = quiz.questions.count()
    unanswered_questions = learner.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                learner_answer = form.save(commit=False)
                learner_answer.student = learner
                learner_answer.save()
                if learner.get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', pk)
                else:
                    correct_answers = learner.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(learner=learner, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'dashboard/learner/take_quiz.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })        

def taken_quizzes(request):
    taken_quizzes = TakenQuiz.objects.filter(learner=request.user.learner).order_by('-id')
    context = { 'taken_quizzes': taken_quizzes }
    return render(request, 'dashboard/learner/taken_quizzes.html', context)

def interests(request):
    form = LearnerInterestsForm()
    if request.method == 'POST':
        form = LearnerInterestsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.interests.add(*form.cleaned_data['interests'])
            instance.save()
            messages.success(request, 'Your interests have been updated successfully!')
            return redirect('interests')
    context = {'form': form }
    return render(request, 'dashboard/learner/interests.html', context)