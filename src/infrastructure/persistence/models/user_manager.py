from django.contrib.auth.models import BaseUserManager

class SbUserManager(BaseUserManager):

    def create_user(self, whatsapp_number, password=None, **extra_fields):
        if not whatsapp_number:
            raise ValueError("WhatsApp number is required")

        user = self.model(
            whatsapp_number=whatsapp_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, whatsapp_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", True)

        return self.create_user(whatsapp_number, password, **extra_fields)
