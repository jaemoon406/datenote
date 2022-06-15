from django.db import models

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The given password must be set')

        email = BaseUserManager.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        verbose_name=_('email'),
        max_length=64,
        unique=True,
        help_text='EMAIL.'
    )
    nickname = models.CharField(_('nickname'), max_length=20, null=False, blank=False)
    profile_image = models.ImageField(_('profile_image'), max_length=1000, null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_("date last work"), default=timezone.now())

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'User'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.nickname

#
# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, email, username, password, **extra_fields):
#         if not email:
#             raise ValueError('이메일을 입력 해 주세요.')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, username, **extra_fields)
#
#     def create_superuser(self, email, password, username, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Is not superuser.')
#
#         return self._create_user(email, password, username, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(_('username'), max_length=20, null=False, blank=False)
#     email = models.EmailField(_('email'), max_length=255, null=False, blank=False, unique=True)
#     nickname = models.CharField(_('nickname'), max_length=15, null=False, blank=False, default=username)
#     profile_image = models.ImageField(_('profile_image'), max_length=1000, null=False, blank=True)
#     is_superuser = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         _("active"),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
#     # last_active = models.DateTimeField(_("date last work"), default=timezone.now())
#
#     objects = UserManager()
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['username', 'email']
#
#     class Meta:
#         db_table = 'User'
