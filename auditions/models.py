from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now

class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    number_of_people = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='photos/',default='')

    def __str__(self):
        return f'{self.name} for {self.movie.name}'
    


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change this line
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change this line
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = now().date()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        else:
            self.age = None  # Ensure age is set to None if no date_of_birth is provided

        super().save(*args, **kwargs)