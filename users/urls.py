from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, ContactView, SearchNameView, SearchNumberView, MarkSpamView
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user/contact', ContactView.as_view()),
    path('search_by_name/', SearchNameView.as_view()),
    path('search_by_number/', SearchNumberView.as_view()),
    path('mark_spam/', MarkSpamView.as_view()),
]