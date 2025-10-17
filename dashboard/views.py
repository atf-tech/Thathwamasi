from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import date
from .models import Employee, Attendance
import os
import base64
from django.utils import timezone
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render
from django.core.files.base import ContentFile








#Login
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('home')
        else:
           messages.error(request, "Invalid credentials or not authorized.")
    return render(request, 'dashboard/login.html')




#Logout
@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def keep_alive(request):
    """Keeps the session alive by marking it as modified."""
    request.session.modified = True
    return JsonResponse({'status': 'alive'})





@login_required(login_url='/dashboard/login')
def home(request):
    emp_name = request.GET.get('employee', '').strip()
    date_str = request.GET.get('date', '').strip() 

    attendance_records = Attendance.objects.select_related('employee').order_by('-date', '-check_in', '-check_out')

    if emp_name:
        attendance_records = attendance_records.filter(employee__employee_name=emp_name)

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            attendance_records = attendance_records.filter(date=date_obj)
        except ValueError:
            pass

    total_employees = Employee.objects.filter(employee_status=True).count()
    today = timezone.localdate()
    present_today = Attendance.objects.filter(date=today).count()
    absent_today = total_employees - present_today
    all_present = absent_today == 0

    employee_list = Employee.objects.filter(employee_status=True).values_list('employee_name', flat=True).distinct()

    return render(request, 'dashboard/index.html', {
        'attendance_records': attendance_records,
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_overview': f"{present_today}/{total_employees}",
        'all_present': all_present,
        'employee_list': employee_list,
        'selected_employee': emp_name,
        'selected_date': date_str,
    })






@login_required(login_url='/dashboard/login')
def employee(request):
    emp_id = request.POST.get('emp_id')

    if request.method == 'POST':
        # DELETE
        if 'delete' in request.POST:
            delete_id = request.POST.get('delete')
            emp = get_object_or_404(Employee, id=delete_id)
            emp.delete()
            messages.success(request, "Employee deleted successfully.")
            return redirect('employee')

        # CREATE OR UPDATE
        if emp_id:
            emp = get_object_or_404(Employee, id=emp_id)
            messages_text = "Employee updated successfully."
        else:
            emp = Employee()
            messages_text = "Employee created successfully."

        # Update employee fields
        emp.employee_name = request.POST['employee_name']
        emp.employee_email = request.POST['employee_email']
        emp.employee_phone = request.POST['employee_phone']
        emp.employee_designation = request.POST.get('employee_designation')
        emp.department = request.POST.get('department')
        emp.shift_timings = request.POST.get('shift_timings')
        emp.employee_address = request.POST.get('employee_address')

        if request.FILES.get('profile_image'):
            emp.profile_image = request.FILES.get('profile_image')

        try:
            emp.save()
            messages.success(request, messages_text)
        except IntegrityError as e:
            if 'employee_email' in str(e):
                messages.error(request, "Error: This email is already registered.")
            elif 'employee_phone' in str(e):
                messages.error(request, "Error: This phone number is already registered.")
            else:
                messages.error(request, "Error: Could not save employee. Please check the data.")

        return redirect('employee')

    employees = Employee.objects.all()
    return render(request, 'dashboard/employee.html', {'employees': employees})






@csrf_exempt
def attendance(request):
    ctx = {"show_step2": False}

    if request.method == "POST":
        step = request.POST.get("step")
        phone_no = request.POST.get("phone_no", "").strip()

        try:
            employee = Employee.objects.get(employee_phone=phone_no, employee_status=True)
        except Employee.DoesNotExist:
            ctx.update(message="Invalid phone number.", message_class="danger")
            return render(request, "dashboard/attendance.html", ctx)

        ctx["employee"] = employee
        today = timezone.localdate()
        now_time = timezone.localtime().time()

        attendance = Attendance.objects.filter(employee=employee, date=today).first()
        ctx["attendance"] = attendance
        ctx["current_time"] = timezone.localtime().strftime("%I:%M:%S %p")
        ctx["show_step2"] = True

        if employee.shift_timings:
            try:
                shift_start = datetime.strptime(employee.shift_timings.split("to")[0].strip(), "%H:%M").time()
            except:
                shift_start = datetime.strptime("09:30", "%H:%M").time()
        else:
            shift_start = datetime.strptime("09:30", "%H:%M").time()

        grace_time = (datetime.combine(today, shift_start) + timedelta(minutes=5)).time()

        if not attendance:
            if now_time <= shift_start:
                pre_remarks = "On Time"
            elif now_time <= grace_time:
                pre_remarks = "Grace"
            else:
                pre_remarks = "Late"
        else:
            pre_remarks = attendance.remarks

        ctx["pre_remarks"] = pre_remarks

        if step == "verify":
            return render(request, "dashboard/attendance.html", ctx)

        # ---- Capture image ----
        image_data = request.POST.get("image_data", "")
        if not image_data:
            ctx.update(message="Please capture a photo.", message_class="danger")
            return render(request, "dashboard/attendance.html", ctx)

        address = request.POST.get("address", "").strip()

        header, imgstr = image_data.split(";base64,")
        ext = header.split("/")[-1]
        file_content = ContentFile(
            base64.b64decode(imgstr),
            name=f"{employee.employee_id}_{timezone.now().strftime('%H%M%S')}.{ext}"
        )

        if not attendance: 
            if now_time <= shift_start:
                remarks = "On Time"
            elif now_time <= grace_time:
                remarks = "Grace"
            else:
                remarks = "Late"

            attendance = Attendance.objects.create(
                employee=employee,
                date=today,
                check_in=now_time,
                check_in_image=file_content,
                remarks=remarks,
                status="Present",
                check_in_location=address  
            )

            ctx.update(
                message=f"Checked in at {attendance.check_in.strftime('%I:%M:%S %p')} ({attendance.remarks})",
                message_class="success",
                preview_url=attendance.check_in_image.url
            )

        elif attendance and not attendance.check_out:
            attendance.check_out = now_time
            attendance.check_out_image = file_content
            attendance.check_out_location = address 
            attendance.save()

            ctx.update(
                message=f"Checked out at {attendance.check_out.strftime('%I:%M:%S %p')}",
                message_class="success",
                preview_url=attendance.check_out_image.url
            )

        else:  
            ctx.update(
                message=f"Already checked out at {attendance.check_out.strftime('%I:%M:%S %p')}",
                message_class="info"
            )

        ctx["attendance"] = attendance
        return render(request, "dashboard/attendance.html", ctx)

    return render(request, "dashboard/attendance.html", ctx)
