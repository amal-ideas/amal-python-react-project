from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
##from .forms import VideoForm
from .models import Post, PostReaction, UserInfo, Comment, Party, PartyTestimonial, Status, UserTag, Tag
from django.forms import formset_factory
from .forms import UserForm, UserProfileInfoForm, LocationForm, PartyForm, PostForm, TagForm, CommentForm, UserEditForm, UserInfoEditForm, PostReactionForm, PartyTestimonialForm, UserTagForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.utils.timezone import now
from django.views import View
from .signals import create_profile
from django.http import HttpResponseNotFound
from sentry_sdk import capture_message
from django.core.mail import send_mail
from .tasks import count_posts


# Create your views here
@csrf_exempt
def index(request):
    current_tag = Tag.objects.filter(userinfo__user_id=request.user.pk)
    post = Post.objects.order_by('-create_at').exclude(deleted=1)
    reaction = PostReaction.objects.all()
    tag = UserTag.objects.all()
    comment = Comment.objects.order_by('-postDate')
    comment_id_list = Comment.objects.values_list('postID_id', flat=True)
    top_post = Post.objects.order_by('-create_at').filter(id__in=comment_id_list)[:5]
    ##myvideoform = VideoForm()
    return render(request, 'politricks/index.html', {'posts': post, 'reactions': reaction, 'comments': comment, 'count': count_posts, 'topPost': top_post, 'tags': tag })


def userprofile(request, user_id):
    if request.user.is_authenticated:
        pass
    else:
        return render(request,'politricks/login.html')
    user = UserInfo.objects.filter(user=user_id).first()
    post = Post.objects.filter(userID=user.pk)
    reaction = PostReaction.objects.all()
    current_user = UserInfo.objects.filter(user=request.user).first()
    return render(request, 'politricks/userProfile.html', {'user': user, 'reactions': reaction, 'posts': post,
                                                           'current_user': current_user})


class UserEdit(View):
    template_name = 'politricks/userEdit.html'
    user_id = None
    userform_class = UserEditForm
    userinfoform_class = UserInfoEditForm

    def getuser(self, request):
        if self.user_id:
            user = get_object_or_404(UserInfo, pk=self.user_id)
        else:
            user = UserInfo.objects.filter(user=request.user).first()
        return user

    def get(self, request):
        user_form = self.userform_class(data=request.POST or None, instance=request.user)
        profile_form = self.userinfoform_class(data=request.POST or None, instance=self.getuser(request))
        return render(request, self.template_name, {'user_form': user_form,
                                'profile_form': profile_form})

    def post(self, request):
        user_form = self.userform_class(data=request.POST or None, instance=request.user)
        profile_form = self.userinfoform_class(data=request.POST or None, instance=self.getuser(request))
        if request.POST and user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.photo = request.FILES['photo']
            profile.save()

            messages.success(request, 'Your profile has been updated!')
            # Save was successful, so redirect to another page

            return HttpResponseRedirect(reverse('index'))
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })


class UserList(View):
    template_name = 'politricks/userList.html'
    status = Status.objects.filter(label='hidden').first()
    userinfo = UserInfo.objects.select_related('user').order_by('user__username')
    users = []

    def get(self, request):
        for user in self.userinfo:
            if (user.user == request.user):
                self.users.append(user)
            else:
                if user.status != self.status:
                    self.users.append(user)
        return render(request, self.template_name, {'users': self.users})


def partydetail(request, party_id):
    if request.user.is_authenticated:
        pass
    else:
        return render(request,'politricks/login.html')
    party = get_object_or_404(Party, pk=party_id)
    ##owner = get_object_or_404(UserInfo, pk=post.userID.pk)
    post = Post.objects.filter(partyID=party)
    testimonials = PartyTestimonial.objects.filter(party=party)
    current_user = UserInfo.objects.filter(user=request.user).first()
    partyTestimonial_form = PartyTestimonialForm(data=request.POST)

    if partyTestimonial_form.is_valid():
        partyTestimonial = partyTestimonial_form.save(commit=False)
        partyTestimonial.user = current_user
        partyTestimonial.party = party
        partyTestimonial.created = now()
        partyTestimonial.lastmodified = now()
        partyTestimonial.save()
        messages.success(request, 'Your added a testimonials!')
    partyTestimonial_form = PartyTestimonialForm()
    return render(request, 'politricks/partyDetail.html',
                      {'party': party, 'posts': post, 'current_user': current_user,
                       'partyTestimonial_form': partyTestimonial_form, 'testimonials': testimonials})

def postdetail(request, post_id):
    if request.user.is_authenticated:
        pass
    else:
        return render(request, 'politricks/login.html')
    supportedcurrentuser = False
    unsupportedcurrentuser = False
    post = get_object_or_404(Post, pk=post_id)
    comment_id_list = Comment.objects.values_list('postID_id', flat=True)
    top_post = Post.objects.order_by('-create_at').filter(id__in=comment_id_list).exclude(pk=post.pk)[:5]
    owner = get_object_or_404(UserInfo, pk=post.userID.pk)
    reaction = PostReaction.objects.filter(postId=post_id)
    comments = Comment.objects.filter(postID=post.pk)
    if request.method == 'POST':
        reaction_form = PostReactionForm(data=request.POST)
        if reaction_form.is_valid():
            if 'support' in request.POST:
                if reaction and reaction.get(postId=post.pk):
                    update_reaction = reaction.get(postId=post.pk)
                    update_reaction.supportCnt.add(UserInfo.objects.filter(user=request.user).first())
                    update_reaction.unSupportCnt.remove(UserInfo.objects.filter(user=request.user).first())
                else:
                    reaction_object = reaction_form.save(commit=False)
                    reaction_form.save()
                    reaction_object.supportCnt.add(UserInfo.objects.filter(user=request.user).first())
            if 'unsupport' in request.POST:
                if reaction and reaction.get(postId=post.pk):
                    update_reaction = reaction.get(postId=post.pk)
                    update_reaction.unSupportCnt.add(UserInfo.objects.filter(user=request.user).first())
                    update_reaction.supportCnt.remove(UserInfo.objects.filter(user=request.user).first())
                else:
                    reaction_object = reaction_form.save(commit=False)
                    reaction_form.save()
                    reaction_object.unSupportCnt.add(UserInfo.objects.filter(user=request.user).first())
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.postID = post
            comment.user = UserInfo.objects.filter(user=request.user).first()
            comment.postDate = now()
            comment_form.save()
            messages.success(request, 'Your added a comment!')
    if reaction and reaction.get(postId=post.pk):
        if reaction.get(postId=post.pk).supportCnt.filter(user=request.user).exists():
            supportedcurrentuser = True
        if reaction.get(postId=post.pk).unSupportCnt.filter(user=request.user).exists():
            unsupportedcurrentuser= True
    comment_form = CommentForm()
    reaction_form = PostReactionForm()
    current_user = UserInfo.objects.filter(user=request.user).first()
    return render(request, 'politricks/postDetail.html', {'owner': owner, 'reactions': reaction, 'post': post,
                                                          'comments': comments, 'comment_form': comment_form,
                                                          'current_user': current_user, 'reaction_form': reaction_form,
                                                          'unsupportedcurrentuser': unsupportedcurrentuser, 'supportedcurrentuser': supportedcurrentuser,'top_post': top_post})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            to_email = user_form.cleaned_data.get('email')
            username = user_form.cleaned_data.get('username')
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            create_profile(True)
            messages.success(request, f'Account created for {username}!')
            send_mail('Account Created!',
                      'Visit politircks.me and login.',
                      'unniya01@myunitec.ac.nz',
                      [
                          to_email,
                      ], fail_silently=False)
        else:
            capture_message(user_form.errors, level="error")
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'politricks/register.html',
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def postupdate(request):
    success = False
    parties = Party.objects.all()
    tags = []
    if request.method == 'POST':
        post_form = PostForm(data=request.POST, prefix='post',)
        location_form = LocationForm(data=request.POST)
        party_form = PartyForm(data=request.POST, prefix='party',)
        tag_form = TagForm(data=request.POST)
        usertag_form = UserTagForm(data=request.POST, prefix='usertag',)
        usertag = UserTag.objects.all()
        if tag_form.is_valid():
            name = tag_form.cleaned_data['name']
            tag_form.save()
            recent_tag = Tag.objects.filter(name__exact=name).order_by('id')[0]
            tags.append(recent_tag)
        if post_form.is_valid() and location_form.is_valid() and party_form.is_valid():
            location = location_form.save()
            party = party_form.save()
            post = post_form.save(commit=False)
            post.locationID = location
            post.create_at = now()
            post.partyID = party
            if 'post-picture' in request.FILES:
                post.picture = request.FILES['post-picture']
            if (UserInfo.objects.filter(user=request.user)):
                post.userID = UserInfo.objects.filter(user=request.user).first()
            else:
                render(request, 'politricks/login.html')
            post.save()
            if post_form.cleaned_data.get('postTag'):
                for value in post_form.cleaned_data.get('postTag'):
                    tags.append(value)
                for _tag in tags:
                    post.postTag.add(_tag)
                    if usertag_form.is_valid():
                        if usertag and UserTag.objects.filter(tagId=_tag).exists():
                            update_usertag = usertag.get(tagId=_tag)
                            update_usertag.postId.add(post)
                        else:
                            usertag_object = usertag_form.save(commit=False)
                            usertag_object.tagId = _tag
                            usertag_object.save()
                            usertag_object.postId.add(post)
            success = True
            messages.success(request, 'Your post was successfully updated!')
        else:
            capture_message(post_form.errors, level="error")
            print(post_form.errors, location_form.errors, party_form.errors)
    else:
        post_form = PostForm(prefix='post',)
        party_form = PartyForm(prefix='party',)
        usertag_form = UserTagForm(prefix='usertag', )
        location_form = LocationForm()
        tag_form = TagForm()
    return render(request, 'politricks/postAdd.html',
                  {'post_form': post_form,
                           'party_form': party_form,
                           'location_form': location_form,
                           'tag_form': tag_form,
                           'success': success, 'parties': parties, 'usertag_form': usertag_form})


def postedit(request, post_id=None, template_name='politricks/postEdit.html'):
    if id:
        post = get_object_or_404(Post, pk=post_id)
    else:
        post = Post(userID=UserInfo.objects.filter(user=request.user).first())

    form = PostForm(request.POST or None, instance=post)
    if request.POST and form.is_valid():
        post = form.save(commit=False)
        if 'picture' in request.FILES:
            post.picture = request.FILES['picture']
        post.save()
        messages.success(request, 'Your post was successfully updated!')
        # Save was successful, so redirect to another page

        return HttpResponseRedirect(reverse('index'))

    return render(request, template_name, {
        'form': form
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Your are successfully logged in!')
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'politricks/login.html', {})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'politricks/change_password.html', {
        'form': form
    })


def my_custom_page_not_found_view(*args, **kwargs):
    capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseNotFound("Not found")