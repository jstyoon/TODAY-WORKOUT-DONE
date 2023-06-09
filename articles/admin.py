from django.contrib import admin
from .models import Articles,Category,InSubCategory,OutSubCategory
# Register your models here.

admin.site.register(Articles)
admin.site.register(Category)
admin.site.register(InSubCategory)
admin.site.register(OutSubCategory)