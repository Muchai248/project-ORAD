from django.contrib import admin
from database.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Document)

