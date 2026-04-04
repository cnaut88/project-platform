from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Project, ProjectComment, Subscription, ProjectLike
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, ProfileUpdateForm
from .models import User

# Create your views here.

def project_list(request):
    projects = Project.objects.all().order_by("-created_a")
    return render(request, "projects/project_list.html", {"projects": projects})


def project_details(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return redirect("show_projects")
    comments = project.comments.all()
    
    return render(request, "projects/detail.html", {"project": project,"comments": comments})

@login_required
def feed(request):
    # отримуємо всіх авторів, на яких підписаний юзер
    subscriptions = Subscription.objects.filter(
        subscriber=request.user
    ).values_list("author", flat=True)

    # беремо їх проекти
    projects = Project.objects.filter(
        owner__in=subscriptions
    ).order_by("-created_a")

    return render(request, "projects/feed.html", {
        "projects": projects
    })
@login_required
def create_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        git_url = request.POST.get("git_url")
        image = request.FILES.get("image")
        file = request.FILES.get("file")
        if not title or not description:
            return HttpResponse("Заповніть всі поля")
        Project.objects.create(owner=request.user,title=title,description=description,status=status,git_url=git_url,image=image,file=file)
        return redirect("show_projects")
    return render(request, "projects/create_project.html")


@login_required
def add_comment(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return redirect("show_projects")
    if request.method == "POST":
        text = request.POST.get("text")
        comment_type = request.POST.get("type", "feedback")
        if text:
            ProjectComment.objects.create(project=project,author=request.user,text=text,type=comment_type)
    return redirect("project_details", project_id=project.id)


@login_required
def like_project(request, project_id):
    project = Project.objects.get(id=project_id)

    like, created = ProjectLike.objects.get_or_create(
        project=project,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect("project_details", project_id=project_id)

@login_required
def subscribe_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return redirect("show_projects")
    Subscription.objects.get_or_create(subscriber=request.user,author=project.owner)
    return redirect("project_details", project_id=project.id)


@login_required
def unsubscribe_project(request, project_id):
    project = Project.objects.get(pk=project_id)

    Subscription.objects.filter(
        subscriber=request.user,
        author=project.owner
    ).delete()

    return redirect("project_details", project_id=project_id)
@login_required
def subscribe_user(request, user_id):
    author = User.objects.get(id=user_id)

    if request.user != author:
        Subscription.objects.get_or_create(
            subscriber=request.user,
            author=author
        )

    return redirect("user_profile", user_id=user_id)

@login_required
def my_projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "projects/my_projects.html", {"projects": projects})


@login_required
def delete_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return redirect("show_projects")
    if project.owner != request.user:
        return redirect("project_details", project_id=project.id)
    project.delete()
    return redirect("show_projects")

@login_required
def edit_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse("Проєкт не знайдено")
    if project.owner != request.user:
        return redirect("project_details", project_id=project.id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        git_url = request.POST.get("git_url")
        
        if not title or not description:
            return HttpResponse("Заповніть всі поля")

        project.title = title
        project.description = description
        project.status = status
        project.git_url = git_url
        project.save()
        return redirect("project_details", project_id=project.id)
    return render(request, "projects/edit_project.html", {"project": project})

def auth_view(request):
    if request.method == "POST":

        
        if "login_submit" in request.POST:
            login_input = request.POST.get("login")
            password = request.POST.get("password")

            user = None

            
            user = authenticate(request, username=login_input, password=password)

            
            if not user:
                try:
                    user_obj = User.objects.get(email=login_input)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

            if user:
                login(request, user)
                return redirect("show_projects")

            return render(request, "projects/login.html", {
                "login_error": "Невірний логін або пароль",
                "register_form": RegisterForm()
            })

        
        if "register_submit" in request.POST:
            form = RegisterForm(request.POST, request.FILES)

            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("show_projects")

            return render(request, "projects/login.html", {
                "register_form": form
            })

    return render(request, "projects/login.html", {
        "register_form": RegisterForm()
    })
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    projects = request.user.projects.all()

    return render(request, "projects/profile.html", {
        "projects": projects
    })

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "projects/edit_profile.html", {"form": form})

def user_profile(request, user_id):
    user_obj = User.objects.get(id=user_id)
    projects = user_obj.projects.all()

    return render(request, "projects/user_profile.html", {
        "profile_user": user_obj,
        "projects": projects
    })
