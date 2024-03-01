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
from django.conf import settings

from django.core.files.storage import FileSystemStorage

from django.http import JsonResponse

from .models import User
# from .models import Worksheet

def get_subjects():
    skill1, created1 = Skill.objects.get_or_create(name='Электротехника')
    skill2, created2 = Skill.objects.get_or_create(name='Информатика')
    skill3, created3 = Skill.objects.get_or_create(name='Математическая статистика')
    skill4, created3 = Skill.objects.get_or_create(name='Математический анализ')
    skill5, created3 = Skill.objects.get_or_create(name='Схемотехника')
    skill6, created3 = Skill.objects.get_or_create(name='Базы данных')
    skill7, created3 = Skill.objects.get_or_create(name='Линейная алгебра')
    list_of_subjects = []
    current_locals = list(locals().items())
    for skill_name, skill_obj in current_locals:
        if 'skill' in skill_name and isinstance(skill_obj, Skill):
            list_of_subjects.append(skill_obj)
    print(list_of_subjects)
    return list_of_subjects


def home(request):
    return render(request, 'polls/home.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


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
        print("POST Data:", request.POST)
        print("Files Data:", request.FILES)
        if form.is_valid():
            print("POST Data:", request.POST)
            print("Files Data:", request.FILES)
            print('FORMA OK ')
            print("requeest files:", request.FILES)
            if 'files' in request.FILES:
                pritn(request.FILES)
                print('asdas')
            task = form.save(commit=False)
            # task.files = request.FILES['files']
            print("TASK FILES", task.files)
            # print(f"Задача сохранена с файлом {task.files.url}")
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
        'skills': get_subjects(),
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

    if request.method == 'POST':

        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # if request.FILES['myphoto']:
            #     myphoto = request.FILES['myphoto']
            #     fs = FileSystemStorage()
            #     photoname = fs.save(myphoto.name, myphoto)
            #     uploaded_file_url = fs.url(photoname)
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
        'skills': get_subjects(),
    }

    return render(request, 'polls/form_worker.html', context)


def currentProfile(request):
    if request.user.is_authenticated is False:
        return redirect('signin')
    star_raiting = range(1, 6)
    user = UserProfile.objects.get(user=request.user)
    comments = Comment.objects.filter(executor=user)
    print(comments)
    selected_skills = user.skills.all()
    context = {
        'user': user,
        'selected_skills': selected_skills,
        'comments': comments,
        'star_raiting': star_raiting
    }
    return render(request, 'polls/worker_profile.html', context)


def otherProfile(request, username):

    # получаем пользователя, к которому зашли на страницу
    user = get_object_or_404(User, username=username)
    star_raiting = range(1, 6)
    # получаем список комментариев к этому пользователю
    comments = Comment.objects.filter(executor=user.userprofile).order_by('-created')
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
                comment = form.save(commit=False)
                # Создайте новый комментарий на основе данных из формы, связав его с профилем пользователя
                comment.author = request.user.userprofile
                comment.executor = user_profile
                request.user.userprofile.last_comment_time = current_time
                request.user.userprofile.save()
                print('TEXT:', comment.description)
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
        'star_raiting': star_raiting,
    }
    print('asdasdasdasdasdasd')
    return render(request, 'polls/other_worker_profile.html', context)


def settings(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

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
        'skills': get_subjects(),
    }

    return render(request, 'polls/settings.html', context)


def fullTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    selected_skills = task.skills.all()
    context = {
        'task': task,
        'selected_skills': selected_skills,
    }
    return render(request, 'polls/some_task.html', context)

def myTasks(request):

    print('asdasdasdasdasd')
    user_tasks = Task.objects.filter(executor=request.user.userprofile)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA', user_tasks)
    user_profiles = UserProfile.objects.all()
    context = {'user_tasks': user_tasks,
               'user_profiles': user_profiles,
               }

    return render(request, 'polls/task.html', context)

def myJobs(request):
    user_jobs = Task.objects.filter(author=request.user.userprofile)
    print('GOVNOO', user_jobs)
    context = {'user_jobs': user_jobs, }
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


def taskAccept(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user == task.executor.user:
        task.status = 'accept'
        task.save()
        return redirect('mytasks')
    context = {'task': task, }
    return render(request, 'polls/myjobs.html', context)

def taskCancel(request, pk):
    print("CANCEL")
    task = get_object_or_404(Task, pk=pk)
    print(task.status)
    if request.user == task.executor.user:
        task.status = 'cancel'
        task.save()
        return redirect('mytasks')
    context = {'task': task, }
    return render(request, 'polls/myjobs.html', context)


def rate(request, pk):
    task = Task.objects.get(pk=pk)
    executor_username = task.executor.pk
    userprofile = UserProfile.objects.get(user=executor_username)
    grade_of_regular = task.report  # оценка, которую поставил пользователь на конерктное задание
    number_of_reports_for_executor = userprofile.feedback  # количество отзывов, поставленных опреденному исполнителю
    rating_of_executor = userprofile.rating  # рейтинг исполнителя

    print("EXECUTOR:", userprofile)

    if request.method == 'POST':
        rating = request.POST.get('rating') # из запроса получаем рейтинг, который поставил пользователь
        print('Оценка', task.report)
        if task.report == None or task.report == 0:       # если нет оценки, значит пользователь еще не отправлял свой отзыв
            print('Первый отзыв на задание - увеличиваем количество отзывов на исполнителя')
            userprofile.feedback += 1
            print('Количество отзывов после операции', userprofile.feedback)
            userprofile.save()
            result = 0

        elif task.report != 0:  # если оценка уже стоит, но пользователь хочет ее изменить
            result = int(rating)-task.report  # определяем разницу между старой и новой оценкой
        else:
            result = 0  # если никакой оценки нет, то разность равна 0
        task.save() # сохраняем изменения
        if result < 0:  # если пользователь уменьшил оценку
            # то он старой оценки отнимаем 
            userprofile.rating = userprofile.rating-abs(result)/userprofile.feedback
        elif result > 0:
            userprofile.rating = userprofile.rating+abs(result)/userprofile.feedback
        elif result == 0 and task.report == 0:
            userprofile.rating = (float(userprofile.rating)+float(rating))/userprofile.feedback
        task.report = rating # меняем оценку пользователя для конкретного задания
        task.save() 
        userprofile.save()
        print("END!!!")
        print('рейтинг исполнителя', userprofile.rating)
        print('оценка, которую поставил пользователь на конерктное задание', grade_of_regular)
        print('Результат', result)
        print('Ответ из запроса', rating)
        print('Количество отзывов отправленных исполнителю', userprofile.feedback)
        return redirect('myjobs')
    return render(request, 'polls/myjobs.html')



    # executor = UserProfile.objects.get()
    # if request.user = task.executor.user:
