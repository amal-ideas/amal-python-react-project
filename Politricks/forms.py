from django import forms
from .models import UserInfo, Post, Party, Location, Tag, Comment, PostReaction, PartyTestimonial, UserTag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserInfo
         fields = ('address', )


class LocationForm(forms.ModelForm):
    class Meta():
        model = Location
        fields = ('name', 'shortName')


class PartyForm(forms.ModelForm):
    class Meta():
        model = Party
        fields = ('title', 'description')


class TagForm(forms.ModelForm):
    class Meta():
        model = Tag
        fields = ('name',)


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('content',)


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'description', 'picture', 'postTag')


class UserEditForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name',)


class UserInfoEditForm(forms.ModelForm):
    class Meta():
        model = UserInfo
        fields = ('address', 'photo', 'tag',)


class PostReactionForm(forms.ModelForm):
    class Meta():
        model = PostReaction
        fields = ('postId',)


class UserTagForm(forms.ModelForm):
    class Meta():
        model = UserTag
        fields = ('tagId',)


class PartyTestimonialForm(forms.ModelForm):
    class Meta():
        model = PartyTestimonial
        fields = ('title', 'description', 'rating')
