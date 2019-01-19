from django.contrib import admin
from accounts.models import UserProfile, CoursesOffered, TutorProfile, StudentProfile, ClassRequest
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'profession', 'city', 'user_type')
admin.site.register(UserProfile, UserProfileAdmin)

class CoursesOfferedAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'study_level', 'subject')
admin.site.register(CoursesOffered, CoursesOfferedAdmin)

class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
admin.site.register(TutorProfile,TutorProfileAdmin)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
admin.site.register(StudentProfile,StudentProfileAdmin)

class ClassRequestAdmin(admin.ModelAdmin):
    list_display = ('user',)
admin.site.register(ClassRequest,ClassRequestAdmin)
