from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from warperprofile.models import Profile
from post.models import Post, Like, Repost
from django.shortcuts import render, get_object_or_404
from warperprofile.forms import ProfileForm
from post.forms import PostForm


def home(request):
    return render(request, "core/home.html", {})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("home_page")
        messages.info(request, "Invalid Username or Password")
        return redirect("signin_page")
    return render(request, "core/signin.html", {})

def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmpassword = request.POST["password_confirm"]

        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("signup_page")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect("signup_page")
            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,  password=confirmpassword)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect("home_page")
        else:
            messages.info(request, "Password doesn't Match")
            return redirect("signup_page")
    else:
        return render(request, "core/signup.html", {})

@login_required(login_url="login_page")
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    # posts = Post.objects.filter(author=user)  

    context = {
        'user': user,
        'profile': profile,
        # 'posts': posts
    }

    return render(request, 'core/profile.html', context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)


    return render(request, 'core/edit_profile.html', {'form': form, "profile" : profile})


@login_required(login_url="login_page")
def feeds(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'core/feeds.html', {'posts': posts, 'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('feeds_page')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect('feeds_page')

@login_required
def repost(request, post_id):
    original_post = get_object_or_404(Post, id=post_id)
    Repost.objects.create(user=request.user, original_post=original_post)
    return redirect('feeds_page')
