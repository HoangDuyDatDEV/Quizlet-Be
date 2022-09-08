from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Folder)
admin.site.register(FlashCard)
admin.site.register(User)
admin.site.register(UserInClass)
admin.site.register(CourseInClass)
admin.site.register(CourseInFolder)
admin.site.register(FolderInClass)

