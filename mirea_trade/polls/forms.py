from django import forms
from .models import UserProfile, Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# CHOICES = [
#     ('Электротехника', 'Электротехника'),
#     ('Информатика', 'Информатика'),
#     ('Математическая статистика', 'Математическая статистика'),
#     ('Системное программное обеспечение', 'Системное программное обеспечение'),
#     ('Схемотехника', 'Схемотехника'),
#     ('Физика', 'Физика'),
#     ('Линейная алгебра', 'Линейная алгебра'),
#     ('Математический анализ', 'Математический анализ'),
#     ('Технология передачи данных', 'Технология передачи данных'),
#     ('Вычислительная математика', 'Вычислительная математика'),
#     ('Базы данных', 'Базы данных'),

# ]


# ДОДЕЛАТЬ СОЗДАНИЕ ЗАДАНИЕ + ВЫВОД ЗАДАНИЙ!!!!!!!!!!!!!!!!!!!!!
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about', 'photo', 'contact_link', 'skills']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'images',
                  'price',
                  #   'contact_link',
                  'skills', 'date']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['author', 'executor', 'title', 'description',
                  'images', 'price', 'date',
                  #   'contact_link'
                  ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['contact_link']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(
    max_length=30,
    required=True,
    widget=forms.TextInput(attrs={
                           'class': 'custom-input',
                           'autocomplete': 'off',
                           'placeholder': 'Имя пользователя',
                           }),
    error_messages={
        'unique': 'Такой username уже занят.',
    }
)

    email = forms.EmailField(
    max_length=30,
    required=True,
    widget=forms.TextInput(attrs={
                           'class': 'custom-input',
                           'autocomplete': 'off',
                           'placeholder': 'Почта',
                           }),
    error_messages={
        'unique': 'Такой почта уже занята.',
    }
)

    password1 = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Повторите пароль'})
    )
