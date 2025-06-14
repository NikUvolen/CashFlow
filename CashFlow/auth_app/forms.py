from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if (not user) or (not user.check_password(password)):
            raise forms.ValidationError(
                f'Пользователь {username} не найден или неправильно введен пароль.'
            )
        return self.cleaned_data
    

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято. Попробуйте снова')
        return username
    
    def clean(self):
        if 'confirm_password' not in self.cleaned_data:
            raise forms.ValidationError('Введите подтверждение пароля')
        
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают.')
        return self.cleaned_data
