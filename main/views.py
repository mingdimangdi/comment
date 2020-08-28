from django.views import generic
from .models import Post,Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages 
from django.shortcuts import get_object_or_404,render
from django.views.decorators.http import require_POST, require_http_methods

class IndexView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'post'
    def get_queryset(self): #ListView에서 사용-표시 하려는 개체 목록을 결정한다. 
        return Post.objects.all()

class DetailView(generic.DetailView):
    model = Post #queryset = Post.objects.all()이랑 같은 기능
    template_name = 'detail.html'
    context_object_name='ppost'

    def get_context_data(self, **kwargs):
        context_data = super(DetailView, self).get_context_data(**kwargs) 
        context_data['form']=CommentForm()
        context_data['comments']=self.object.comment_set.all()
        return context_data

def comment_create(request, post_id):
    if not request.user.is_anonymous: 
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.author = request.user
            comment.post_id = post_id
            comment.save()
       
        else:
            messages.info(request, "올바르지 않은 댓글입니다.")
    else:
        messages.info(request, "로그인 해주세요!")
    return HttpResponseRedirect(reverse('detail',args=(post_id,)))


def comment_update(request, post_id, comment_id):

    comment = Comment.objects.get(pk=comment_id)
    if comment.author == request.user:
        comment_form = CommentForm(instance = comment)
        if request.method == "POST":
            update_form = CommentForm(request.POST, instance = comment)
            if update_form.is_valid():
                update_form.save()
                return HttpResponseRedirect(reverse('detail', args=(post_id,)))
        return render(request,'update.html',{'comment_form':comment_form})
    else:
        messages.info(request, "댓글 수정안됨 ")
        return HttpResponseRedirect(reverse('detail', args=(post_id,)))




def comment_delete(request, post_id, comment_id):
       comment = get_object_or_404(Comment, pk=comment_id)
       if request.user == comment.author:
           comment.delete()
           return HttpResponseRedirect(reverse('detail',args=(post_id,)))
           