from django.contrib import admin

# Register your models here.
from .models import Members,Payment,GymReport
admin.site.register(Members)
admin.site.register(Payment)
admin.site.register(GymReport)