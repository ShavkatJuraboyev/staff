import openpyxl
from django.shortcuts import get_object_or_404, render, redirect
from .models import Employee
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def upload_excel(request):
    if request.method == "POST" and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        # Faylni ochish
        try:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active

            # Excel faylidagi qatorlarga o'qish
            for row in sheet.iter_rows(min_row=2, values_only=True):  # 1-qatordan keyingi qatorlar
                Employee.objects.create(
                    employee_id=row[0],
                    citizenship=row[1],
                    passport=row[2],
                    personal_number=row[3],
                    faculty=row[4],
                    department=row[5],
                    frist_name=row[6],
                    last_name=row[7],
                    sur_name=row[8],
                    labor_form=row[9],
                    stavka=row[10],
                    position=row[11],
                    academic_degree=row[12],
                    academic_title=row[13],
                    expertise=row[14],
                    start_position=row[15],
                    contract_number=row[16],
                    contract_date=row[17],
                    order_number=row[18],
                    order_date=row[19],
                    bithday=row[20],
                    gender=row[22],
                    email=row[23],
                    phone=row[24],
                    permanent_registration=row[25],
                )
            messages.success(request, "Ma'lumotlar muvaffaqiyatli saqlandi!")
        except Exception as e:
            messages.error(request, f"Xato yuz berdi: {str(e)}")
        
        return redirect('upload_excel')  # Foydalanuvchini qaytarish

    return render(request, 'admin/upload_excel.html')


def all_employees(request):
    employees = Employee.objects.all()[::-1] # barcha talabalar malumotni olish
    query = request.GET.get('q', '') # Qidiruv so'zini olish
    if query:
        employees = Employee.objects.filter(
            Q(frist_name__icontains=query) | # Ismi
            Q(last_name__icontains=query) | # Familiyasi
            Q(sur_name__icontains=query) | # Otasining ismi
            Q(employee_id__icontains=query) | # Xodim ID
            Q(stavka__icontains=query) | # Stavka
            Q(age__icontains=query)  # O'qituvchilarning yoshi
        )

    page_size = request.GET.get('page_size', 7)  # Agar qiymat bo'lmasa, default 7 bo'ladi
    paginator = Paginator(employees, page_size)  # Paginatorni yaratish
    page_number = request.GET.get('page')  # Foydalanuvchi tanlagan sahifa raqamini olish
    page_obj = paginator.get_page(page_number) # Tanlangan sahifani olish

    context =  {
        'page_obj':page_obj, 'employees': employees, 'segment':'employee'
        }
    return render(request, 'employee/all_employees.html', context=context)


def view_employees(request, employee_id):
    try:
        employee = Employee.objects.filter(employee_id=employee_id).first()
    except Employee.DoesNotExist:
        return HttpResponseNotFound("Xaodim topilmadi.")
    
    context = {
        "employee": employee, 'segment':'employee'
        }

    return render(request, "employee/view_employees.html", context=context)

def add_employees(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        citizenship = request.POST.get("citizenship")
        passport = request.POST.get("passport")
        personal_number = request.POST.get("personal_number")
        faculty = request.POST.get("faculty")
        department = request.POST.get("department")
        frist_name = request.POST.get("frist_name")
        last_name = request.POST.get("last_name")
        sur_name = request.POST.get("sur_name")
        labor_form = request.POST.get("labor_form")
        stavka = request.POST.get("stavka")
        position = request.POST.get("position")
        academic_degree = request.POST.get("academic_degree")
        academic_title = request.POST.get("academic_title")
        expertise = request.POST.get("expertise")
        start_position = request.POST.get("start_position")
        contract_number = request.POST.get("contract_number")
        contract_date = request.POST.get("contract_date")
        order_number = request.POST.get("order_number")
        order_date = request.POST.get("order_date")
        bithday = request.POST.get("bithday")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        permanent_registration = request.POST.get("permanent_registration")
        organization = request.POST.get("organization")
        nationality = request.POST.get("nationality")
        place_of_birth = request.POST.get("place_of_birth")
        city = request.POST.get("city")
        graduation_end_year = request.POST.get("graduation_end_year")
        end_education = request.POST.get("end_education")
        
        employee = Employee.objects.create(
            employee_id=employee_id, citizenship=citizenship, passport=passport, personal_number=personal_number,
            faculty=faculty, department=department, frist_name=frist_name,
            last_name=last_name, sur_name=sur_name, labor_form=labor_form,
            stavka=stavka, position=position, academic_degree=academic_degree,
            academic_title=academic_title, expertise=expertise, start_position=start_position,
            contract_number=contract_number, contract_date=contract_date, order_number=order_number,
            order_date=order_date, bithday=bithday, gender=gender,
            email=email, phone=phone, permanent_registration=permanent_registration,
            organization=organization, nationality=nationality, place_of_birth=place_of_birth,
            city=city, graduation_end_year=graduation_end_year, end_education=end_education,
        )

        return redirect("all_employees")  # Talabalar ro'yxatiga yo'naltirish
    context = {'segment':'employee'}
    return render(request, "employee/add_employees.html", context=context)


def edit_employees(request, employee_id):
    employee = Employee.objects.filter(employee_id=employee_id).first()

    if request.method == "POST":
        # Talabaning asosiy ma’lumotlarini yangilash
        employee.employee_id = request.POST.get("employee_id")
        employee.citizenship = request.POST.get("citizenship")
        employee.passport = request.POST.get("passport")
        employee.personal_number = request.POST.get("personal_number")
        employee.faculty = request.POST.get("faculty")
        employee.department = request.POST.get("department")
        employee.frist_name = request.POST.get("frist_name")
        employee.last_name = request.POST.get("last_name")
        employee.sur_name = request.POST.get("sur_name")
        employee.labor_form = request.POST.get("labor_form")
        employee.stavka = request.POST.get("stavka")
        employee.position = request.POST.get("position")
        employee.academic_degree = request.POST.get("academic_degree")
        employee.academic_title = request.POST.get("academic_title")
        employee.expertise = request.POST.get("expertise")
        employee.start_position = request.POST.get("start_position")
        employee.contract_number = request.POST.get("contract_number")
        employee.contract_date = request.POST.get("contract_date")
        employee.order_number = request.POST.get("order_number")
        employee.order_date = request.POST.get("order_date")
        employee.bithday = request.POST.get("bithday")
        employee.gender = request.POST.get("gender")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")
        employee.permanent_registration = request.POST.get("permanent_registration")
        employee.organization = request.POST.get("organization")
        employee.nationality = request.POST.get("nationality")
        employee.place_of_birth = request.POST.get("place_of_birth")
        employee.city = request.POST.get("city")
        employee.graduation_end_year = request.POST.get("graduation_end_year")
        employee.end_education = request.POST.get("end_education")

        employee.save()


        return redirect("all_employees")  # Talabalar ro'yxatiga yo'naltirish
    context = {
        "employee": employee, 'segment':'employee'
        }

    return render(request, "employee/add_employees.html", context=context)


def delete_employees(request, employee_id):
    employee = Employee.objects.filter(employee_id=employee_id).first()
    employee.delete()
    return redirect("all_employees")
