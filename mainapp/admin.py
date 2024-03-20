from django.contrib import admin
from .models import Workout


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'description', 'all_sets_done', 'all_arms_done', 'all_legs_done', 'all_chest_done')
    list_filter = ('user', 'date', 'all_sets_done', 'all_arms_done', 'all_legs_done', 'all_chest_done')
    search_fields = ('user__username', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)


admin.site.register(Workout, WorkoutAdmin)