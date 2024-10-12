from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

# Create your tests here.
class AccountModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password': 'securepassword123'
        }
        
    def test_create_user_with_valid_data(self):
        """
        Test if a user can be created with valid data.
        """
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        
        # Check if the user has been created successfully
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_admin)
        
    def test_create_superuser(self):
        """
        Test if a superuser can be created with valid data.
        """
        
        User = get_user_model()
        superuser = User.objects.create_superuser(**self.user_data)
        
        # Check if the superuser has been created successfully
        self.assertEqual(superuser.email,self.user_data['email'])
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_superadmin)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        
    def test_user_requires_email(self):
        """
        Test that creating a user without an email raises a ValueError.
        """
        User = get_user_model()

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                username='testuser',
                first_name='Test',
                last_name='User',
                password='securepassword123'
            )

    def test_user_requires_username(self):
        """
        Test that creating a user without a username raises a ValueError.
        """
        User = get_user_model()

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='testuser@example.com',
                username=None,
                first_name='Test',
                last_name='User',
                password='securepassword123'
            )

    def test_create_user_with_existing_email(self):
        """
        Test that creating a user with a duplicate email raises IntegrityError.
        """
        User = get_user_model()

        # Create the first user
        User.objects.create_user(**self.user_data)

        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.user_data['email'],
                username='testuser2',
                first_name='Test2',
                last_name='User2',
                password='securepassword456'
            )

    def test_user_str_method(self):
        """
        Test the __str__ method returns the correct email.
        """
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])