from django.contrib import admin
from .models import *


admin.site.register([User,Role,SubRole,Admin])

# Register your models here.
