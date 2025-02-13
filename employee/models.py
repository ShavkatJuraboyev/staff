from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Rol nomi")  # Rol nomi
    permissions = models.TextField(verbose_name="ruxsatlar")  # JSON yoki boshqa formatda ruxsatlar ro'yxati

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Rol yaratish"
        verbose_name_plural = "Rollar"

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="Xodim ID", help_text="Xodim ID", unique=True)
    citizenship = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fuqaroligi", help_text="Fuqaroligini kirting")
    passport = models.CharField(max_length=9, null=True, blank=True, verbose_name="Passport seriyasi", help_text="Passport seriyasini kiritish lozim")
    personal_number = models.CharField(max_length=14, null=True, blank=True, verbose_name="Shaxsiy raqami (JSHER)", help_text="Shaxsiy raqamini kiritish lozim")
    first_name  = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ismi", help_text="Ismini kiritish lozim")
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Familiyasi", help_text="Familiyasini kiritish lozim")
    sur_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Otasining ismi", help_text="Otasining ismini kiritish lozim")
    academic_degree = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ilmiy darajasi", help_text="Ilmiy darajasini kiriting")
    academic_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ilmiy unvon", help_text="Ilmiy unvonini kiriting")
    bithday = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tug'ilgan kun", help_text="Tug'ilgan kunini kiritish lozim")
    age = models.IntegerField(null=True, blank=True, verbose_name="Yoshi", help_text="Yoshini kiritish lozim")
    gender = models.CharField(max_length=10, null=True, blank=True, verbose_name="Jinsi", help_text="Jinsini kiritish lozim")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Email", help_text="Email manzilimi kiritish")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name="Telefon raqami", help_text="Telefon raqamini kiritish lozim")
    permanent_registration = models.CharField(max_length=250, null=True, blank=True, verbose_name="Doimiy yashash joyi", help_text="Doimiy yashash joyini kiritish lozim")

    organization = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tashkiloti nomi", help_text="Tashkilotini kiritish lozim")
    nationality = models.CharField(max_length=50, null=True, blank=True, verbose_name="Millati", help_text="Millatini kiritish lozim")
    place_of_birth = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tug'ilgan joyi", help_text="Tug'ilgan joyini kiritish lozim")
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tuman yoki Shaxar", help_text="Tuman yoki shaharni kiritish lozim")
    graduation_end_year = models.CharField(max_length=250, null=True, blank=True, verbose_name="Oliy ta'lim muassasasini tugatgan yili", help_text="Oliy ta'lim tugatgan yili")
    end_education = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tugatgan oliy ta'limi nomi", help_text="Tugatgan oliy ta'limini kiritish lozim")

    graduation_end_year_mag = models.CharField(max_length=250, null=True, blank=True, verbose_name="Oliy ta'lim muassasasini tugatgan yili (Magistrt)", help_text="Oliy ta'lim tugatgan yili")
    end_education_mag = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tugatgan oliy ta'limi nomi (Magistrt)", help_text="Tugatgan oliy ta'limini kiritish lozim")

    class Meta: 
        verbose_name = "Xodimlar"
        verbose_name_plural = "Xodimlar ro'yxati"

    def save(self, *args, **kwargs):
        if self.bithday:
            birth_date = datetime.strptime(self.bithday, "%d.%m.%Y")
            self.age = datetime.now().year - birth_date.year
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id}-{self.first_name}"
 
class Departments(models.Model):
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Xodimlar", related_name="xodim")
    faculty = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fakulteti", help_text="Fakultetini kiritish lozim")
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name="Kafedra/Bo'lim", help_text="Kafedra/Bo'limini kiritish lozim")
    labor_form = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ish shakli", help_text="Ish shaklini kiritish lozim")
    stavka = models.CharField(max_length=100, null=True, blank=True, verbose_name="Stavka", help_text="Stavkani kiritish lozim")
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name="Lavozimi", help_text="Lavozimini kiritish lozim")
    expertise = models.CharField(max_length=200, null=True, blank=True, verbose_name="Mutaxassisligi", help_text="Mutaxassisligini kiritish lozim")
    start_position = models.CharField(max_length=10, null=True, blank=True, verbose_name="Ishga kirgan sana", help_text="Ishga kirigan sanasini kiritish lozim")
    contract_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Shartnoma raqami", help_text="Shartnoma raqamini kiriting")
    contract_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="Shartnoma sanasi", help_text="Shartnoma sanasini kiriting")
    order_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Buyruq raqami", help_text="Buyruq raqamini kiriting")
    order_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="Buyruq sanasi", help_text="Buyruq sanasini kiriting")

    class Meta:
        verbose_name = "Xodimlar bo'limi"
        verbose_name_plural = "Xodimlar bo'limi"

    def __str__(self):
        return f"{self.employees}-{self.employees.last_name}"
    