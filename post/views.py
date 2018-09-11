from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import PostForm 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    posts = Post.objects.all().order_by('-id')

    paginator = Paginator(posts, 3) # < 3 is the number of items on each page
    page = request.GET.get('page') # < Get the page number
    posts = paginator.get_page(page) # < New in 2.0!

    context = {
        'posts': posts,
    }
    return render(request, 'post/index.html', context)


def post_detail(request, id=None):
    pd = get_object_or_404(Post, id=id)
    context = {
        'pd': pd,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_update(request, id=None):
    pd = get_object_or_404(Post, id=id)
    print(f'from func {pd.author}')
    if request.user == pd.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=pd)
            if form.is_valid:
                form.save()
                return redirect('post_detail', id=id)
        else:
            form = PostForm()

        context = {
            'form': form,
        }
    if request.user != pd.author:
        context = {'error': "You cant change someone else's content"}
    return render(request, 'post/post_update.html', context)


@login_required
def post_delete(request, id=None):
    pd = get_object_or_404(Post, id=id)
    pd.delete()
    return redirect('home')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)