from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from .models import UserProfile, Skill, Task, Comment
from .forms import UserProfileForm, TaskForm, OrderForm, ContactForm, SignUpForm, CommentForm
from django.urls import reverse
from django.utils import timezone

from django.http import JsonResponse

from .models import User
# from .models import Worksheet
# Create your views here.


def signinPage(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Пользователь не зарегистрирован.")
            # Перенаправляем обратно на страницу входа
            return redirect('signin')

        if user:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Неверный пароль.")
        else:
            messages.error(request, "Пользователь не зарегистрирован.")

    context = {}
    return render(request, 'polls/signin.html', context)


def signupPage(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password1']
            )
            login(request, user)  # Авторизация пользователя после создания
            return redirect('home')
        else:
            # Если форма не прошла валидацию, выведите сообщение об ошибке
            messages.error(
                request, 'Пожалуйста, исправьте ошибки в форме ниже.')
    else:
        form = SignUpForm()  # Создание пустой формы, когда запрос не POST

    context = {'form': form}
    return render(request, 'polls/signup.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def myTasks(request):

    print('asdasdasdasdasd')
    user_tasks = Task.objects.filter(executor=request.user.userprofile)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA', user_tasks)
    user_profiles = UserProfile.objects.all()
    context = {'user_tasks': user_tasks,
               'user_profiles': user_profiles,
               }

    return render(request, 'polls/task.html', context)


def home(request):
    return render(request, 'polls/home.html')


@login_required
def for_worker(request, pk):

    if request.user.is_authenticated is False:
        return redirect('signin')

    user_profile = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        form = OrderForm(request.POST, request.FILES)

        if form.is_valid():

            task = form.save(commit=False)
            author_profile = request.user.userprofile
            task.author = author_profile
            task.kind = 'order'

            if user_profile:

                task.executor = user_profile.userprofile
                task.save()
                response_data = {
                    'success': 'AAA',
                }
                return JsonResponse(response_data)
        else:

            print(form.errors)

    else:

        form = OrderForm()

    context = {'user_profile': user_profile,
               'form': form,
               }

    return render(request, 'polls/for_worker.html', context)


# def form_worker(request):

#     return render(request, 'polls/form_worker.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def tasks(request):
    all_tasks = Task.objects.filter(kind='task')
    tasks = all_tasks

    if is_ajax(request=request):
        selected_subjects = request.GET.getlist('selected_subjects[]')
        if selected_subjects:
            tasks = all_tasks.filter(skills__name__in=selected_subjects)

        # Формируем список заданий с информацией о предметах
        task_data = [{
            'title': task.title,
            'description': task.description,
            'price': task.price,
            'date': task.date,
            'pk': task.pk,
            # Список предметов задания
            'skills': [skill.name for skill in task.skills.all()]
        } for task in tasks]

        return JsonResponse({'tasks': task_data})

    context = {'tasks': tasks}
    return render(request, 'polls/tasks_list.html', context)


def freeTask(request, task_id=None):

    if request.user.is_authenticated is False:
        return redirect('signin')
    skill1, created1 = Skill.objects.get_or_create(name='Электротехника')
    skill2, created2 = Skill.objects.get_or_create(name='Информатика')
    skill3, created3 = Skill.objects.get_or_create(
        name='Математическая статистика')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if not user.is_authenticated:
        return redirect('signin')

    task = None

    if task_id:
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            pass

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            print('FORMA OK ')
            task = form.save(commit=False)

            task.author = request.user.userprofile
            contact_link = request.POST.get('contact_link')
            user_profile.contact_link = contact_link
            user_profile.save()
            task.save()
            form.save_m2m()
            response_data = {
                'success': 'AAA',
            }
            return JsonResponse(response_data)

        else:
            print('FORM NE OK OWIBKA !!!!!!!!!!!!!!')
            print(form.errors)

    else:
        form = TaskForm()

    context = {
        'form': form,
        'skills': [skill1, skill2, skill3],
    }

    return render(request, 'polls/make_free_task.html', context)


def success(request):
    return render(request, 'polls/success_template.html')


def search(request):

    user_profiles = UserProfile.objects.all()
    profiles = user_profiles

    if is_ajax(request=request):
        selected_subjects = request.GET.getlist('selected_subjects[]')
        print(selected_subjects)
        if selected_subjects:
            profiles = user_profiles.filter(skills__name__in=selected_subjects)

        profile_data = [{
            'username': profile.user.username,
            'about': profile.about,
            'pk': profile.pk,
            # Список предметов задания
            'skills': [skill.name for skill in profile.skills.all()]
        } for profile in profiles]

        return JsonResponse({'profiles': profile_data})
    # worker = UserProfile.objects.filter()

    context = {'profiles': profiles,

               }
    return render(request, 'polls/search_worker.html', context)


def profileComments(request):

    comments = Comment.objects.filter(executor=request.user)

    print('COMMENTS:', comments)

    context = {
        'comments': comments,
    }

    return render(request, 'polls/worker_profile.html', context)


def comment(request, username):

    print('COMMENTS!!!!!!!')
# Получите объект UserProfile по его ID
    user_profile = UserProfile.objects.get(username=username)

    if request.method == 'POST':
        print('POST!')
        form = CommentForm(request.POST)
        if form.is_valid():
            print('FORMA OK!')
            # Создайте новый комментарий на основе данных из формы, связав его с профилем пользователя
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            # Замените 'user_profile_detail' на имя вашего представления пользователя
            return redirect('otherprofile')
        else:
            print('FORMA NE OK!')
    else:
        print("NE POST!!!!")
        form = CommentForm()

    return render(request, 'polls/worker_profile.html', {'form': form, 'user_profile': user_profile})


def editProfile(request):  # заполнение анкеты -> становление исполнителем
    if request.user.is_authenticated is False:
        return redirect('signin')

    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)  # Создание экземпляра класса UserProfile,
    #  определенного в models.py. #request.user - это авторизированный пользователь. objects - менеджеров объектов,
    #  который предоставляет различные методы, в данном случае - get, которые обращается в базе данных
    #  в UserProfile полe user, равное текущему авториз. пользователю request.user
    # Получение или создание существующих объектов Skill
    skill1, created1 = Skill.objects.get_or_create(name='Электротехника')
    skill2, created2 = Skill.objects.get_or_create(name='Информатика')
    skill3, created3 = Skill.objects.get_or_create(
        name='Математическая статистика')

    if request.method == 'POST':

        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            selected_skills = form.cleaned_data.get('skills')
            user_profile.skills.set(selected_skills)
            user_profile.status = 'worker'
            user_profile.save()
            response_data = {
                'success': 'AAA',
            }
            return JsonResponse(response_data)
        else:
            print(form.errors)

    else:

        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
        'skills': [skill1, skill2, skill3],
    }

    return render(request, 'polls/form_worker.html', context)


def currentProfile(request):
    if request.user.is_authenticated is False:
        return redirect('signin')
    user = UserProfile.objects.get(user=request.user)
    comments = Comment.objects.filter(executor=user)
    print(comments)
    selected_skills = user.skills.all()
    context = {
        'user': user,
        'selected_skills': selected_skills,
        'comments': comments,
    }
    return render(request, 'polls/worker_profile.html', context)


def otherProfile(request, username):

    # получаем пользователя, к которому зашли на страницу
    user = get_object_or_404(User, username=username)
    # получаем список комментариев к этому пользователю
    comments = Comment.objects.filter(executor=user.userprofile)
    # user_profile - хозяин страницы, как экземпляр UserProfile
    user_profile = user.userprofile
    selected_skills = user_profile.skills.all()  # получаем все skills этого хозяина
    comment = None
    flug = None
    form = None

    if request.method == 'POST':

        last_comment_time = request.user.userprofile.last_comment_time
        current_time = timezone.now()
        time_difference = current_time - last_comment_time
        form = CommentForm(request.POST, request.FILES, instance=comment)

        if time_difference.total_seconds() >= 60:
            flug = True
            if form.is_valid():
                print(form.errors)

                # print('FORMA OK!')
                comment = form.save(commit=False)
                # Создайте новый комментарий на основе данных из формы, связав его с профилем пользователя

                comment.author = request.user.userprofile
                comment.executor = user_profile
                request.user.userprofile.last_comment_time = current_time
                request.user.userprofile.save()
                print('TEXT:', comment.description)
                # form.text =
                comment.save()

            else:
                print('FORMA NE OK!')
                print(form.errors)

        elif time_difference.total_seconds() < 60:
            flug = False
        else:
            print("NE POST!!!!")
            form = CommentForm()
    context = {
        'user_profile': user_profile,
        'selected_skills': selected_skills,
        'user': user,
        'form': form,
        'comment': comment,
        'comments': comments,
        'flug': flug,
    }
    print('asdasdasdasdasdasd')
    return render(request, 'polls/other_worker_profile.html', context)


def settings(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)
    skill1, created1 = Skill.objects.get_or_create(name='Электротехника')
    skill2, created2 = Skill.objects.get_or_create(name='Информатика')
    skill3, created3 = Skill.objects.get_or_create(
        name='Математическая статистика')

    if request.method == "POST":
        if user_profile.status == 'worker':
            form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                selected_skills = form.cleaned_data.get('skills')
                user_profile.skills.set(selected_skills)
                user_profile.status = 'worker'
                # user_profile.photo = request.FILES['photo']
                form.save()
                user_profile.save()
                return redirect('home')
        elif user_profile.status == 'regular':
            form = ContactForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                user_profile.save()
                return redirect('home')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
        'skills': [
            Skill.objects.get_or_create(name='Электротехника'),
            skill2,
            skill3
        ],
    }

    return render(request, 'polls/settings.html', context)


# def createComment(request):

    # comment =


def fullTask(request, pk):

    task = get_object_or_404(Task, pk=pk)

    context = {'task': task}

    return render(request, 'polls/some_task.html', context)


def myJobs(request):
    
    user_jobs = Task.objects.filter(author=request.user.userprofile)

    context = {'user_jobs': user_jobs,
               }

    return render(request, 'polls/myjobs.html', context)


def myOrder(request, pk):

    order = get_object_or_404(Task, pk=pk)

    context = {'order': order}

    return render(request, 'polls/some_order.html', context)


def deleteTask(request, pk):

    task = get_object_or_404(Task, pk=pk)
    if request.user == task.author.user:
        # Если текущий пользователь - владелец, удаляем задание
        task.delete()
        return redirect('myjobs')
    context = {'task': task, }
    return render(request, 'polls/myjobs.html', context)
