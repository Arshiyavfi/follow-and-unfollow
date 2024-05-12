from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .form import UseRegesterationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.views import Post
from .models import Relation

# Create your views here.
class RegesterView(View):
    form_class = UseRegesterationForm
    template_name = 'account/regester.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'regester done.', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully', 'succsess')
                return redirect('home:home')
            messages.error(request, 'username or password is wrong.', Warning)
        return render(request, self.template_name, {'form':form})
    
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You log out.', 'success')
        return redirect('home:home')
    
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            if_following = True
        return render(request, 'account/profile.html', {'user':user, 'posts':posts, 'if_following':if_following })
    
class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You have already follow each other', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'You followed this user', 'SUCCESS')
        return redirect('account:user_profile', user.id)
    
class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You unfollowed this user', 'SUCCESS')
        else:
            messages.error(request, 'You have follow each other.', 'danger')
        return redirect('account:user_profile', user_id)
    
    

