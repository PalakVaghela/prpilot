from django.contrib import admin
from .models import User
# Register your models here.

admin.site.register(User)
# because django provide a admin panel so if we register our model in it, data will visible there without any
