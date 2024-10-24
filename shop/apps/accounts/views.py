from django.shortcuts import render, redirect
from django.views import View
from .forms import (RegisterUserForm, VerifyRegisterForm,
                    LoginUserForm, ChangePasswordForm,
                    RememberPasswordForm, UpdateProfileForm)
import utils
from .models import CustomUser, Customer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from apps.orders.models import Order
from django.contrib.auth.decorators import login_required
from apps.payments.models import Payment

# Create your views here.

class RegisterUserView(View):
    
    def dispatch(self, request, *args, **kwargs):    # تابعی که قبل از همه ی تابع های دیگر اجرا می شود
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)  #اخر بار این دستور الزامی می باشد

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, 'accounts_app/register_user.html', {'form':form})
        
        
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            active_code = utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number = data['mobile_number'],
                active_code = active_code,
                password = data['password1'],
            )
            utils.send_sms(data['mobile_number'], f'کد فعال سازی حساب کاربری شما {active_code} می باشد')
            request.session['user_session'] = {
                'active_code': str(active_code),
                'mobile_number': str(data['mobile_number']),
                'remember_password': False,
            }
            messages.success(request, 'اطلاعات شما ثبت شد کد فعال سازی را وارد کنید', 'success')
            return redirect('accounts:verify')
        messages.error(request, 'خطا در انجام ثبت نام', 'danger')
        
#----------------------------------------------------------------
class VerifyRegisterCreateView(View):
    template_name = 'accounts_app/verify_register_code.html'
    
    def dispatch(self, request, *args, **kwargs):    # تابعی که قبل از همه ی تابع های دیگر اجرا می شود
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)  #اخر بار این دستور الزامی می باشد

    def get(self, request, *args, **kwargs):
        form = VerifyRegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code']:
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                if user_session['remember_password'] == False:
                    user.is_active = True
                    user.active_code = utils.create_random_code(5)
                    user.save()
                    messages.success(request, 'ثبت نام با موفقیت انجام شد', 'success')
                    return redirect('main:index')
                else:
                    return redirect('accounts:change_password')
            else:
                messages.error(request, 'کد فعال سازی وارد شده اشتباه می باشد', 'danger')
                return render(request, self.template_name , {'form': form})
        messages.error(request, 'اطلاعات درست نمی باشد', 'danger')
        return render(request, self.template_name, {'form': form})

#----------------------------------------------------------------
class LoginUserView(View):
    template_name = 'accounts_app/login.html'

    def dispatch(self, request, *args, **kwargs):    # تابعی که قبل از همه ی تابع های دیگر اجرا می شود
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)  #اخر بار این دستور الزامی می باشد

    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        return render(request, 'accounts_app/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user=authenticate(username=data['mobile_number'], password=data['password'])
            if user is not None:
                db_user = CustomUser.objects.get(mobile_number=data['mobile_number'])

                if db_user.is_admin == False:
                    messages.success(request, 'ورود با موفقیت انجام شد', 'success')
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
                else:
                        messages.error(request, 'کاربر ادمین نمی تواند از این صفحه وارد شود', 'warning')
                        return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, 'اطلاعات وارد شده صحیح نمی باشد', 'danger')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'اطلاعات وارد شده نامعتبر است ', 'danger')
            return render(request, self.template_name, {'form': form})

#----------------------------------------------------------------
class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):    # تابعی که قبل از همه ی تابع های دیگر اجرا می شود
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)  #اخر بار این دستور الزامی می باشد

    
    def get(self, request, *args, **kwargs):
        session_data = request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart'] = session_data
        return redirect('main:index')
    
#----------------------------------------------------------------
class ChangePasswordView(View):
    template_name = 'accounts_app/change_password.html'
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            user_session=request.session['user_session']
            user=CustomUser.objects.get(mobile_number=user_session.get('mobile_number'))
            user.set_password(data['password1'])
            user.active_code=utils.create_random_code(5)
            user.save()
            messages.success(request, 'رمز عبور شما با موفقعیت تغییر کرد', 'success')
            return redirect('accounts:login')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
#----------------------------------------------------------------
class RememberPasswordView(View):
    template_name = 'accounts_app/remember_password.html'
    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code=utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data['mobile_number'], f'کد تایید حساب کاربری شما {active_code} می باشد')
                request.session['user_session'] = {
                    'active_code': str(active_code),
                    'mobile_number': str(data['mobile_number']),
                    'remember_password':True,
                }
                messages.success(request, 'جهت تغییر رمز عبور خود کد تایید را ارسال کنید', 'success')
                return redirect('accounts:verify')
            except:
                messages.error(request, 'شماره موبایل وارد شده موجود نمی باشد', 'danger')
                return render(request, self.template_name, {'form': form})
                
#----------------------------------------------------------------
class UserPanelView(LoginRequiredMixin,View):
    template_name = 'accounts_app/userpanel.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'phone_number': customer.phone_number,
                'address': customer.address,
                'image': customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }
        return render(request, self.template_name, {'user_info': user_info})
    
#----------------------------------------------------------------
@login_required
def show_last_order(request, *args, **kwargs):
    orders = Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:6]
    return render(request, "accounts_app/partials/show_last_orders.html", {'orders': orders})

#----------------------------------------------------------------
class UpdateProfile(LoginRequiredMixin, View):
    template_name = 'accounts_app/partials/update_profile.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            customer = Customer.objects.get(user=request.user)
            initial_dict={
                "mobile_number": user.mobile_number,
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "phone_number": customer.phone_number,
                "address": customer.address,
            }
            
        except ObjectDoesNotExist:
            initial_dict={
                "mobile_number": usre.mobile_number,
                "name": usre.name,
                "family": usre.family,
                "email": usre.email,
            }
        form = UpdateProfileForm(initial=initial_dict)
        return render(request, self.template_name, {'form':form, 'image_url': customer.image_name})

    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user=request.user
            user.name=cd['name']
            user.family=cd['family']
            user.email=cd['email']
            user.save()
            try:
                customer = Customer.objects.get(user=request.user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                customer.image_name=cd['image']
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=request.user,
                    phone_number=request.cd['phone_number'],
                    address=cd['address'],
                    image=cd['image']
                )
            messages.success(request, 'ویرایش پروفایل با موفقیت انجام شد', 'success')
            return redirect('accounts:userpanel')
        else:
            messages.error(request, 'main_app/update_profile.html', {'form': form})

#----------------------------------------------------------------
@login_required
def show_user_payments(request):
    payments = Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
    return render(request, 'accounts_app/show_user_payments.html', {'payments':payments})