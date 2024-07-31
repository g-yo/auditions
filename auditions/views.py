from django.shortcuts import *
from .models import Movie
from .forms import *
from django.shortcuts import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.contrib.auth.decorators import login_required



def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'auditions/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'auditions/movie_detail.html', {'movie': movie})

def apply_for_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.movie = movie
            application.save()
            return redirect('application_success')
    else:
        form = ApplicationForm()
    return render(request, 'auditions/apply_form.html', {'form': form, 'movie': movie})

def application_success(request):
    return render(request, 'auditions/application_success.html')

def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'auditions/movie_add.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Send a welcome email
            subject = 'Welcome to ACTRS'
            message = f'Thank you for registering, {user.full_name}!'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=True)

            # Log in the user after registration
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Redirect to the movie list page
            return redirect('movie_list')
        else:
            # Handle form errors
            form.add_error(None, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auditions/register.html', {'form': form})

logger = logging.getLogger(__name__)

def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Log username but not password
            logger.debug(f'Attempting login for username: {username}')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('movie_list')
            else:
                logger.error(f'Invalid login attempt for username: {username}')
                form.add_error(None, "Invalid username or password.")
        else:
            logger.error(f'Form is not valid: {form.errors}')
            form.add_error(None, "Please correct the errors below.")
    else:
        form = AuthenticationForm()

    return render(request, 'auditions/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('movie_list')


@login_required
def user_profile(request):
    return render(request, 'auditions/user_profile.html')