from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import get_messages


class RegisterViewTests(TestCase):
    def setUp(self):
        # Create a user with a unique username for testing
        self.existing_user = User.objects.create_user(
            username='existinguser', email='existing@example.com', password='password123'
        )
    
    def test_register_view_invalid_username(self):
        '''
        Test that registration fails when the username is less than 3 characters long.
        Steps to execute:
        1. Create a POST request to the 'register' URL with a username less than 3 characters long.
        2. Assert that the response is redirected to the 'register' URL.
        3. Assert that the response contains the message 'Username should be at least 3 characters long.'
        '''
        response = self.client.post(reverse('register'), {
            'signup-username': 'ab',
            'signup-email': 'test@example.com',
            'signup-password': 'password123',
            'signup-password-confirm': 'password123',
        })
        self.assertRedirects(response, reverse('register'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Username should be at least 3 characters long.',
                    [str(message) for message in messages])

    def test_register_view_password_mismatch(self):
        '''
        Test that registration fails when the password and confirmation password do not match.
        Steps to execute:
        1. Create a POST request to the 'register' URL with a password and confirmation password that do not match.
        2. Assert that the response is redirected to the 'register' URL.
        3. Assert that the response contains the message 'Passwords do not match.'
        '''
        response = self.client.post(reverse('register'), {
            'signup-username': 'testuser',
            'signup-email': 'test@example.com',
            'signup-password': 'password123',
            'signup-password-confirm': 'password456',
        })
        self.assertRedirects(response, reverse('register'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Passwords do not match.',
                    [str(message) for message in messages])

    def test_register_view_existing_username(self):
        '''
        Test that registration fails when the username already exists.
        Steps to execute:
        1. Create a user with an existing username.
        2. Create a POST request to the 'register' URL with the existing username.
        3. Assert that the response is redirected to the 'register' URL.
        4. Assert that the response contains the message 'Username is already taken.'
        '''
        response = self.client.post(reverse('register'), {
            'signup-username': self.existing_user.username,  # Use the existing username
            'signup-email': 'test@example.com',
            'signup-password': 'password123',
            'signup-password-confirm': 'password123',
        })
        self.assertRedirects(response, reverse('register'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Username is already taken.',
                    [str(message) for message in messages])

    def test_register_view_existing_email(self):
        '''
        Test that registration fails when the email already exists.
        Steps to execute:
        1. Create a user with an existing email.
        2. Create a POST request to the 'register' URL with the existing email.
        3. Assert that the response is redirected to the 'register' URL.
        4. Assert that the response contains the message 'Email is already taken.'
        '''
        response = self.client.post(reverse('register'), {
            'signup-username': 'not_testuser',
            'signup-email': 'existing@example.com',
            'signup-password': 'password123',
            'signup-password-confirm': 'password123',
        })
        self.assertRedirects(response, reverse('register'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Email is already taken.',
                    [str(message) for message in messages])
    
    def test_register_view_existing_username_and_email(self):
        '''
        Test that registration fails when the username and email already exist.
        Steps to execute:
        1. Create a user with an existing username and email.
        2. Create a POST request to the 'register' URL with the existing username and email.
        3. Assert that the response is redirected to the 'register' URL.
        4. Assert that the response contains the message 'Username and email are already taken.'
        '''
        response = self.client.post(reverse('register'), {
            'signup-username': 'existinguser',
            'signup-email': 'existing@gmail.com',
            'signup-password': 'password123',
            'signup-password-confirm': 'password123',
        })
        self.assertRedirects(response, reverse('register'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Username and email are already taken.',
                    [str(message) for message in messages])

    def test_register_view_success(self):
        '''
        Test that registration is successful when all requirements are met.
        Steps to execute:
        1. Create a POST request to the 'register' URL with valid registration data.
        2. Assert that the response is redirected to the 'index' URL.
        3. Assert that the response contains the message 'Registration successful. You can now log in.'
        '''
        response = self.client.post(reverse('register'), {
            'signup-username': 'testuser',
            'signup-email': 'test@example.com',
            'signup-password': 'password123',
            'signup-password-confirm': 'password123',
        })
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Registration successful. You can now log in.',
                    [str(message) for message in messages])



class LoginViewTests(TestCase):
    def test_login_view_success(self):
        '''
        Test that login is successful with valid username and password.
        Steps to execute:
        1. Create a user.
        2. Create a POST request to the 'login' URL with valid username and password.
        3. Assert that the response is redirected to the 'index' URL.
        4. Assert that the success message 'Login successful.' is present in the messages.
        '''
        user = User.objects.create_user(
            username='testuser', password='password123')
        response = self.client.post(reverse('login'), {
            'login-username': 'testuser',
            'login-password': 'password123',
        })
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Login successful.', [
                    str(message) for message in messages])

    def test_login_view_invalid_credentials(self):
        '''
        Test that login fails with invalid username or password.
        Steps to execute:
        1. Create a POST request to the 'login' URL with invalid username or password.
        2. Assert that the response is redirected to the 'login' URL.
        3. Assert that the error message 'Invalid username or password.' is present in the messages.
        '''
        response = self.client.post(reverse('login'), {
            'login-username': 'testuser',
            'login-password': 'wrongpassword',
        })
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Invalid username or password.', [
                    str(message) for message in messages])


class LogoutViewTests(TestCase):
    def test_logout_view_success(self):
        '''
        Test that logout is successful.
        Steps to execute:
        1. Create a user.
        2. Log in the user.
        3. Create a POST request to the 'logout' URL.
        4. Assert that the response is redirected to the 'index' URL.
        5. Assert that the success message 'Logout successful.' is present in the messages.
        '''
        user = User.objects.create_user(
            username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Logout successful.', [
                    str(message) for message in messages])
