from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import *
from django.contrib import messages
from voteguard import settings
from .models import *
from django.core.paginator import Paginator

"""
For each bug and feature I either solve or create, I'll drop a dad joke.

1. What do you call a cow with no legs???
    Ground Beef(solved user auth bug)

2. Why are educated so hot???
    Cause they have more degress(Fixed mailing list bugs)

3. Why did the programmer need new glasses?
    Becaue he couldn't C# *ba dum tsss (Fixed Looping Issue With Maps API)

4. Why was 6 afraid of 7?
    Because 7, 8, 9(Fixed styling issue with maps)

5. What do you call a cow with no legs?
    Ground BEEF!!!!!!
"""

# UNAUTHENTICATED VIEWS START


def index(request):
    posts = BlogPost.objects.filter(is_published=True)
    context = {
        'posts' : posts
    }
    return render(request, "index.html", context)


def login(request):
    user = request.user

    if user.is_authenticated:
        return redirect("dashboard")

    context = {
        'title' : 'Login',
    }
    if request.method == 'POST':
        username = request.POST['username'] #Requesting Username
        password = request.POST['password'] #Requesting Password
    
        user = auth.authenticate(username=username, password=password)

        if user is not None: #Cheking If User Exists in the database
            auth.login(request, user) # Logs in User
            return redirect('dashboard') # Redirects to home view
        else:
            messages.info(request, 'Invalid Username or Password') #Conditional Checking if credentials are correct
            return redirect('login')#Redirects to login if invalid

    else:
        return render(request, 'login.html', context)


def register(request):
    user = request.user

    if user.is_authenticated:
        return redirect("edit-profile")
    context = {
        'title' : 'Sign Up',
    }
    if request.method == 'POST':
        #Requesting POST data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #End of POST data request

        #Condition is executed if both passwords are the same
        if password == password2:
            if User.objects.filter(email=email).exists(): #Checking databse for existing data
                messages.info(request, "This email is already in use")#Returns Error Message
                return redirect(register)
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('register')
            #Else condition executed if the above conditions are not fulfilled    
            else:
                ctx = {
                    'user' : username
                }
                message = get_template('mail.html').render(ctx)
                msg = EmailMessage(
                    'Welcome to Paradoxx',
                    message,
                    'Paradoxx',
                    [email],
                )
                msg.content_subtype ="html"# Main content is now text/html
                msg.send()
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name )
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)#Logs in USER



            #Create user model and redirect to edit-profile
            return redirect('cont')#Rediects to specified page once condition is met
        else:
            messages.info(request, "Passwords do not match")
            return redirect("register")

    else:
        return render(request, 'register.html', context)
    

# @login_required
def cont(request):
    if Profile.objects.filter(owner=request.user).exists():
        return redirect("dashboard")
    else:
        user_model = User.objects.get(username=request.user)
        new_profile = Profile.objects.create(owner=user_model, id_user=user_model.id)
        new_profile.save()
        ctx = {
            'user' : user_model.username
        }
        message = get_template('mail.html').render(ctx)
        msg = EmailMessage(
            'Welcome to Sigma',
            message,
            'Paradoxx',
            [user_model.email],
        )
        msg.content_subtype ="html"# Main content is now text/html
        msg.send()
    return redirect("edit-profile")
    

def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    context = {
        'posts' : posts,
        'title' : "Blog"
    }
    return render(request, 'blog.html', context)



def blog_detail(request, pk):
    post = BlogPost.objects.get(slug=pk)

    context = {
        'post' : post,
        'title' : post.title
    }

    return render(request, 'blog-details.html', context)




# UNAUTHENTICATED VIEWS END



# AUTHENTICATED VIEWS START


@login_required
def edit_profile(request):
    user_profile = Profile.objects.get(owner=request.user)

    if request.method == "POST":
        phone_number = request.POST['phone_number']
        how_did_you_hear_about_us = request.POST['how_did_you_hear_about_us']
        nationality = request.POST['nationality']
        address = request.POST['address']
        about_me = request.POST['about_me']


        user_profile.phone_number = phone_number
        user_profile.how_did_you_hear_about_us = how_did_you_hear_about_us
        user_profile.nationality = nationality
        user_profile.address = address
        user_profile.about_me = about_me
        user_profile.save()

        return redirect("dashboard")



    context = {
        "user_profile" : user_profile
    }


    
    return render(request, 'profile.html', context)

@login_required
def dashboard(request):
    all_polls = Poll.objects.all()
    paginator = Paginator(all_polls, 6)
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls' : polls
    }
    return render(request, 'dashboard.html', context)

@login_required
def poll_list(request):
    all_polls = Poll.objects.all()
    paginator = Paginator(all_polls, 6)
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls' : polls
    }

    return render(request, 'poll_list.html', context)

@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'poll_detail.html', context)



@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("poll-list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'poll_result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("detail", poll_id)
    return render(request, 'poll_result.html', {'poll': poll})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

# AUTHENTICATED VIEWS END