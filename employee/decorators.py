import json
from functools import wraps # Decoratorlar uchun
from django.http import HttpResponseForbidden # 403
from django.shortcuts import render, redirect # Redirect uchun

def role_required(permission): # Ruxsatlarni tekshirish uchun decorator
    def decorator(func): # Decorator
        @wraps(func) # Decoratorlar uchun
        def wrapped(request, *args, **kwargs): # Wrapper
            if not request.user.is_authenticated: # Agar foydalanuvchi tizimga kirgan bo'lmasa
                return render(request, "admin/role.html") # Login sahifasiga yo'naltirish
 
            user_role = getattr(request.user, "role", None) # Foydalanuvchining ruxsati
            if user_role: #
                # Ruxsatlarni JSON formatidan deserializatsiya qilish
                permissions = json.loads(user_role.role.permissions) if isinstance(user_role.role.permissions, str) else user_role.role.permissions
                if not permissions.get(permission, False):
                    return render(request, "admin/role.html")
            else:
                return render(request, "admin/role.html")

            return func(request, *args, **kwargs)
        return wrapped
    return decorator
