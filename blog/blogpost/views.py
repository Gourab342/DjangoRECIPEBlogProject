from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser, Post, BlogComment, Category, contact
from django.contrib.auth import authenticate, login, logout
from math import ceil
from django.core.files.storage import FileSystemStorage
from .form import AddBloggerForm, AddBlogPostForm, PostForm, AboutForm, ProfilePicFrom, UserDetailForm
from .form import First_nameForm, Last_nameForm, passform
from django.core.paginator import  Paginator, EmptyPage




def regform(request):
    form = ProfilePicFrom()
    formud = UserDetailForm()
    formfn = First_nameForm()
    formln = Last_nameForm()
    formab = AboutForm()
    formpass = passform()
    return render(request, 'template/home.html', {'form': form, 'formud': formud, 'formfn': formfn, 'formln': formln, 'formab': formab, 'formpass': formpass})



def add_blogger_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = ProfilePicFrom(request.POST, request.FILES)
        formud = UserDetailForm(request.POST)
        formfn = First_nameForm(request.POST)
        formln = Last_nameForm(request.POST)
        formab = AboutForm(request.POST)
        formpass = passform(request.POST)

        if (form.is_valid() and formud.is_valid()) and ((formfn.is_valid() and formln.is_valid()) and (formab.is_valid() and formpass.is_valid())):
            first_name = formfn.cleaned_data['first_name']
            last_name = formln.cleaned_data['last_name']
            username = formud.cleaned_data['username']
            email = formab.cleaned_data['email']
            password = formpass.cleaned_data['password']
            address = formab.cleaned_data['address']
            about = formab.cleaned_data['about']


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







def home(request):
    allPosts = Post.objects.all().order_by('-sno')
    cats = Category.objects.all()
    n = len(allPosts)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))

    context = {'allPosts': allPosts, 'no_of_slides':nSlides, 'range': range(1,nSlides), 'product': allPosts, 'cats': cats}
    return render(request, 'webpage/sample.html', context)


def register(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('register')
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.POST.get('profile_pic')
        about = request.POST.get('userabout')
        address = request.POST.get('useraddress')

        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None



        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, profile_pic=profile_pic, address=address, about=about )
            user.save()
            messages.success(request, "Added Successfully!")
            return redirect('home')
        except:
            messages.error(request, "Failed to Add!")
            return redirect('home')


def log_in(request):
    return render(request, 'blog/login.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = authenticate(request, username=request.POST.get('username'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('home')


def homead(request):
    return render(request, 'template/home.html')

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def Posts(request):
    allposts = Post.objects.all().order_by('-sno')

    p = Paginator(allposts, 10)
    page_num =request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {'allPosts': page}
    return render(request, 'blog/posts.html', context)


def search(request):
    query=request.GET['query']
    posts = Post.objects.all().order_by('-sno')
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query, 'posts': posts}
    return render(request, 'blog/search.html', params)

def viewtry(request):
    return render(request, 'blog/try.html')



def recipe(request, sno):
    post=Post.objects.filter(sno=sno).first()
    user = post.author
    allposts = Post.objects.filter(author=user)
    comments = BlogComment.objects.filter(post=post)
    context={"post":post, "comments": comments, 'user': request.user, 'allposts': allposts}
    return render(request, "blog/recipe.html", context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        comment = BlogComment(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    return redirect(f"/{postSno}")



def test(request):
    allposts = Post.objects.all().order_by('-sno')
    return render(request,'webpage/test.html', {'posts': allposts})


def CategorySearch(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    catposts = Post.objects.filter(category=cat)
    posts = Post.objects.all()
    return render(request, 'blog/categorypage.html', {'catposts': catposts, 'posts': posts, 'cat': cat})


def contact(request):
    if request.method=="POST":
        name=request.POST['c_name']
        email=request.POST['c_email']
        subject =request.POST['c_subject']
        text =request.POST['c_text']
        cont=contact(name=name, email=email, subject=subject, text=text)
        if len(name) < 2 or len(email) < 3 or len(text) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            cont = contact(name=name, email=email, subject=subject, text=text)
            cont.save()
            messages.success(request, "Your message has been successfully sent")

    return render(request,'webpage/contact.html')


def about(request):
    return render(request, 'webpage/about.html')

