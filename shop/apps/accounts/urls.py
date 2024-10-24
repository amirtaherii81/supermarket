from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', VerifyRegisterCreateView.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('userpanel/', UserPanelView.as_view(), name='userpanel'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('remember_password/', RememberPasswordView.as_view(), name='remember_password'),
    
    path('userpanel/', UserPanelView.as_view(), name='userpanel'),
    path('show_last_order/', show_last_order, name='show_last_order'),
    path('update_profile/', UpdateProfile.as_view(), name='update_profile'),
    path('show_user_payments/', show_user_payments, name='show_user_payments'),
]
