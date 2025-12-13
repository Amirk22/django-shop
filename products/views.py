from django.shortcuts import render , redirect
from django.views.generic import ListView , DetailView
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView,ListCreateAPIView

from .forms import CommentForm ,CommentReplyForm
from .models import Product, ProductSubCategory, ProductCategory, Brand, ProductGallery, ProductVisit ,Comment ,CommentReply
from django.db.models import F, Q
from django.utils import timezone
from cart.models import Cart

from .serializers import ProductSerializer ,BrandSerializer ,SubCategorySerializer ,GallerySerializer,CategorySerializer,VisitSerializer,CommentSerializer,CommentReplySerializer

# Create your views here.
#...............................
#region ProductListView
class ProductList(ListView):
    template_name = 'products/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 4
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = get_object_or_404(ProductSubCategory, slug=self.kwargs['subcategory_slug'])
        category = get_object_or_404(ProductCategory, slug=self.kwargs['category_slug'])
        context['subcategory'] = subcategory
        context['category'] = category
        context['brands'] = Brand.objects.filter( products__isnull=False).distinct()
        return context

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        subcategory_slug = self.kwargs['subcategory_slug']

        return Product.objects.filter(
            category__slug=subcategory_slug,
            category__parent__slug=category_slug,
            is_active=True
        )
#endregion
#region ProductListBrandView
class ProductListBrand(ListView):
    template_name = 'products/product_list_brand.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        brand = get_object_or_404(Brand,slug=self.kwargs['brand_slug'])
        products = Product.objects.filter(
            brand = brand ,
            is_active=True
        )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = get_object_or_404(Brand,slug = self.kwargs['brand_slug'])
        return context
#endregion
#region ProductDetailView
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class ProductDetail(DetailView):
    template_name = 'products/product_detail.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'pk'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = ProductGallery.objects.filter(product_id=self.object.id)
        context['products'] = Product.objects.filter(is_active=True,category=self.object.category).exclude(id=self.object.id)
        comment_count = Comment.objects.filter(product = self.object).count()
        reply_count = CommentReply.objects.filter(product = self.object).count()
        total_count = comment_count + reply_count
        context['total_comments'] = total_count
        context['comment_form'] = CommentForm()
        context['commentreply_form'] = CommentReplyForm()
        context['comments'] = Comment.objects.filter(product_id=self.object.id).order_by('-id')
        context['commentreplies'] = CommentReply.objects.filter(product_id=self.object.id).order_by('id')
        cart_item = None
        if self.request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=self.request.user, product=self.object).first()
        context['cart_item'] = cart_item
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(product_id=self.object.id,ip__iexact=user_ip).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip,user_id=user_id, product_id=self.object.id)
            new_visit.save()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = self.object
                comment.save()
                return redirect(request.path)
        elif 'reply_submit' in request.POST:
            form = CommentReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.product = self.object
                reply.comment_id = request.POST.get('comment_id')
                reply.save()
                return redirect(request.path)
        return self.get(request, *args, **kwargs)
#endregion
#region ProductListDiscountView
class ProductListDiscount(ListView):
    template_name = 'products/product_list_discount.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        now = timezone.now()
        return Product.objects.filter(
            discount_price__lt=F('price')
        ).filter(
            Q(discount_start__isnull=True) | Q(discount_start__lte=now),
            Q(discount_end__isnull=True) | Q(discount_end__gte=now),
        ).order_by('-price')
#endregion
#...............................
#region ProductListAPIView
class ProductListAPI(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
#endregion
#region ProductListFilterWithCategoryAPIView
class ProductListFilterWithCategoryAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        subcategory_slug = self.kwargs['subcategory_slug']
        return Product.objects.filter(
            category__slug=subcategory_slug,
            category__parent__slug=category_slug,
            is_active=True
        )
#endregion
#region ProductListFilterWithBrandAPIView
class ProductFilterWithBrandAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        brand = get_object_or_404(Brand, slug=self.kwargs['brand_slug'])
        return Product.objects.filter(
            brand=brand,
            is_active=True
        )

#endregion
#region ProductBrandListAPIView
class ProductBrandAPIView(ListAPIView):
    serializer_class = BrandSerializer
    def get_queryset(self):
        return Brand.objects.all()

#endregion
#region ProductCategoryAPIView
class ProductCategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = ProductCategory.objects.all()
#endregion
#region ProductSubCategoryAPIView
class ProductSubCategoryAPIView(ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = ProductSubCategory.objects.all()
#endregion
#region ProductGalleryAPIView
class ProductGalleryAPI(ListAPIView):
    serializer_class = GallerySerializer
    queryset = ProductGallery.objects.all()
#endregion
#region ProductVisitAPIView
class ProductVisitAPIView(ListAPIView):
    serializer_class = VisitSerializer
    queryset = ProductVisit.objects.all()
#endregion
#region CommentVisitAPIView
class CommentVisitAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
#endregion
#region CommentReplyVisitAPIView
class CommentReplyVisitAPIView(ListCreateAPIView):
    serializer_class = CommentReplySerializer
    queryset = CommentReply.objects.all()
#endregion
#region ProductListDiscountAPIView
class ProductListDiscountAPIView(ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        now = timezone.now()
        return Product.objects.filter(
            discount_price__lt=F('price')
        ).filter(
            Q(discount_start__isnull=True) | Q(discount_start__lte=now),
            Q(discount_end__isnull=True) | Q(discount_end__gte=now),
        ).order_by('-price')
#endregion


