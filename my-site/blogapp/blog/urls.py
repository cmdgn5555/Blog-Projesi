from django.urls import path
from . import views



# http://127.0.0.1:8000/            => anasayfa
# http://127.0.0.1:8000/index       => anasayfa
# http://127.0.0.1:8000/blogs       => bloglar
# http://127.0.0.1:8000/blogs/2     => blog-detayı

urlpatterns = [
     path("", views.index, name="ana"),
     path("index", views.index),
     path("blogs", views.blogs, name="bloglar"),
     path("category/<slug:sluginfo>", views.blogs_by_category, name="kategoriye göre blog"),
     path("blogs/<slug:sluginfo>", views.blog_details, name="blog_detayi"),
     path("blogs/<slug:sluginfo>/comments", views.comment_detail, name="yorum_detayi"),
     path('comment/edit/<int:comment_id>/', views.edit_comment, name='yorum_düzenle'),
     path('comment/delete/<int:comment_id>/', views.delete_comment, name='yorum_sil'),
     path('comment/like/<int:comment_id>/', views.like_comment, name='begen'),
     path('comment/dislike/<int:comment_id>/', views.dislike_comment, name='begenme')
]


