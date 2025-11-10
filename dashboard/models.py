from django.db import models
from django.contrib.auth.models import User

SHIFT_CHOICES = [
    ('09:00 to 18:00', '09:00 to 18:00'),
    ('09:30 to 17:30', '09:30 to 17:30'),
    ('10:00 to 18:00', '10:00 to 18:00'),
]

DEPARTMENT_CHOICES = [
    ('Tech', 'Tech'),
    ('Digital Marketing', 'Digital Marketing'),
    ('Video Editor', 'Video Editor'),
    ('RM', 'RM'),
    ('Admin', 'Admin'),
    ('HR', 'HR'),
    ('Field Team', 'Field Team'),
    ('Video Grapher', 'Video Grapher'),
    ('Media', 'Media'),
]

class Employee(models.Model):
    
    employee_name = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=10, unique=True, blank=True)
    employee_email = models.EmailField(max_length=50, unique=True)
    employee_phone = models.CharField(max_length=15, unique=True)
    employee_address = models.TextField(blank=True, null=True)
    employee_designation = models.CharField(max_length=100, blank=True, null=True)
    employee_status = models.BooleanField(default=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    shift_timings = models.CharField(max_length=20, blank=True, null=True, choices=SHIFT_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.employee_name} ({self.employee_id})"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_emp = Employee.objects.all()
            max_id = 0
            for emp in last_emp:
                try:
                    parts = emp.employee_id.split('TI')
                    if len(parts) == 2:
                        num = int(parts[1])
                        if num > max_id:
                            max_id = num
                except:
                    continue
            new_id = max_id + 1
            self.employee_id = f"TI{new_id:03d}"  
        super().save(*args, **kwargs)





ATTENDANCE_STATUS = [
    ('Present', 'Present'),
    ('Absent', 'Absent'),
  
]

ATTENDANCE_REMARKS = [
    ('On Time', 'On Time'),
    ('Grace', 'Grace'),
    ('Late', 'Late'),
    ('Permission', 'Permission'),
    ('Half Day', 'Half Day'),
    
]

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.TimeField(blank=True, null=True)
    check_in_image = models.ImageField(upload_to='checkin_images/', blank=True, null=True)
    check_in_location = models.TextField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    check_out_image = models.ImageField(upload_to='checkout_images/', blank=True, null=True)
    check_out_location = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=ATTENDANCE_STATUS, default='Present')
    remarks = models.TextField(blank=True, choices=ATTENDANCE_REMARKS, default='On Time')
    total_duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} ({self.status})"
