from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from warperprofile.models import Profile
from post.models import Post
from django.shortcuts import render, get_object_or_404
from warperprofile.forms import ProfileForm
from post.forms import PostForm


def home(request):
    if request.user.is_authenticated:
        return redirect("feeds_page")    
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
    posts = Post.objects.filter(user=user)  
    current_user = request.user

    # Check if the current user follows the profile
    is_following = profile.followers.filter(id=current_user.id).exists()

    # Check if the profile owner follows the current user (for follow back logic)
    follow_back = current_user.profile.followers.filter(id=profile.user.id).exists()

    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        "is_following": is_following,
        "follow_back": follow_back,
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

@login_required(login_url="login_page")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Posted!!!.")
        return redirect('feeds_page')

@login_required(login_url="login_page")
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({'likes': post.like_count()})

@login_required(login_url="login_page")
def repost_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.reposts.all():
        post.reposts.remove(request.user)
    else:
        post.reposts.add(request.user)
    return JsonResponse({'reposts': post.repost_count()})

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile

    if request.user in target_profile.followers.all():
        target_profile.followers.remove(request.user)
        messages.success(request, f'You have unfollowed {target_user.username}.')
    else:
        target_profile.followers.add(request.user)
        messages.success(request, f'You are now following {target_user.username}.')

    # Get the URL of the page the user was on before the follow/unfollow action
    referrer_url = request.META.get('HTTP_REFERER', '/')

    return redirect(referrer_url)
    # return redirect(reverse('profile', kwargs={'username': username}))


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followers.all()
    context = {
        'user': user,
        'followers': followers,
        'list_type': 'followers'

    }
    return render(request, 'core/followers.html', context)

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following_profiles = user.following.all()  # Users that this user is following
    # Extract the User objects from the Profile objects
    following_users = [profile.user for profile in following_profiles]
    context = {
        'user': user,
        'followers': following_users,  # Passed 'following' as 'followers' to reuse the template
        'list_type': 'following'  # To differentiate between followers and following
    }
    return render(request, 'core/followers.html', context)

def search(request):
    query = request.GET.get("query", "query") if request.GET.get("query", "query") != None else ""

    if len(query) > 0:
        warpers = User.objects.filter(username__icontains=query)
        warps = Post.objects.filter(content__icontains=query)
        messages.success(request, "We found something....")
    else:
        warpers = []
        warps = []

    context = {
        'query': query,
        "warpers" : warpers,
        "warps" : warps,
    }

    return render(request, "core/search.html", context)