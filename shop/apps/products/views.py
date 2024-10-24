from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductGroup, FeatureValue, Brand
from django.db.models import Q, Count, Min, Max
from django.views import View
from django.http import JsonResponse
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compares import CompareProduct
from django.http import HttpResponse
# Create your views here.

def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))

#----------------------------------------------------------------
#  محصولات
def get_cheapest_products(request,*args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-price')
    product_groups = get_root_group()
    context = {
        'products': products,
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/cheapest_products.html', context)


#----------------------------------------------------------------
#  جدید ترین محصولات
def get_last_products(request,*args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:2]
    product_groups = get_root_group()
    context = {
        'products': products,
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partials/last_products.html', context)


#----------------------------------------------------------------
# گروه های محبوب
def get_popular_product_groups(request,*args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active=True))\
                                        .annotate(count=Count('products_of_groups'))\
                                        .order_by('-count')[:6]
    context = {
        'product_groups':product_groups,
    }
    return render(request, 'products_app/partials/popular_product_groups.html', context)
    
#----------------------------------------------------------------
#  جزییات محصول
class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, 'products_app/product_detail.html', {'product': product})


#----------------------------------------------------------------
# محصولات مرتبط
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])
    related_products = []
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request, 'products_app/partials/related_products.html', {'related_products':related_products})


#----------------------------------------------------------------
# لیست کلیه گروه های محصولات
class ProductGroupsView(View):
    def get(self, request, *args, **kwargs):
        product_groups = ProductGroup.objects.filter(Q(is_active=True))\
                                        .annotate(count=Count('products_of_groups'))\
                                        .order_by('-count')
        return render(request, 'products_app/product_groups.html', {'product_groups':product_groups})
            
#----------------------------------------------------------------
# لیست گروه محصولات برای فیلتر
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count= Count('products_of_groups'))\
                                        .filter(Q(is_active=True) & ~Q(count=0))\
                                        .order_by('-count')
    return render(request, 'products_app/partials/product_groups.html', {'product_groups':product_groups})
     

#----------------------------------------------------------------
#tow dropduwn in adminpanel
def get_filter_value_for_feature(request):
    if request.method == "GET":
        feature_id = request.GET["feature_id"]
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)

#----------------------------------------------------------------
# لیست برندها برای فیلتر
def get_brands(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id = product_group.products_of_groups.filter(is_active=True).values('brand_id')
    brands = Brand.objects.filter(pk__in=brand_list_id)\
                            .annotate(count=Count('product_of_brands'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    
    return render(request, 'products_app/partials/brands.html', {'brands':brands})

#----------------------------------------------------------------
# لیست های دیگر فیلتر ها بر حسب مقادیر ویژگیهای کالاهای درون گروه
def get_feature_for_filter(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list = product_group.features_of_groups.all()

    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_values.all()

    return render(request, 'products_app/partials/features_filter.html', {'feature_dict':feature_dict})

#----------------------------------------------------------------
# لیست محصولات هر گروه محصولات
class ProductByGroupView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup, slug=slug)
        products = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))

        res_aggre = products.aggregate(min=Min('price'), max=Max('price'))

        # price filter
        filter=ProductFilter(request.GET, queryset=products)
        products=filter.qs

        # brand filter
        brands_filter = request.GET.getlist('brand')
        if brands_filter:
            products = products.filter(brand__id__in=brands_filter)

        # feature filter
        features_filter = request.GET.getlist('feature')
        if features_filter:
            products = products.filter(product_feature__filter_value__id__in=features_filter).distinct()    # distinct باعث می شود تکراری ها حذف شوند

        # sort type
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = '0'
        if sort_type == '1':
            products = products.order_by('price')
        elif sort_type == '2':
            products = products.order_by('-price')
        
        # pager
        group_slug=slug
        product_per_page=6                                      # تعداد کالاها در هر صفحه
        paginator = Paginator(products, product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
        
        
        # display type
        display_type = request.GET.get('display', 'default_value')  # در صورت عدم وجود مقدار پیشفرض قرار داده می شود
        try:
            display_type = int(display_type)
        except ValueError:
            display_type = product_per_page    # مقدار پیش فرض
        # صفحه بندی جدید
        paginator = Paginator(products, display_type)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        
        
        # لیست اعداد برای ساخت منو باز شونده برای تعیین تعداد کالای هر صفحه توسط کاربر 
        show_count_per_page=[]
        i=product_per_page
        while i<product_count:
            show_count_per_page.append(i)
            i+=2
        show_count_per_page.append(i)
        
             
             
        context = {
            'products':products,
            'current_group':current_group,
            'res_aggre':res_aggre,
            'group_slug':group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'filter': filter,
            'sort_type':sort_type,
            'show_count_product':show_count_per_page,
            'current_display': display_type,
        }       
        return render(request, 'products_app/products.html', context)
    
#----------------------------------------------------------------
# main compare page: show products added to the comparison list
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        return render(request, 'products_app/compare_list.html', {'compare_list': compare_list})

#----------------------------------------------------------------
# show table of Comparison list products 
def compare_table(request):
    compare_list = CompareProduct(request)

    products=[]
    for productId in compare_list.compare_product:
        product = Product.objects.get(id=productId)
        products.append(product)

    features=[]
    for product in products:
        for item in product.product_feature.all():
            if item.feature not in features:
                features.append(item.feature)
    context = {
        'products': products,
        'features': features
    }
    return render(request, 'products_app/partials/compare_table.html', context)

# ----------------------------------------------------------------
# محاسبه تعداد کالاهای موجود در لیست مقایسه
def status_of_compare_list(request):
    compare_list = CompareProduct(request)
    return HttpResponse(compare_list.count)

# ----------------------------------------------------------------
# اضافه کردن کالا به لیست مقایسه
def add_to_compare_list(request):
    product_id = request.GET.get('productId')
    compare_list = CompareProduct(request)
    compare_list.add_to_compare_product(product_id)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')

#-----------------------------------------------------------------
# حذف کالا از لیست مقایسه ها
def delete_from_compare_list(request):
    product_id = request.GET.get('productId')
    compare_list = CompareProduct(request)
    compare_list.delete_from_compare_product(product_id)
    return redirect("products:compare_table")

#-----------------------------------------------------------------
# دسته بندی کالاها در نوبار
def category(request):
    group_parents = ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
    return render(request, 'partials/category.html', {'group_parents':group_parents})
    
#-----------------------------------------------------------------
# کالاهای دسته گروه های فرزند
def products_groups(request, slug):
    products = Product.objects.filter(Q(is_active=True) & Q(product_group__slug = slug))
    return render(request, 'products_app/products_group_parent.html', {'products': products})

#-----------------------------------------------------------------
# کالاهای دسته گروه های والد
def products_parent_group(request, slug):
    print(slug)
    products = Product.objects.filter(Q(is_active=True) & Q(product_group__group_parent__slug = slug))
    print(products)
    return render(request, 'products_app/products_group_parent.html', {'products': products})
