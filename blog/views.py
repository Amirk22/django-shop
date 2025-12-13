from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Blog , BlogCategory
from .serializers import BlogSerializer, BlogCategorySerializer


# Create your views here.


def blog_list(request):
    blogs = Blog.objects.all()
    authors = blogs.values_list('author__username', flat=True).distinct()
    categories = BlogCategory.objects.all()

    author = request.GET.get('author')
    category = request.GET.get('category')
    sort = request.GET.get('sort')

    if author and author != 'all':
        blogs = blogs.filter(author__username=author)

    if category and category != 'all':
        blogs = blogs.filter(category__title=category)

    if sort == 'imdb_rate':
        pass
    elif sort == 'newest':
        blogs = blogs.order_by('-created_at')
    elif sort == 'oldest':
        blogs = blogs.order_by('created_at')

    return render(request,'blog/list_blog.html',{'blogs':blogs , 'authors':authors, 'categories':categories})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request,'blog/detail_blog.html',{'blog':blog})

#.....................................................API

class BlogListViewAPI(ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class BlogCategoryListAPIView(ListAPIView):
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()

