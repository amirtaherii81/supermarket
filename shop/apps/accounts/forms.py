from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

#----------------------------------------------------------------
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repassword", widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'email', 'name', 'family', 'gender']

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغایرت دارند')
        return pass2

    def save(self, commit=True):    # این تابع دوباره نویسی میشود به دلیل هش شدن پسورد
        user = super().save(commit=False)  # باعث می شود یوزر سیو نشود
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
#----------------------------------------------------------------
class UserChangeForm(forms.ModelForm):  # وقتی میخواهیم کاربری را تغییر دهیم
    password = ReadOnlyPasswordHashField(help_text="<a href='../password'>تغییر رمز عبور </a>")
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin']
        
#----------------------------------------------------------------
class RegisterUserForm(forms.ModelForm):    # ایجاد فرمی برای ثبت نام کاربرای در سایت
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید'}))
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور را وارد کنید'}))
    class Meta:
        model = CustomUser
        fields = ['mobile_number',]
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موبایل را وارد کنید'})
        }

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغایرت دارند')
        return pass2
#----------------------------------------------------------------

class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد دریافتی را وارد کنید'})
                                )

#----------------------------------------------------------------
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' موبایل را وارد کنید'})
                                )
    password = forms.CharField(label='رمز عبور',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' رمز عبور را وارد کنید'})
                                )

#----------------------------------------------------------------
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور',
                            error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' رمز عبور را وارد کنید'})
                            )
    password2 = forms.CharField(label='رمز عبور',
                        error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' تکرار رمز عبور را وارد کنید'})
                        )
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغایرت دارند')
        return pass2
    
#----------------------------------------------------------------
class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                    error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'شماره موبایل را وارد کنید'}),
                                    )


#----------------------------------------------------------------
class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(label='',
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly', 'placeholder':'شماره موبایل را وارد کنید'})
                )
    
    name = forms.CharField(label='',
                error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'نام را وارد کنید'}))

    family = forms.CharField(
                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'نام خانوادگی را وارد کنید'}))

    email = forms.CharField(
                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ایمیل را وارد کنید'}))

    phone_number = forms.CharField(
                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'شماره موبایل را وارد کنید'}))   

    address = forms.CharField(label='',
                            error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'آدرس را وارد کنید', 'rows': '3'})
                            )
    
    image = forms.ImageField(required=False)