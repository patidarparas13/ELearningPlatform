from django.contrib import admin
from .models import Subject,Course,Module
# Register your models here.

#@admin.register() decorator to register models in the administration site
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    #The attribute prepopulated_fields tells the admin application to automatically
    # fill the field slug - in this case with the text entered into the title field.
    prepopulated_fields = {'slug':('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','subject','created']
    list_filter = ['created','subject']
    search_fields = ['title','overview']
    prepopulated_fields = {'slug':('title',)}
    inlines = [ModuleInline]
