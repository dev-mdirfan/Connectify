from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

def register(request):
    '''
    Register view for user model.

    Parameters:
        - request: The HTTP request object.

    Returns:
        - If the registration is successful, redirects to a success page.
        - If the registration fails, renders the registration form with error messages.

    Requirements:
        - Length of username should be greater or equal to 3.
        - Password must match the confirmation password.
        - Username should be unique.
        - Email should be unique.

    '''

    if request.method == 'POST':
        # Get form data
        username = request.POST['signup-username']
        email = request.POST['signup-email']
        password = request.POST['signup-password']
        confirm_password = request.POST['signup-password-confirm']
        terms = request.POST.get('signup-terms')

        # Check if username meets the length requirement
        if len(username) < 3:
            messages.error(request, 'Username should be at least 3 characters long.')
            return redirect('register')

        # Check if password matches the confirmation password
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
            # Check if username and email already exist
            messages.error(request, 'Username and email are already taken.')
        elif User.objects.filter(username=username).exists():
            # Check if username already exists
            messages.error(request, 'Username is already taken.')
        elif User.objects.filter(email=email).exists():
            # Check if email already exists
            messages.error(request, 'Email is already taken.')
            return redirect('register')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Registration successful. You can now log in.')
        # user is automatically logged in after registration
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return redirect('index')

    else:
        # Render the registration form
        return render(request, 'accounts/register.html')


def login(request):
    '''
    Login view for user authentication.

    Parameters:
        - request: The HTTP request object.

    Returns:
        - If the login is successful, redirects to a success page.
        - If the login fails, renders the login form with error messages.

    Requirements:
        - User must provide a valid username and password combination.

    '''

    if request.method == 'POST':
        # Get form data
        username = request.POST['login-username']
        password = request.POST['login-password']

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Log in the user
            auth.login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    else:
        # Render the login form
        return render(request, 'accounts/login.html')



def logout(request):
    '''
    Logout view for user authentication.

    Parameters:
        - request: The HTTP request object.

    Returns:
        - Redirects to the login page.

    '''

    # Log out the user
    auth.logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('index')


