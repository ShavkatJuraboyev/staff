import openpyxl, csv # Excel fayllarini o'qish uchun
from django.shortcuts import render, redirect # render va redirect kutubxonasini import qilamiz
from .models import Employee # Talabalar modelini import qilamiz
from django.contrib import messages # Xabarlar uchun
from django.db.models import Q # Q kutubxonasini import qilamiz
from django.core.paginator import Paginator # Paginator kutubxonasini import qilamiz
from django.http import HttpResponseNotFound, HttpResponse # 404 xatolikni chiqarish uchun
import requests # requests kutubxonasini import qilamiz
from django.http import HttpResponse

def export_excel(request):
    # Filtrlarni olish
    katta_yosh = request.GET.get('katta', None)  # Katta yosh filtri
    kichik_yosh = request.GET.get('kichik', None)  # Kichik yosh filtri
    gender = request.GET.get('gender', None)  # Jinsi
    ilmiy_daraja = request.GET.get('ilmiy_daraja', None)  # Ilmiy daraja
    ilmiy_unvon = request.GET.get('ilmiy_unvon', None)  # Ilmiy unvon
    
    employees = Employee.objects.all()

    if katta_yosh:
        employees = employees.filter(age__gte=katta_yosh)

    if kichik_yosh:
        employees = employees.filter(age__lte=kichik_yosh)

    if gender:
        employees = employees.filter(gender=gender)

    if ilmiy_daraja:
        employees = employees.filter(academic_degree=ilmiy_daraja)

    if ilmiy_unvon:
        employees = employees.filter(academic_title=ilmiy_unvon)

    # Excel faylni yaratish
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Employees"

    # Sarlavha qatorini qo'shamiz
    headers = [
        "Xodim ID", "Fuqaroligi", "Passport seriyasi", "Shaxsiy raqam (JSHER)", "Fakulteti",
        "Kafedra/Bo'lim", "Ismi", "Familiyasi", "Otasining ismi", "Ish shakli", "Stavka",
        "Lavozimi", "Ilmiy darajasi", "Ilmiy unvon", "Mutaxassisligi", "Ishga kirgan sana",
        "Shartnoma raqami", "Shartnoma sanasi", "Buyruq raqami", "Buyruq sanasi", 
        "Tug'ilgan kun", "Yoshi", "Jinsi", "Email", "Telefon raqami", "Doimiy yashash joyi",
        "Tashkiloti nomi", "Millati", "Tug'ilgan joyi", "Tuman yoki Shaxar",
        "Tugatgan yili", "Tugatgan oliy ta'lim nomi"
    ]
    sheet.append(headers)

    for employee in enumerate(employees, start=1):
        sheet.append([
            employee.employee_id, employee.citizenship, employee.passport, employee.personal_number,
            employee.faculty, employee.department, employee.frist_name, employee.last_name,
            employee.sur_name, employee.labor_form, employee.stavka, employee.position,
            employee.academic_degree, employee.academic_title, employee.expertise, employee.start_position,
            employee.contract_number, employee.contract_date, employee.order_number, employee.order_date,
            employee.bithday, employee.age, employee.gender, employee.email, employee.phone,
            employee.permanent_registration, employee.organization, employee.nationality,
            employee.place_of_birth, employee.city, employee.graduation_end_year, employee.end_education
        ])

    # Javob qaytarish
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
    workbook.save(response)
    return response


def get_employment_info(hemis_id): # Hemis ID bo'yicha ish joyi ma'lumotlarini olish
    """Hemis id kiritilishi lozim"""
    url = f"https://student.samtuit.uz/rest/v1/data/employee-list?type=all&search={hemis_id}" # API URL
    token = "Y-R36P1BY-eLfuCwQbcbAlvt9GAMk-WP" # Token
    headers = {"Authorization": "Bearer " + token} # Tokenni headerga qo'shish
    response = requests.get(url, headers=headers) # API ga so'rov yuborish
    if response.status_code == 200: # Agar so'rov muvaffaqiyatli bo'lsa
        return response.json() # JSON ma'lumotlarni qaytarish
    return None # Aks holda None qaytarish


def export_employees_to_excel(request):
    # Excel faylni yaratamiz
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Employees"

    # Sarlavha qatorini qo'shamiz
    headers = [
        "Xodim ID", "Fuqaroligi", "Passport seriyasi", "Shaxsiy raqam (JSHER)", "Fakulteti",
        "Kafedra/Bo'lim", "Ismi", "Familiyasi", "Otasining ismi", "Ish shakli", "Stavka",
        "Lavozimi", "Ilmiy darajasi", "Ilmiy unvon", "Mutaxassisligi", "Ishga kirgan sana",
        "Shartnoma raqami", "Shartnoma sanasi", "Buyruq raqami", "Buyruq sanasi", 
        "Tug'ilgan kun", "Yoshi", "Jinsi", "Email", "Telefon raqami", "Doimiy yashash joyi",
        "Tashkiloti nomi", "Millati", "Tug'ilgan joyi", "Tuman yoki Shaxar",
        "Tugatgan yili", "Tugatgan oliy ta'lim nomi"
    ]
    sheet.append(headers)

    # Ma'lumotlarni qo'shamiz
    employees = Employee.objects.all()
    for employee in employees:
        sheet.append([
            employee.employee_id, employee.citizenship, employee.passport, employee.personal_number,
            employee.faculty, employee.department, employee.frist_name, employee.last_name,
            employee.sur_name, employee.labor_form, employee.stavka, employee.position,
            employee.academic_degree, employee.academic_title, employee.expertise, employee.start_position,
            employee.contract_number, employee.contract_date, employee.order_number, employee.order_date,
            employee.bithday, employee.age, employee.gender, employee.email, employee.phone,
            employee.permanent_registration, employee.organization, employee.nationality,
            employee.place_of_birth, employee.city, employee.graduation_end_year, employee.end_education
        ])

    # Javob qaytarish
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
    workbook.save(response)
    return response


def upload_excel(request): # Excel faylni yuklash
    if request.method == "POST" and request.FILES.get('excel_file'): # POST so'rovni tekshirish
        excel_file = request.FILES['excel_file'] # Excel faylini olish

        # Faylni ochish
        try:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active

            # Excel faylidagi qatorlarga o'qish
            for row in sheet.iter_rows(min_row=2, values_only=True):  # 1-qatordan keyingi qatorlar
                Employee.objects.create(
                    employee_id=row[0], # Xodim ID
                    citizenship=row[1], # Fuqarolik
                    passport=row[2], # Passport
                    personal_number=row[3], # Shaxsiy raqam
                    faculty=row[4], # Fakultet
                    department=row[5], # Kafedra
                    frist_name=row[6], # Ismi
                    last_name=row[7], # Familiyasi
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
                    gender=row[22],  # Corrected index for gender
                    email=row[23],   # Corrected index for email
                    phone=row[24],   # Corrected index for phone
                    permanent_registration=row[25],  # Corrected index for permanent_registration
                )
            messages.success(request, "Ma'lumotlar muvaffaqiyatli saqlandi!") # Xabar chiqarish
        except Exception as e: # Xatolikni tekshirish
            messages.error(request, f"Xato yuz berdi: {str(e)}") # Xabar chiqarish
        
        return redirect('upload_excel')  # Foydalanuvchini qaytarish

    return render(request, 'admin/upload_excel.html') # Agar POST bo'lmasa, faylni yuklash sahifasini chiqarish


def all_employees(request):
    employees = Employee.objects.all().order_by('-id')  # Barcha xodimlarni olish
    query = request.GET.get('q', '')  # Qidiruv uchun so'rov
    katta_yosh = request.GET.get('katta', None)  # Katta yosh filtri
    kichik_yosh = request.GET.get('kichik', None)  # Kichik yosh filtri
    gender = request.GET.get('gender', None)  # Jinsi
    ilmiy_daraja = request.GET.get('ilmiy_daraja', None)  # Ilmiy daraja
    ilmiy_unvon = request.GET.get('ilmiy_unvon', None)  # Ilmiy unvon
    academic_degree = Employee.objects.filter(academic_degree__isnull=False).values_list('academic_degree', flat=True).distinct() # Ilmiy darajalar
    academic_title = Employee.objects.filter(academic_title__isnull=False).values_list('academic_title', flat=True).distinct() # Ilmiy unvonlar

    # Filtrlash
    if query:
        employees = employees.filter(
            Q(frist_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(sur_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(phone__icontains=query) |
            Q(age__icontains=query)
        )
    if katta_yosh:
        employees = employees.filter(age__gte=int(katta_yosh))  # Yoshdan katta
    if kichik_yosh:
        employees = employees.filter(age__lte=int(kichik_yosh))  # Yoshdan kichik
    if gender:
        employees = employees.filter(gender=gender)  # Jinsi bo'yicha filtr
    if ilmiy_daraja:
        employees = employees.filter(academic_degree=ilmiy_daraja)  # Ilmiy daraja bo'yicha filtr
    if ilmiy_unvon:
        employees = employees.filter(academic_title=ilmiy_unvon)  # Ilmiy unvon bo'yicha filtr


    # Pagination
    page_size = request.GET.get('page_size', 10)  # Default 10
    paginator = Paginator(employees, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if the request is an AJAX request using the proper header
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # If it's an AJAX request, return filtered employee data (optional: add pagination if needed)
        context = {
                'page_obj': page_obj,
                'employees': employees,
                'segment': 'employee',
                "academic_degree": academic_degree,
                "academic_title": academic_title
            }
        return render(request, 'employee/all_employees.html', context)
    

    context = {
        'page_obj': page_obj,
        'employees': employees,
        'segment': 'employee',
        "academic_degree": academic_degree,
        "academic_title": academic_title
    }
    return render(request, 'employee/all_employees.html', context=context)



def view_employees(request, employee_id): # Xodim ma'lumotlarini ko'rish
    try: # Xodimni topish
        employee = Employee.objects.filter(employee_id=employee_id).first() # Xodimni olish
        user_data = get_employment_info(employee_id)
        user_info = user_data.get('data', {}).get('items', [])[0]

    except Employee.DoesNotExist: # Agar xodim topilmasa
        return HttpResponseNotFound("Xaodim topilmadi.") # 404 xatolikni chiqarish
    
    context = {
        "employee": employee, 'segment':'employee',
        'user_info':user_info
        }   # Context yaratish

    return render(request, "employee/view_employees.html", context=context) # Xodim ma'lumotlarini chiqarish


def add_employees(request): # Xodim qo'shish
    if request.method == "POST": # POST so'rovni tekshirish
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
        ) # Xodimni yaratish

        return redirect("all_employees")  # Talabalar ro'yxatiga yo'naltirish
    context = {'segment':'employee'} 
    return render(request, "employee/add_employees.html", context=context) # Xodim qo'shish sahifasini chiqarish


def edit_employees(request, employee_id): # Xodim ma'lumotlarini tahrirlash
    employee = Employee.objects.filter(employee_id=employee_id).first() # Xodimni olish

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

        employee.save() # Ma'lumotlarni saqlash


        return redirect("all_employees")  # Talabalar ro'yxatiga yo'naltirish
    context = {
        "employee": employee, 'segment':'employee'
        }

    return render(request, "employee/add_employees.html", context=context) # Xodim ma'lumotlarini tahrirlash sahifasini chiqarish


def delete_employees(request, employee_id): # Xodimni o'chirish
    employee = Employee.objects.filter(employee_id=employee_id).first() # Xodimni olish
    employee.delete() # Xodimni o'chirish
    return redirect("all_employees") # Talabalar ro'yxatiga yo'naltirish
