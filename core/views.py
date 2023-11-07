from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import *
from django.contrib import messages
from voteguard import settings
from .models import *


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
    return render(request, "index.html")


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
            return redirect('home') # Redirects to home view
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
        return redirect("home")
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



def blog_detail(self, request, pk):
    post = BlogPost.objects.get(slug=pk)

    context = {
        'post' : post,
        'title' : post.title
    }

    return render(request, 'blog-details.html', context)




# UNAUTHENTICATED VIEWS END



# AUTHENTICATED VIEWS START


def dashboard(request):
    return render(request, 'dashboard.html')

def poll_results(request):
    pass

def poll_vote(request):
    pass

def edit_profile(request):
    user_profile = Profile.objects.get(owner=request.user)

    if request.method == "POST":
        pass


    context = {
        "user_profile" : user_profile
    }


    
    return render(request, 'profile.html', )



# AUTHENTICATED VIEWS END