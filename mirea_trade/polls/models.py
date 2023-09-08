from django.db import models
from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.models import User



CHOICES = [
    ('Электротехника', 'Электротехника'),
    ('Информатика', 'Информатика'),
    ('Математическая статистика', 'Математическая статистика'),
    ('Системное программное обеспечение', 'Системное программное обеспечение'),
    ('Схемотехника', 'Схемотехника'),
    ('Физика', 'Физика'),
    ('Линейная алгебра', 'Линейная алгебра'),
    ('Математический анализ', 'Математический анализ'),
    ('Технология передачи данных', 'Технология передачи данных'),
    ('Вычислительная математика', 'Вычислительная математика'),
    ('Базы данных', 'Базы данных'),
    
]



class Skill(models.Model):

    name = models.CharField(max_length=100)


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username =  models.CharField(max_length=20)
    # email = models.CharField(max_length=254)
    # password = models.CharField(max_length=20)
    about = models.TextField(null = True, blank=True)
    
    skills = models.ManyToManyField(Skill, related_name='providers')

    rating = models.FloatField(null = True, blank = True, default=0)

    status = models.CharField(max_length=20 ,default='regular')

    created =  models.DateTimeField(auto_now_add=True)

    orders = models.IntegerField(default=0)

    contact_link = models.CharField(max_length=32)

    photo = models.ImageField(upload_to='media/images/', null=True, blank=True)

    rank = models.CharField(max_length=20, default='Новичок')


    def __str__(self):
        return self.user.username


    # is_active = models.BooleanField(default=False)




class Task(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_orders', null=True, blank=True)
    executor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='tasks')
    description = models.TextField()
    images = models.ImageField(null = True, blank=True,upload_to='images/', default='free-icon-user-149071.png')
    price = models.FloatField()
    created = models.DateField(auto_now_add=True)
    # contact_link = models.CharField(max_length=32, null=True, blank=True)
    kind = models.CharField(max_length=20, default='task')
    date = models.DateField()
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text[0:40]

# class Worksheet(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.ForeignKey(User, on_delete=models.CASCADE)


# class Order(models.Model):
#     title = models.CharField(max_length=500)
#     description = models.TextField()

