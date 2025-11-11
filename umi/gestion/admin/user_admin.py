from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _ 
from umi.gestion.models.user import CustomUser, Role

class CustomUserCreationForm(forms.ModelForm):
    """
    Formulario para crear nuevos usuarios desde el admin.
    Permite asignar rol, contraseña y estado.
    """
    password1 = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirmar Contraseña"), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "role", "is_staff", "is_active")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Las contraseñas no coinciden"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario para editar usuarios existentes.
    """
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role", "is_active", "is_staff", "is_superuser")

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Permisos"), {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Fechas importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)