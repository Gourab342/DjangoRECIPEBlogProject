
from django.urls import path
from . import views, bloggerview
from .bloggerview import EditBlogPost


urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.log_in, name="login"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('homead', views.homead, name="homead"),
    path('logout', views.log_out, name="logout"),

    path('posts', views.Posts, name="posts"),
    path('search', views.search, name="search"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),

    path('try', views.viewtry, name="try"),

    path('<int:sno>', views.recipe, name="recipe"),
    path('postComment', views.postComment, name="postComment"),

    path('test', views.test, name='test'),
    path('regform', views.regform, name='regform'),
    path('add_blogger_save/', views.add_blogger_save, name="add_bloggger_save"),
    path('add_Posts_save/', bloggerview.add_Posts_save, name="add_Posts_save"),
    path('Addpostform/', bloggerview.Addpostform, name="Addpostform"),
    path('<int:pk>/edit', EditBlogPost.as_view(), name="editpost"),
    path('<int:pk>/delete', bloggerview.DeletePost, name="deletepost"),
    path('<int:pk>/confirmdel', bloggerview.delconf, name="confirmdel"),
    path('category/<str:slug>', views.CategorySearch, name="category")




]