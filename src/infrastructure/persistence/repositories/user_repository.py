from django.contrib.auth import get_user_model
from django.utils import timezone
import secrets

from src.application.ports.auth import UserRepositoryPort
from src.application.dtos.auth_dtos import UserDetailsOutput
from src.infrastructure.persistence.models import SbUserInterestedPlatform, InterestedPlatform


class DjangoUserRepository(UserRepositoryPort):
    def get_or_create_user_id_by_phone(self, *, phone: str) -> int:
        """
        Uses Django's default User model. Stores phone in `username` for simplicity.
        If you later add a custom user model, keep this as the only place that changes.
        """
        User = get_user_model()
        # Use the model's USERNAME_FIELD (may be 'whatsapp_number' for custom user)
        username_field = getattr(User, "USERNAME_FIELD", "username")
        field_names = {f.name for f in User._meta.get_fields()}

        # If identifier looks like an email and the model has an email field, prefer using email.
        is_email = "@" in str(phone)
        if is_email and "email" in field_names:
            lookup = {"email": phone}
            user = User.objects.filter(**lookup).first()
            if user:
                return int(user.id), False

            # Create using email field; set username_field if different and valid length.
            user_code = f"U{int(timezone.now().timestamp())}{secrets.randbelow(10_000):04d}"
            full_name = str(phone).split("@")[0]
            create_kwargs = {"email": phone, "user_code": user_code, "full_name": full_name}

            # If username field exists and is not email, set it to a short placeholder
            if username_field != "email" and username_field in field_names:
                # set a short unique username to avoid length issues
                create_kwargs[username_field] = user_code[:30]

            if "whatsapp_number" in field_names and username_field != "whatsapp_number":
                # do not set whatsapp_number for email identifiers
                pass

            if "status" in field_names:
                create_kwargs["status"] = True

            user = User.objects.create(**create_kwargs)
            return int(user.id), True

        # Otherwise treat as phone identifier
        lookup = {username_field: phone}
        user = User.objects.filter(**lookup).first()
        if user:
            return int(user.id), False

        # Create a minimal user record for phone identifier.
        user_code = f"U{int(timezone.now().timestamp())}{secrets.randbelow(10_000):04d}"
        full_name = str(phone)
        create_kwargs = {username_field: phone, "user_code": user_code, "full_name": full_name}
        if "whatsapp_number" in field_names and username_field != "whatsapp_number":
            create_kwargs["whatsapp_number"] = phone
        if "status" in field_names:
            create_kwargs["status"] = True

        user = User.objects.create(**create_kwargs)
        return int(user.id), True

    def get_user_by_id(self, *, user_id: int) -> dict:
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return {}
        # serialize relevant fields into dict
        data = {
            "id": int(user.id),
            "user_code": getattr(user, "user_code", None),
            "full_name": getattr(user, "full_name", None),
            "whatsapp_number": getattr(user, "whatsapp_number", None),
            "email": getattr(user, "email", None),
            "country_id": getattr(user, "country_id", None),
            "state_id": getattr(user, "state_id", None),
            "city_id": getattr(user, "city_id", None),
            "occupation_id": getattr(user, "occupation_id", None),
            "language_id": getattr(user, "language_id", None),
            "country_name": getattr(user, "country_name", None),
            "state_name": getattr(user, "state_name", None),
            "city_name": getattr(user, "city_name", None),
            "occupation_name": getattr(user, "occupation_name", None),
            "language_name": getattr(user, "language_name", None),
            "budget_to_invest": str(getattr(user, "budget_to_invest", None)),
            "gender": getattr(user, "gender", None),
            "status": getattr(user, "status", None),
        }
        # load interested platforms from mapping table
        plats = (
            SbUserInterestedPlatform.objects.filter(user_id=user_id)
            .select_related("platform")
            .order_by("platform__title")
        )
        data["interested_platforms"] = [
            {"id": int(p.platform.id), "title": p.platform.title} for p in plats
        ]
        return data
        return data

    def update_user(self, *, user_id: int, data: dict) -> dict:
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return {}

        # Validate uniqueness for email and whatsapp_number before updating
        from src.shared.exceptions import ValidationError
        from django.db import IntegrityError

        # If updating email, ensure no other user has the same email
        new_email = data.get("email")
        if new_email:
            exists = User.objects.filter(email=new_email).exclude(pk=user_id).exists()
            if exists:
                raise ValidationError("email already exists")

        # If updating whatsapp_number, ensure uniqueness
        if "whatsapp_number" in data:
            new_whatsapp = data.get("whatsapp_number")
            if new_whatsapp:
                exists = User.objects.filter(whatsapp_number=new_whatsapp).exclude(pk=user_id).exists()
                if exists:
                    raise ValidationError("whatsapp_number already exists")

        # Only allow updating fields that exist on the model
        field_names = {f.name for f in User._meta.get_fields()}
        for k, v in data.items():
            if k in field_names:
                setattr(user, k, v)
        try:
            user.save(update_fields=[k for k in data.keys() if k in field_names])
        except IntegrityError as e:
            # Convert DB integrity errors into a user-friendly validation error
            raise ValidationError("unique constraint violated") from e
        return self.get_user_by_id(user_id=user.id)

    def set_user_interested_platforms(self, *, user_id: int, platform_ids: list[int]) -> None:
        # Replace existing mappings atomically
        from django.db import transaction

        with transaction.atomic():
            SbUserInterestedPlatform.objects.filter(user_id=user_id).delete()
            objs = []
            for pid in platform_ids:
                objs.append(
                    SbUserInterestedPlatform(user_id=user_id, platform_id=pid)
                )
            SbUserInterestedPlatform.objects.bulk_create(objs, ignore_conflicts=True)

