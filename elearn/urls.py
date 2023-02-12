from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path('contact/', views.contact, name='contact'),    
    path("about/",views.about,name="about"),
    path("services/",views.services,name="services"),
    
    path("login/",views.login_view,name="login"),
    path("logout/",views.sing_out,name="logout"),
    path("LearnerSignUp/",views.LearnerSignUp,name="LearnerSignUp"),
    
    path("dashboard/",views.admin_dashboard,name="dashboard"),
    path("users/",views.user_list,name="users"),
    path("user/delete/<str:pk>/",views.user_delete,name="user_delete"),
    path("add_instructor/",views.add_instructor,name="add_instructor"),
    path("new-course/",views.make_course,name="make_course"),
    path("announcement_list/",views.announcement_list,name="announcement_list"),
    path("delete_ann/<str:pk>/",views.delete_ann,name="delete_ann"),
    path("profile/",views.profile_management,name="profile"),
    path("profile_update/",views.profile_update,name="profile_update"),
    
    
    path("instructor/",views.instructor_dashboard,name="instructor"),
    path("make_quiz/",views.make_quiz,name="make_quiz"),
    path("update_quiz/<str:pk>/",views.update_quiz,name="update_quiz"),
    path("quiz_list/",views.quiz_list,name="quiz_list"),
    path("quiz_questions/<str:pk>/",views.quiz_questions,name="quiz_questions"),
    path("make_tutorial/",views.make_tutorial,name="make_tutorial"),
    path("tutorial_list/",views.tutorial_list,name="tutorial_list"),
    path("tutorial_details/<str:pk>/",views.tutorial_details,name="tutorial_details"),
    path("notes/",views.notes,name="notes"),
    path("add_notes/",views.add_notes,name="add_notes"),
    path("update_notes/<str:pk>/",views.update_notes,name="update_notes"),
    path("question_change/<str:quiz_pk>/<str:question_pk>/",views.question_change,name="question_change"),
    path("question_delete/<str:quiz_pk>/<str:question_pk>/",views.question_delete,name="question_delete"),
    path("quiz_results/<str:pk>/",views.quiz_results,name="quiz_results"),
    
    
    path("take_quiz/<str:pk>/",views.take_quiz,name="take_quiz"),
    path("learner/",views.learner,name="learner"),
    path("taken_quizzes/",views.taken_quizzes,name="taken_quizzes"),
    path("interests/",views.interests,name="interests")
]