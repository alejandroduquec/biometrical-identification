"""Admin Students"""

# Django
from django.contrib import admin

# Models
from students.models import (Student, TypeDocument, TypeFood,
                             FoodRation, DactilarIdentification)

admin.site.register(TypeDocument)
admin.site.register(TypeFood)
admin.site.register(FoodRation)
#admin.site.register(DactilarIdentification)