from django.contrib import admin

from articles.models import Comment, Articles, Category, InSubCategory, OutSubCategory

admin.site.register(Comment)
admin.site.register(Articles)
admin.site.register(Category)
admin.site.register(InSubCategory)
admin.site.register(OutSubCategory)
