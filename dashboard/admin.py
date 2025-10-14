from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Attendance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'employee_name', 'employee_email', 'employee_phone', 
        'department', 'employee_designation', 'shift_timings', 'employee_status', 
        'profile_image_tag', 'created_at'
    ]
    list_filter = ['department', 'employee_status', 'shift_timings']
    search_fields = ['employee_id', 'employee_name', 'employee_email', 'employee_phone']
    readonly_fields = ['employee_id', 'created_at', 'profile_image_tag']
    ordering = ['-created_at']
    fieldsets = (
        (None, {
            'fields': (
                'user', 'employee_name', 'employee_email', 'employee_phone', 
                'employee_address', 'profile_image', 'profile_image_tag'
            )
        }),
        ('Job Info', {
            'fields': (
                'employee_id', 'employee_designation', 'department', 
                'shift_timings', 'employee_status'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:50%;" />', obj.profile_image.url)
        return "-"
    profile_image_tag.short_description = 'Profile Image'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'date', 'check_in', 'check_in_image_tag', 
        'check_out', 'check_out_image_tag', 'status', 'remarks', 'created_at'
    ]
    list_filter = ['status', 'remarks', 'date']
    search_fields = ['employee__employee_name', 'employee__employee_id']
    readonly_fields = ['created_at', 'check_in_image_tag', 'check_out_image_tag']
    ordering = ['-date']
    fieldsets = (
        (None, {
            'fields': (
                'employee', 'date', 'check_in', 'check_in_image', 'check_in_image_tag',
                'check_out', 'check_out_image', 'check_out_image_tag', 'status', 'remarks'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def check_in_image_tag(self, obj):
        if obj.check_in_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:5px;" />', obj.check_in_image.url)
        return "-"
    check_in_image_tag.short_description = 'Check-In Image'

    def check_out_image_tag(self, obj):
        if obj.check_out_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:5px;" />', obj.check_out_image.url)
        return "-"
    check_out_image_tag.short_description = 'Check-Out Image'
