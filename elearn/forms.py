from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Announcement
        fields = ('content',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email','first_name', 'last_name','avatar','country','state','bio')
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email')
        

class InstructorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        
    def __init__(self, *args, **kwargs):
        super(InstructorSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
                    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_instructor = True
    #     if commit:
    #         user.save()
    #     return user

class LearnerSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)
    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(LearnerSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_learner = True
        user.save()
        learner = Learner.objects.create(user=user)
        learner.interests.add(*self.cleaned_data.get('interests'))
        return user

class LearnerInterestsForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('interests',)
        widgets = {
            'interests': forms.CheckboxSelectMultiple()
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    correct_answer = True
                    break
        if not correct_answer:
            raise forms.ValidationError('Mark at least one answer as correct.')
        
class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)
    class Meta:
        model = LearnerAnswer
        fields = ('answer',)
        
    def __init__(self,*args,**kwargs):
        question = kwargs.pop('question')
        super().__init__(*args,**kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
        
class LearnerCourse(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('interests',)
        widgets = {
            'interests': forms.CheckboxSelectMultiple()
        }
    
    @transaction.atomic
    def save(self):
        learner = Learner()
        learner.interests.add(*self.cleaned_data.get('interests'))
        return learner
    
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'course',)
        
class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ('course','title', 'content','thumb','video')
        
class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('course','title', 'cover','file')