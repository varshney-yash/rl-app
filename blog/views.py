from typing import Optional
from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
    )
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
    )
from .models import Post


def home(request):
    client_ip = get_client_ip(request)
    posts = Post.objects.all()
    print(posts)
    context={
        'posts':posts,
        'title':'Test'
        }
    print(context)
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if  self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home'

    def test_func(self):
        post = self.get_object()
        if  self.request.user == post.author:
            return True
        return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip