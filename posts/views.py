from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from accounts.models import Account
from posts.forms import CommentForm
from posts.models import Post, Comment


class PostListView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return context
        user: Account = self.request.user
        subscriptions = user.subscriptions.all()
        posts = Post.objects.all()
        subscriptions_posts = posts.filter(author__in=subscriptions)
        context['posts'] = subscriptions_posts
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post_add_view.html'
    model = Post
    fields = ['image', 'description']

    def form_valid(self, form):
        self.object: Post = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account_detail', kwargs={'username': self.request.user.username})


class PostDetailView(DetailView):
    template_name = 'post_detail_view.html'
    model = Post
    context_object_name = 'post'


class PostLikeView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        if request.user not in post.user_likes.all():
            post.user_likes.add(request.user)
            user = Account.object.get(pk=request.user.pk)
            user.liked_posts.add(post)
            Post.objects.filter(id=post.id).update(likes_count=(post.likes_count + 1))
            return redirect('index')
        else:
            post.user_likes.remove(request.user)
            user = Account.object.get(pk=request.user.pk)
            user.liked_posts.remove(post)
            Post.objects.filter(id=post.id).update(likes_count=(post.likes_count - 1))
            return redirect('index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text')
        account = get_user_model()
        author = account.objects.get(pk=request.user.pk)
        post = Post.objects.get(pk=kwargs.get('pk'))
        comment = Comment.objects.create(
            author=author,
            post=post,
            text=text,
        )

        return redirect('post_detail', pk=kwargs.get('pk'))

        #
        # post = get_object_or_404(Post, pk=kwargs.get('pk'))
        # if request.user not in post.user_comments.all():
        #     post.user_comments.add(request.user)
        #     user = Account.object.get(pk=request.user.pk)
        #     user.user_comments.add(post)
        #     Post.objects.filter(id=post.id).update(comments_count=(post.comments_count + 1))
        #     return redirect('post_detail', kwargs={'pk': post})
