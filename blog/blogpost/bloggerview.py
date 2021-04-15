from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .form import AddBloggerForm, AddBlogPostForm, PostForm, EditBlogPostForm, EditPostForm
from .models import CustomUser, Post
from django.contrib.auth import authenticate, login, logout

from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import  reverse_lazy





def postadd(request):
    form = AddBloggerForm()
    return render(request,'blog/addpost.html', {'form':form})


def Addpostform(request):
    user = request.user
    posts = Post.objects.filter(author=user).all().order_by('-sno')

    form = AddBlogPostForm()
    formp = PostForm()
    return render(request,'blog/addblogpostform.html', {'form':form, 'formp': formp, 'posts': posts, 'user': user})


def add_blogger_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddBloggerForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            about = form.cleaned_data['about']


            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, profile_pic=profile_pic_url, address=address, about=about )

                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('home')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('home')
        else:
            return redirect('home')




def add_Posts_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('home')
    else:
        form = AddBlogPostForm(request.POST, request.FILES)
        formp = PostForm(request.POST, request.FILES)

        if form.is_valid() and formp.is_valid():
            title = form.cleaned_data['title']
            about = formp.cleaned_data['about']
            content = formp.cleaned_data['content']
            user = request.user
            authorname = user.username
            category = formp.cleaned_data['category']


            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                cover_pic = request.FILES['cover_pic']
                fs = FileSystemStorage()
                filename = fs.save(cover_pic.name, cover_pic)
                cover_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                post = Post(title=title, author=user, content=content, about=about, cover_pic=cover_pic, author_name=authorname, category=category)
                post.save()
                messages.success(request, "Poat Added Successfully!")
                thispost = Post.objects.filter(title=title).first()
                postSno = thispost.sno

                return redirect('recipe', postSno)
            except:
                messages.error(request, "Failed to Add Post")
                return redirect('home')
        else:
            return redirect('home')






class EditBlogPost(UpdateView):
    model = Post
    template_name = 'blog/editpost.html'
    fields = ['title', 'cover_pic', 'category', 'about', 'content']


def delconf(request, pk):
    user = request.user
    obj = get_object_or_404(Post, sno=pk)
    return render(request, 'blog/delpost.html', {'obj': obj, 'user': user})



def DeletePost(request, pk):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return HttpResponse('wrong method')
    else:
        obj=get_object_or_404(Post, sno=pk)
        obj.delete()
        return redirect('home')

