"""View logic for the forum app."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm
from .models import Post


class PostListView(ListView):
    """Display all forum posts ordered by newest first."""

    model = Post
    template_name = "forum/forum.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    """Display the detail page for a single forum post."""

    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create a new forum post."""

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        """Attach the current user as the post author before saving."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow post authors to edit their own forum posts."""

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        """Preserve the current user as the post author when updating."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Restrict updates to the original post author."""
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow post authors to delete their own forum posts."""

    model = Post
    success_url = "/discussion_forum/"

    def test_func(self):
        """Restrict deletes to the original post author."""
        return self.request.user == self.get_object().author


@login_required
def add_comment_to_post(request, pk):
    """Display and process the form used to add a comment to a post."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect("post-detail", pk=post.pk)
    else:
        form = CommentForm()

    context = {
        "form": form,
        "post": post,
    }
    return render(request, "forum/add_comment_to_post.html", context)


@login_required
def chat_room(request, room_name):
    """Render the real-time chat room page with recent message history."""
    from .models import ChatMessage

    messages = ChatMessage.objects.filter(room_name=room_name).order_by("timestamp")[:100]

    context = {
        "room_name": room_name,
        "chat_history": messages,
    }
    return render(request, "forum/chat.html", context)