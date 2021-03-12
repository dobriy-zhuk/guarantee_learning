from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 9)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/blog.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/blog_post.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form': form})


@login_required
def edit_post(request, pk):

    module = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post_form = PostForm(request.POST, instance=module)

        if post_form.is_valid():
            post_form.save()

        return redirect("blog")
    else:
        post_form = PostForm(instance=module)

    return render(request, "blog/edit_post.html", {"post_form": post_form, })


@login_required
def remove_post(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
    except Post.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('blog')

    except Exception as e:
        return redirect('blog', {'err':e.message})

    return redirect('blog')