"""users model"""

from django.db import models
from django.contrib.auth.models import User

ROL_CHOICES = (
    (1, 'Admin'),
    (2, 'Consulta')
)


class Institution(models.Model):
    """Institutions model"""
    name = models.CharField('Nombre', max_length=30, blank=True)

    def __str__(self):
        """return name"""
        return self.name


class Profile(models.Model):
    """Profile model that extens the db with other informations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveIntegerField(
        'Rol',
        choices=ROL_CHOICES,
    )
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return username"""
        return self.user.username
