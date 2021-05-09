from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
from django.contrib.auth import get_user_model


def authenticate(username=None, password=None):
    try:
        user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username) | Q(phoneNo__iexact=username))
        if user.check_password(password):
            return user
        return None
    except User.DoesNotExist:
        return None
    except MultipleObjectsReturned:
        return User.objects.filter(email=username).order_by('id').first()
    except Exception:
        return None
