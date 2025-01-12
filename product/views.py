from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.views.generic import ListView, DetailView
from product.forms import CommentForm
from django.http import HttpResponseRedirect
# Create your views here.
def list(request):
  data={'Posts':Post.objects.all().order_by("-date")}
  return render(request, 'bl/bl.html', data)
class PostListViews(ListView):
  queryset=Post.objects.all().order_by("-date")
  template_name='bl/bl.html'
  context_object_name='Post'
  paginate_by=1
def post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  form = CommentForm()
  if request.method=='POST':
    form=CommentForm(request.POST, author=request.user, post=post)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(request.path)
  return render(request,"bl/post.html",{"post":post,"form":form})
class PostDetaiView(DetailView):
  model = Post
  template_name='bl/post.html'