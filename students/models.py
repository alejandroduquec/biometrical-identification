"""Students models"""
# Django
from django.db import models
from django.contrib.auth.models import User
# Models
from users.models import Institution


GENDER_CHOICE = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)


class TypeFood(models.Model):
    """Food type model"""

    name = models.CharField(max_length=30)

    def __str__(self):
        """return type food name"""
        return '{}'.format(self.name)


class TypeDocument(models.Model):
    """Document type model"""

    name = models.CharField(max_length=30)
    abreviation = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        """return type document"""
        return '{}'.format(self.name)


class Student(models.Model):
    """Post model """

    document = models.CharField(max_length=50, unique=True)
    document_type = models.ForeignKey(
        TypeDocument, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICE,
        default='M',
    )
    birthdate = models.DateField('Fecha Nacimiento')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    grade = models.IntegerField()
    group = models.IntegerField()
    estract = models.IntegerField(blank=True, null=True)

    # metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """returrn full name"""
        return '{} {}'.format(self.first_name, self.last_name)
    
    def got_dactilar(self):
        """check dactilar identification"""
        dactilar = DactilarIdentification.objects.filter(student=self)
        if dactilar:
            return True
        else:
            return False


class DactilarIdentification(models.Model):
    """Dactilar information"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dactilar_md = models.BinaryField()
    dactilar_mi = models.BinaryField()

    def __str__(self):
        """return full name"""
        return '{} {}'.format(self.student.first_name, self.student.last_name)


class FoodRation(models.Model):
    """Food Ration Model"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    food_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    food_type = models.ForeignKey(TypeFood, on_delete=models.DO_NOTHING)

    # metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        """return user and food name"""
        return '{} {} / {}'.format(self.student.first_name, self.student.last_name, self.food_type)



