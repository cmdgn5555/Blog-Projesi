from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from blog.models import Blog, Category
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment
from .forms import CommentForm
from django.http import JsonResponse




data = { 
    
    "blog_listesi": [
    
    {
        "id":1,
        "title": "komple web geliştirme",
        "image": "1.jpg",
        "is_active": True,
        "is_home": False,
        "description": "çok iyi bir kurs"
    },

    {
        "id":2,
        "title": "python kursu",
        "image": "2.jpg",
        "is_active": True,
        "is_home": True,
        "description": "orta seviye bir kurs"
    },

    {
        "id":3,
        "title": "django kursu",
        "image": "3.jpg",
        "is_active": False,
        "is_home": True,
        "description": "temel düzeyde bir kurs"
    }

]

}

# Create your views here.



def index(request):
    
    icerik = {
        "blogs": Blog.objects.filter(is_active=True, is_home=True),
        "time": datetime.now(),
        "posts" : Blog.objects.all(),
        "categories": Category.objects.all()
        
     }
    return render(request, "blog/index.html", context=icerik)






def blogs(request):
    
    icerik = {
        "blogs": Blog.objects.filter(is_active=True),
        "time":  datetime.now(),
        "posts" : Blog.objects.all(),
        "categories": Category.objects.all()
       }
    
    return render(request, "blog/blogs.html", context=icerik)






@login_required(login_url="/account/login")
def blog_details(request, sluginfo):
    
    #bloglarimiz = data["blog_listesi"]
    #selectedBlog = None

    #for blog in bloglarimiz:
    #    if blog["id"] == id:
    #        selectedBlog = blog

    #bloglarimiz = data["blog_listesi"]
    #selectedBlog = [blog for blog in bloglarimiz if blog["id"] == id][0]

    selectedBlog = get_object_or_404(Blog, slug=sluginfo)
    comments = Comment.objects.filter(blog=selectedBlog, parent=None).order_by('created_at')
    selectedBlog.view_count += 1
    selectedBlog.save()

    yorum_sayisi = selectedBlog.yorumlar.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = selectedBlog
            comment.author = request.user if request.user.is_authenticated else None
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
            comment.save()
            return redirect('blog_detayi', sluginfo=selectedBlog.slug)
    else:
        form = CommentForm()
    
    
    return render(request, "blog/blog-details.html", {
        "selected_blog": selectedBlog,
        "form": form,
        "comment_count": yorum_sayisi,
        "comments" : selectedBlog.yorumlar.all(),
        "comments": comments
    })






@login_required(login_url="/account/login")
def comment_detail(request, sluginfo):

    selected_comment = Blog.objects.get(slug=sluginfo)
    
    return render(request, "blog/comments.html", {
        "selected_comment": selected_comment         
    })






def blogs_by_category(request, sluginfo):
    
    icerik = {
        "blogs": Category.objects.get(slug=sluginfo).blog_set.filter(is_active=True),
        #"blogs": Blog.objects.filter(is_active=True, category__slug=sluginfo),
        "categories": Category.objects.all(),
        "selected_category": sluginfo
        }
    
    return render(request, "blog/blogs.html", context=icerik)






@login_required
def edit_comment(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect('blog_detayi', sluginfo=comment.blog.slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('blog_detayi', sluginfo=comment.blog.slug)
    
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {
        'form': form, 
        'comment': comment
    })






@login_required
def delete_comment(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user or request.user.is_superuser:
        comment.delete()
        return redirect('blog_detayi', sluginfo=comment.blog.slug)
    
    else:
        return redirect('blog_detayi', sluginfo=comment.blog.slug)






@login_required
def like_comment(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    
    else:
        comment.likes.add(request.user)
        
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
    
    return JsonResponse({
        'toplam_begenme_sayisi': comment.total_likes(),
        'toplam_begenmeme_sayisi': comment.total_dislikes()
    })






@login_required
def dislike_comment(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
    
    else:
        comment.dislikes.add(request.user)
        
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
    
    return JsonResponse({
        'toplam_begenme_sayisi': comment.total_likes(),
        'toplam_begenmeme_sayisi': comment.total_dislikes()
    })


























































    
    
   
    

   
 
  








