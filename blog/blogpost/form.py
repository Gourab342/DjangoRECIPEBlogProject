from django import forms
from .models import CustomUser, Post
from ckeditor.fields import RichTextField
from django.views.generic import UpdateView


#DataFlair #File_Upload


class AddBloggerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    about = forms.CharField(label="About", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class": "form-control"}))



class ProfilePicFrom(forms.Form):
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class": "form-control", "id": "wizard-picture" }))

class UserDetailForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"(Must Be Unique)"}))

    def clean_name(self):
        username = self.cleaned_data.get('username')


        if CustomUser.objects.filter(username=username).count():
            raise forms.ValidationError(
                'This email address is already in use. Please supply a different email address.')
        return username





class passform(forms.Form):
    password = forms.CharField(label="Password", max_length=50,widget=forms.PasswordInput(attrs={"class": "form-control"}))



class First_nameForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))



class Last_nameForm(forms.Form):
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AboutForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=300, widget=forms.Textarea(attrs={"class": "form-control", "rows":3}))
    about = forms.CharField(label="About", max_length=300, widget=forms.Textarea(attrs={"class": "form-control", "rows":3}))



class AddBlogPostForm(forms.Form):
    title = forms.CharField(label="title", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    cover_pic = forms.FileField(label="Add a Cover Pic", required=False, widget=forms.FileInput(attrs={"class": "form-control"}))



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'content', 'about', 'category'}

class EditBlogPostForm(forms.Form):
    title = forms.CharField(label="title", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    cover_pic = forms.FileField(label="Add a Cover Pic", required=False, widget=forms.FileInput(attrs={"class": "form-control"}))


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'category', 'about', 'content'}


