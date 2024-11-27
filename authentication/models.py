from django.db import models


from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


# Role Model
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # description = models.TextField()
      
    def __str__(self):
        return self.name


# SubRole Model
class SubRole(MPTTModel):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    description = models.TextField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


   
# Custom User Manager
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not username:
            raise ValueError("The given username must be set")

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Please enter a valid email")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        if password is None:
            raise ValueError("Password must not be none")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


# User Model
class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    subrole = models.ForeignKey(SubRole, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    



# Admin model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    phone_no = models.CharField(max_length=250)

    def __str__(self):
        return self.user.email        



