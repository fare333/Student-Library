from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_learner = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'images/', blank=True)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='none@email.com')
    birth_date = models.DateField(default='1975-12-12')
    bio = models.TextField(default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.user.username
    
@receiver(post_save,sender=User)
def make_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return str(self.content)


class Course(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Tutorial(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    thumb = models.ImageField(upload_to='', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/',blank=True, null=True)


class Notes(models.Model):
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to='', null=True, blank=True)
    cover = models.ImageField(upload_to='', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)    
        
        
class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    
    def questions_count(self):
        return self.questions.count()
    
    def taken_count(self):
        return self.taken_quizzes.count()

    def __str__(self):
        return self.name
    
class QuizResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    
    def calculate_score(self, answers):
        questions = Question.objects.filter(quiz=self.quiz)
        num_questions = questions.count()
        num_correct = 0
        for question, answer in zip(questions, answers):
            if question.correct_answer == answer:
                num_correct += 1
        self.score = num_correct / num_questions
        self.save()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text
    
    def answers_count(self):
        return self.answers.count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Course, related_name='interested_learners')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username



class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest = models.ManyToManyField(Course, related_name="more_locations")


class TakenQuiz(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)



class LearnerAnswer(models.Model):
    student = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')    

