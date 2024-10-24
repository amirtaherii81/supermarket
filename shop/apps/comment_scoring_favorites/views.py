from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CommentForm
from .models import Comment, Scoring, Favorite
from apps.products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

class CommentView(View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('productId')
        comment_id = request.GET.get('commentId')
        slug = kwargs.get('slug')
        initial_dict = {
            'product_id': product_id,
            'comment_id': comment_id,
        }
        form = CommentForm(initial=initial_dict)
        context = {
            'form': form,
            'slug': slug,
        }
        return render(request, 'csf_app/partials/create_comment.html', context)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            parent = None
            if cd['comment_id']:
                parent_id = cd['comment_id']
                parent = Comment.objects.get(id=parent_id)

            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent,
            )
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_details', product.slug)
        messages.error(request, 'خطا در ارسال نظر', 'danger')
        return redirect('products:product_details', product.slug)
    
#----------------------------------------------------------------
def add_score(request):
    productId = request.GET.get('productId')
    score = request.GET.get('score')
    # product = get_object_or_404(Product ,id=productId)
    product = Product.objects.get(id=productId)
    average_score = product.get_average_score()
    Scoring.objects.create(
        product = product,
        scoring_user = request.user,
        score = score
    )
    new_avg_score = product.get_average_score()
    return HttpResponse(new_avg_score)

#-----------------------------------------------------------------------
def add_to_favorite(request):
    product_id = request.GET.get('productId')
    product = Product.objects.get(id=product_id)
    flag = Favorite.objects.filter(
        Q(favorite_user_id=request.user.id) &
        Q(product_id=product_id)).exists()
    
    if(not flag):
        Favorite.objects.create(
            product=product,
            favorite_user=request.user
        )
        return HttpResponse('این کالا به لیست علاقه مندی های شما اضافه شد')
    return HttpResponse('این کالا قبلا در لیست علاقه مندی های شما قرار گرفته')

#==========================================================
class UserFavorite(View):
    def get(self, request, *args, **kwargs):
        # products_favorites = Favorite.objects.filter(Q(favorite_user=request.user.id))
        # list_favorites = []
        # for product in products_favorites:
        #     list_favorites.append(Product.objects.get(favorite_product=product))
            
        # products_favorites = Product.objects.filter(favorite_product__favorite_user_id=request.user.id)
        # user_favorite = Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request, 'csf_app/wishlist.html',)

#----------------------------------------------------------
def delete_favorite(request):
    product_id = request.GET.get('product_id')
    # print(product_id)
    Favorite.objects.filter(product__id=product_id).delete()
    return redirect('csf:show_wishlist')

#----------------------------------------------------------
def show_wishlist(request):
        user_favorite = Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request, 'csf_app/partials/show_wishlist.html', {'user_favorite': user_favorite})