import http
from django.test import TestCase, override_settings, modify_settings, RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.conf import settings
from django.urls import reverse
from .forms import UserRegisterForm
from .models import Profile,Post

User = get_user_model()

testuser = {
        'username':'1testuser',
        'email':'testuser@example.com',
        'password':'webly.com'
    }

user_data = {
    'username':'Test_User',
    'first_name':'Test',
    'email':'raphaelapeh322@gmail.com',
    'last_name': 'User',
    'password1':'webly.com',
    'password2':'webly.com'
}

error_user_data = {
    'username':'Test User',
    'first_name':'Test',
    'email':'raphaelapeh322@gmail.com',
    'last_name': 'User',
    'password1':'webly.com',
    'password2':'webly.com'
}

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='efefse',email='',password='testuser')
        # self.profile = Profile.objects.create(user=self.user)
        self.post = Post.objects.create(user=self.user,name="TEST USER POST",image="test.png")
    def test_user_profile(self):
        test = self.user.profile.following.count()
        self.assertEqual(test,0)

    def test_post_reverse_relationship(self):
        user_post = self.user.post_set.count()
        self.assertEqual(user_post,1)

class CustomTest(TestCase):

    def test_settings_secret_key_strength(self):
        settings_strength = settings.SECRET_KEY
        validate_password(settings_strength)


class RegisterFormTest(TestCase):
    
    def setUp(self) -> None:
        self.form = UserRegisterForm(user_data)
        self.user = User.objects.create(username='TEST',password='webly.com')
        self.error_form = UserRegisterForm(error_user_data)

    def test_form_is_valid(self):
        form = self.form
        self.assertTrue(form.is_valid())

    def test_form_redirects(self):
        client = self.client.post(reverse('signup'),user_data)
        self.assertRedirects(client,reverse('home'))

    def test_user_registration_template_used(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response,'sign_up.html')

    # Test Invalid form
        
    def test_form_error(self):
        error_form = self.error_form
        self.assertFalse(error_form.is_valid())
        self.assertTrue(error_form.has_error('username'))


class PostModelTest(TestCase):

    def setUp(self)->None:
        self.user = User.objects.create_user(**testuser)
        self.post = Post.objects.create(name=get_random_string(10),user=self.user)
        self.request = RequestFactory()


    def test_user_post_contains(self):
        user = self.user
        post = self.post
        self.assertIn(post,user.post_set.all())
        self.assertTrue(user.post_set.contains(post))
    
    def test_number_of_posts(self):
        pass 
    
    def test_post_comments(self):
        user = self.user
        post = self.post
        with self.assertRaises(AssertionError):
            self.assertEqual(user.post_set.count(),2)
            self.assertEqual(post.comment_set.count(),0)


class UserModelTest(TestCase):

    def setUp(self)->None:
        self.user = User.objects.create_user(**testuser)

    def test_user_password_validation(self):
        pass