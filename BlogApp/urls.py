from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.getRegister.as_view(),name="register"),
    path('login/',views.loginfunction.as_view(),name="login"),
    #path('logout/',LogoutView.as_view(),name="logout"),
    path('logout/',views.logoutfunction.as_view(),name="logout"),
    path('',views.getArticle.as_view(),name="index"),
    path('article/<pk>',views.ArticleDetails.as_view(),name="article"),
    path('category/<pk>',views.CategoryPost.as_view(),name="category"),
    path('profile',views.getProfile.as_view(),name="profile"),
    path('delete/<pk>',views.DeleteArticle.as_view(),name="delete"),
    path('update/<pk>',views.UpdateArticle.as_view(),name="update"),
    path('create',views.CreateArticle.as_view(),name="create"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('post_archive_month/<year>/<month>',views.ArticleSorting.as_view(),name='post_archive_month'),
    path('search/',views.ArticleSearch.as_view(),name="search"),
    path('about',views.getAbout.as_view(),name="about"),
    path('contact',views.getContact.as_view(),name="contact"),
 
]