from django.urls import path
from . import views


app_name = 'csf'
urlpatterns = [
    path('create_comment/<slug:slug>/', views.CommentView.as_view(), name='create_comment'),
    path('add_score/', views.add_score, name='add_score'),
    path('add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('user_favorite/', views.UserFavorite.as_view(), name='user_favorite'),

    path('delete_favorite/', views.delete_favorite, name='delete_favorite'),
    path('show_wishlist/', views.show_wishlist, name='show_wishlist'),
    
    
]



