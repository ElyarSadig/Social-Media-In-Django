from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import validate_password, validate_username, validate_iranian_phone_number, convert_shamsi_to_georgian,\
    convert_georgian_to_shamsi, calculate_age, validate_picture
from .models import User
from django.contrib.auth.decorators import login_required
from base.models import Follower


def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "نام کاربری و یا رمز عبور اشتباه است.")

    return render(request, 'users/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if not(validate_password(password1)):
                messages.error(request, "رمز عبور باید حداقل شامل ۸ کاراکتر و دارای حداقل ۱ عدد و ۱ حرف بزرگ و کوچک باشد.")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "ایمیل قبلا وارد شده است.")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "نام کاربری قبلا وارد شده است.")
                return redirect("register")
            elif not(validate_username(username)):
                messages.error(request, 'نام کاربری معتبر نیست.')
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                login(request, user)
                return redirect("settings")
        else:
            messages.error(request, "رمز های عبور مطابقت ندارد.")
            return redirect("register")

    return render(request, 'users/register.html', {})


@login_required(login_url='login')
def settings(request):
    user = request.user
    shamsi_date = ""
    phone_number_error = ""

    if request.method == "POST":
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        phone_number = request.POST.get("phoneNumber")
        job = request.POST.get("job")
        address = request.POST.get("address")
        birth_date = request.POST.get("date-picker-shamsi-list")
        profile_picture = request.FILES.get("profile-image")

        if profile_picture:
            if validate_picture(profile_picture):
                user.profile_picture = profile_picture

            else:
                messages.error(request, "فایل ورودی معتبر نیست.")

        if phone_number != user.phoneNumber:
            if phone_number:
                if validate_iranian_phone_number(phone_number):
                    if User.objects.filter(phoneNumber=phone_number).exists():
                        phone_number_error = "شماره تلفن وارد شده قبلا ثبت شده است."
                    else:
                        user.phoneNumber = phone_number
                else:
                    phone_number_error = "شماره تلفن وارد شده معتبر نیست."

        if birth_date:
            user.birthDate = convert_shamsi_to_georgian(birth_date)

        user.job = job
        user.location = address
        user.name = name
        user.bio = bio

        user.save()

        return redirect('user-profile')

    if user.birthDate:
        shamsi_date = convert_georgian_to_shamsi(str(user.birthDate))

    return render(request, "users/user-settings.html",
                  {'user': user, "shamsi_date": shamsi_date, "error": phone_number_error})


@login_required(login_url='login')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        old_password = request.POST.get("old-password")
        new_password1 = request.POST.get("new-password1")
        new_password2 = request.POST.get("new-password2")

        user = authenticate(request, username=user.username, password=old_password)

        if user:

            if new_password1 != new_password2:
                messages.error(request, "پسورد های وارد شده تطابق ندارد")

            elif not validate_password(new_password1):
                messages.error(request, "رمز عبور باید حداقل شامل ۸ کاراکتر و دارای حداقل ۱ عدد و ۱ حرف بزرگ و کوچک باشد.")

            else:
                messages.success(request, "رمز عبور شما با موفقیت تغییر یافت. لطفا دوباره لاگین شوید.")
                user.set_password(new_password1)
                user.save()
                return redirect('login')

        else:
            messages.error(request, "رمز عبور فعلی صحیح نمی باشد.")

    return render(request, "users/reset_password.html", {})


@login_required(login_url='login')
def user_profile(request):
    user = request.user

    age = calculate_age(user.birthDate)

    posts = user.post_set.all()

    liked_post = []
    for post in posts:
        if len(post.like_set.all()):
            liked_post.append(len(post.like_set.all()))

    followers = user.followed.all()
    followings = user.following.all()

    context = {'user': user, 'age': age, 'posts': posts, 'followers': followers, 'num_liked_post': sum(liked_post),
               "followings": followings}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def profile_view(request, pk):
    user = User.objects.get(id=pk)

    age = calculate_age(user.birthDate)

    posts = user.post_set.all()

    liked_post = []
    for post in posts:
        if len(post.like_set.all()):
            liked_post.append(len(post.like_set.all()))

    followers = user.followed.all()
    follower_obj = Follower.objects.filter(user=request.user, followed=user)

    context = {'user': user, 'age': age, 'posts': posts, 'followers': followers, 'num_liked_post': sum(liked_post),
               'follower_obj': follower_obj}

    return render(request, "users/profile.html", context)
