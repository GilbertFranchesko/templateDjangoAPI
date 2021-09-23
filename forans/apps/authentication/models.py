import jwt

from datetime import datetime, timedelta

from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin
)

from .UserManager import UserManager

from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    
    # Each user needs a human-readable unique identifier,
    # which we can use to provide User in the user
    # interface. We will also index this column in the database for
    # improve search speed in the future. 
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a field with which we will be able to
    # contact the user and identify him at login.
    # Since we need the email address anyway, we will also
    # use it for logins, as it is the most
    # the most common form of credentials at the moment (well, another phone).
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wants to use our system, he can
    # want to delete your account. This is a problem for us, since the collected
    # the data is very valuable for us, and we do not want to delete it :) We just offer
    # for users a way to deactivate the account instead of completely deleting it.
    # This way they won't show up on the site, but we can still
    # further analyze the information.
    is_active = models.BooleanField(default=True)


    # This flag determines who can log into the admin area of our
    # site. For most users, this flag will be false.
    is_staff = models.BooleanField(default=False)

    # Timestamp of object creation.
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp showing when the object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    
    
    # Additional fields required by Django
    # when specifying a custom user model.

    # The USERNAME_FIELD property tells us which field we will use
    
    # to login. In this case, we want to use mail.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above is
    # must manage objects of this type.

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self.__generate_jwt_token()


    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username



    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')


        return token.decode("utf-8")

