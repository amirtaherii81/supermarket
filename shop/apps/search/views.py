from django.shortcuts import render
from django.views import View
from apps.products.models import Product
from django.db.models import Q
# Create your views here.

class SearchResultsView(View): 
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(discription__icontains=query)
        )
        print(products)
        context = {
            "products": products,
        }
        return render(request, 'search_app/search_results.html', context)
    