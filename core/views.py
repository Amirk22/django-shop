from django.db.models import Count
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from  products.models import ProductCategory , ProductSubCategory ,Product , Brand
from .models import Banner ,Slider ,ProductHomePage, ListFooter
from blog.models import Blog
from .serializers import BannerSerializer, SliderSerializer, ListFooterSerializer


# Create your views here.

def home(request):
    banner1 = Banner.objects.filter(is_active=True, position=Banner.SiteBannerPositions.home_page_1).first()
    banner2 = Banner.objects.filter(is_active=True, position=Banner.SiteBannerPositions.home_page_2).first()
    banner3 = Banner.objects.filter(is_active=True, position=Banner.SiteBannerPositions.home_page_3).first()
    sliders = Slider.objects.filter(is_active=True)
    blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:4]
    visit_products = Product.objects.filter(is_active=True).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]
    products = Product.objects.filter(is_active=True)
    product_sub_category = ProductSubCategory.objects.all()
    product_home_page1 = ProductHomePage.objects.filter(is_active=True, position=ProductHomePage.ProductHomePagePositions.product_category_home_page_1).first()
    product_home_page2 = ProductHomePage.objects.filter(is_active=True, position=ProductHomePage.ProductHomePagePositions.product_category_home_page_2).first()
    product_home1 = product_home_page1.category.products.all()[:12] if product_home_page1 else []
    product_home2 = product_home_page2.category.products.all()[:12] if product_home_page2 else []
    single_product = Product.objects.filter(is_active=True,single_product=True).first()
    brands = Brand.objects.all()
    return render(request, 'core/home.html', {
        'banner1': banner1,
        'banner2': banner2,
        'banner3': banner3,
        'sliders': sliders,
        'blogs': blogs,
        'visit_products': visit_products,
        'product_sub_category': product_sub_category,
        'products': products,
        'product_home1': product_home1,
        'product_home2': product_home2,
        'product_home_page1' : product_home_page1,
        'product_home_page2' : product_home_page2,
        'single_product': single_product,
        'brands': brands,
    })


def site_header_partial(request):
    categories= ProductCategory.objects.all()
    subcategories= ProductSubCategory.objects.all()
    return render(request,'site_header_partial.html',{'categories':categories,'subcategories':subcategories})

def site_footer_partial(request):
    list_footer = ListFooter.objects.all()
    return render(request,'site_footer_partial.html',{'list_footer':list_footer})

#.................................................. API

class BannerAPIView(ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)

class SliderAPIView(ListAPIView):
    serializer_class = SliderSerializer
    queryset = Slider.objects.filter(is_active=True)

class ListFooterAPIView(ListAPIView):
    serializer_class = ListFooterSerializer
    queryset = ListFooter.objects.all()