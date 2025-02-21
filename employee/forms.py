from django import forms
from employee.models import Employee
from datetime import datetime


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))



class EmployeeForm(forms.ModelForm):
    bithday = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '25.12.2024'}),
        required=False
    )


    class Meta:
        model = Employee
        fields = [
            'employee_id', 'citizenship', 'passport', 'personal_number', 'first_name',
            'last_name', 'sur_name', 'academic_degree', 'academic_title', 'bithday',
            'gender', 'email', 'phone', 'permanent_registration', 'organization',
            'nationality', 'place_of_birth', 'city', 'graduation_end_year', 'end_education',
            'graduation_end_year_mag', 'end_education_mag'
        ]

    def clean_bithday(self):
        bithday = self.cleaned_data.get('bithday')
        if bithday:
            try:
                # Foydalanuvchi kiritgan sanani DD.MM.YYYY formatiga tekshiramiz
                datetime.strptime(bithday, "%d.%m.%Y")
            except ValueError:
                raise forms.ValidationError("Tug‘ilgan sana noto‘g‘ri formatda. To‘g‘ri format: DD.MM.YYYY")
        return bithday

    def clean_passport(self):
        passport = self.cleaned_data.get('passport')
        if passport and len(passport) != 9:
            raise forms.ValidationError("Passport seriyasi 9 ta belgidan iborat bo‘lishi kerak.")
        return passport

    def clean_personal_number(self):
        personal_number = self.cleaned_data.get('personal_number')
        if personal_number and len(personal_number) != 14:
            raise forms.ValidationError("Shaxsiy raqam (JSHER) 14 ta belgidan iborat bo‘lishi kerak.")
        return personal_number
