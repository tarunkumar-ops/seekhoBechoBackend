# OTP Authentication Code Flow

This document traces the complete code flow for WhatsApp OTP authentication, following Clean Architecture principles.

---

## Architecture Layers

```
┌─────────────────────────────────────────┐
│  Interfaces (API Layer)                 │  ← HTTP entry point
├─────────────────────────────────────────┤
│  Application (Use Cases)                 │  ← Business orchestration
├─────────────────────────────────────────┤
│  Domain (Business Logic)                 │  ← Pure Python, no frameworks
├─────────────────────────────────────────┤
│  Infrastructure (Technical Details)      │  ← Django ORM, Twilio, JWT
└─────────────────────────────────────────┘
```

**Dependency Rule**: Inner layers never import outer layers.

---

## Flow 1: Request OTP (`POST /api/auth/request-otp/`)

### Step-by-Step Flow

```
1. HTTP Request
   ↓
2. config/urls.py
   → Routes to: path("api/", include("src.interfaces.api.urls"))
   ↓
3. src/interfaces/api/urls.py
   → Routes to: path("auth/request-otp/", RequestOtpView.as_view())
   ↓
4. src/interfaces/api/auth_views.py :: RequestOtpView.post()
   ├─ Validates HTTP input via RequestOtpSerializer
   ├─ Converts to DTO: RequestOtpInput(phone="+919818445669")
   ├─ Gets container: get_container()
   └─ Calls: container.request_login_otp().execute(input_dto)
   ↓
5. src/container.py :: Container.request_login_otp()
   ├─ Creates use case with dependencies:
   │  ├─ otp_repo: DjangoLoginOtpRepository (infrastructure)
   │  └─ otp_sender: TwilioWhatsAppOtpSender or DevLoggingWhatsAppOtpSender
   └─ Returns: RequestLoginOtpUseCase instance
   ↓
6. src/application/use_cases/request_login_otp.py :: RequestLoginOtpUseCase.execute()
   ├─ Normalizes phone: normalize_e164("+919818445669")
   │  └─ src/domain/value_objects/phone.py :: normalize_e164()
   │     └─ Validates E.164 format, raises ValidationError if invalid
   ├─ Generates 6-digit code: secrets.randbelow(1_000_000) → "405083"
   ├─ Saves OTP to DB: otp_repo.create_login_otp(phone, code, ttl=300)
   │  └─ src/infrastructure/persistence/repositories/otp_repository.py
   │     ├─ Hashes code: HMAC-SHA256(code, secret)
   │     ├─ Creates LoginOtp model:
   │     │  └─ phone, code_hash, expires_at (now + 5min), attempts=0
   │     └─ Saves via Django ORM: LoginOtp.objects.create(...)
   └─ Sends WhatsApp: otp_sender.send_whatsapp_otp(phone, code)
      └─ src/infrastructure/messaging/whatsapp_sender.py
         ├─ If TWILIO_ENABLED=1:
         │  └─ TwilioWhatsAppOtpSender.send_whatsapp_otp()
         │     └─ Calls Twilio API: client.messages.create(
         │        from_="whatsapp:+14155238886",
         │        to="whatsapp:+919818445669",
         │        body="Your login code is: 405083"
         │     )
         └─ Else (dev mode):
            └─ DevLoggingWhatsAppOtpSender.send_whatsapp_otp()
               └─ Logs: "DEV OTP for +919818445669 is 405083"
   ↓
7. Response
   └─ HTTP 200: {"detail": "otp_sent"}
```

### Key Files

| Layer | File | Responsibility |
|-------|------|----------------|
| **Interfaces** | `src/interfaces/api/auth_views.py` | Thin HTTP handler, converts HTTP ↔ DTO |
| **Interfaces** | `src/interfaces/api/auth_serializers.py` | DRF validation (phone format) |
| **Application** | `src/application/use_cases/request_login_otp.py` | Orchestrates: normalize → generate → save → send |
| **Application** | `src/application/ports/otp.py` | Interfaces: `OtpRepositoryPort`, `OtpSenderPort` |
| **Domain** | `src/domain/value_objects/phone.py` | Pure Python phone validation (E.164) |
| **Infrastructure** | `src/infrastructure/persistence/repositories/otp_repository.py` | Django ORM: saves hashed OTP |
| **Infrastructure** | `src/infrastructure/messaging/whatsapp_sender.py` | Twilio SDK: sends WhatsApp message |
| **Infrastructure** | `src/infrastructure/persistence/models/login_otp.py` | Django model: `LoginOtp` table |
| **Wiring** | `src/container.py` | Dependency injection: wires ports → implementations |

---

## Flow 2: Verify OTP (`POST /api/auth/verify-otp/`)

### Step-by-Step Flow

```
1. HTTP Request
   Body: {"phone": "+919818445669", "code": "405083"}
   ↓
2. config/urls.py → src/interfaces/api/urls.py
   → Routes to: path("auth/verify-otp/", VerifyOtpView.as_view())
   ↓
3. src/interfaces/api/auth_views.py :: VerifyOtpView.post()
   ├─ Validates HTTP input via VerifyOtpSerializer
   ├─ Converts to DTO: VerifyOtpInput(phone="+919818445669", code="405083")
   ├─ Gets container: get_container()
   └─ Calls: container.verify_login_otp().execute(input_dto)
   ↓
4. src/container.py :: Container.verify_login_otp()
   ├─ Creates use case with dependencies:
   │  ├─ otp_repo: DjangoLoginOtpRepository
   │  ├─ user_repo: DjangoUserRepository
   │  └─ token_provider: SimpleJwtTokenProvider
   └─ Returns: VerifyLoginOtpUseCase instance
   ↓
5. src/application/use_cases/verify_login_otp.py :: VerifyLoginOtpUseCase.execute()
   ├─ Normalizes phone: normalize_e164("+919818445669")
   ├─ Validates code format: must be 6 digits
   │  └─ Raises ValidationError if invalid
   ├─ Verifies OTP: otp_repo.verify_and_consume(phone, code, max_attempts=5)
   │  └─ src/infrastructure/persistence/repositories/otp_repository.py
   │     ├─ Finds latest active OTP for phone (not expired, not consumed)
   │     ├─ Checks attempts < max_attempts (5)
   │     ├─ Increments attempts counter
   │     ├─ Compares: HMAC-SHA256(code) == stored code_hash
   │     ├─ If match:
   │     │  ├─ Marks consumed: consumed_at = now
   │     │  └─ Returns True
   │     └─ If no match:
   │        └─ Returns False (code saved, attempts incremented)
   ├─ If verification fails:
   │  └─ Raises AuthError("invalid or expired code")
   ├─ Gets or creates user: user_repo.get_or_create_user_id_by_phone(phone)
   │  └─ src/infrastructure/persistence/repositories/user_repository.py
   │     ├─ Looks up Django User by phone (custom field or username)
   │     ├─ If not found: creates new User(username=phone)
   │     └─ Returns user.id (str)
   └─ Issues JWT tokens: token_provider.issue_tokens_for_user_id(user_id)
      └─ src/infrastructure/auth/jwt_provider.py :: SimpleJwtTokenProvider
         ├─ Loads Django User: User.objects.get(id=user_id)
         ├─ Creates access token: RefreshToken.for_user(user).access_token
         ├─ Creates refresh token: RefreshToken.for_user(user)
         └─ Returns: TokenPair(access="...", refresh="...")
   ↓
6. Response
   └─ HTTP 200: {"access": "eyJ...", "refresh": "eyJ..."}
   └─ Or HTTP 401: {"detail": "invalid or expired code"}
```

### Key Files

| Layer | File | Responsibility |
|-------|------|----------------|
| **Interfaces** | `src/interfaces/api/auth_views.py` | HTTP handler, converts HTTP ↔ DTO, handles exceptions |
| **Interfaces** | `src/interfaces/api/auth_serializers.py` | DRF validation (phone, code) |
| **Application** | `src/application/use_cases/verify_login_otp.py` | Orchestrates: validate → verify → get user → issue tokens |
| **Application** | `src/application/ports/auth.py` | Interfaces: `TokenProviderPort`, `UserRepositoryPort` |
| **Application** | `src/application/dtos/auth_dtos.py` | DTOs: `VerifyOtpInput`, `VerifyOtpOutput` |
| **Domain** | `src/domain/value_objects/phone.py` | Phone normalization |
| **Infrastructure** | `src/infrastructure/persistence/repositories/otp_repository.py` | Atomic OTP verification with attempt tracking |
| **Infrastructure** | `src/infrastructure/persistence/repositories/user_repository.py` | Django User lookup/create |
| **Infrastructure** | `src/infrastructure/auth/jwt_provider.py` | SimpleJWT: issues access + refresh tokens |
| **Wiring** | `src/container.py` | Dependency injection |

---

## Exception Handling Flow

### ValidationError (400 Bad Request)
- **Raised by**: Domain (`normalize_e164`), Application (code format check)
- **Caught by**: `RequestOtpView`, `VerifyOtpView`
- **Response**: `HTTP 400: {"detail": "error message"}`

### AuthError (401 Unauthorized)
- **Raised by**: Application (`VerifyLoginOtpUseCase` when OTP invalid/expired)
- **Caught by**: `VerifyOtpView`
- **Response**: `HTTP 401: {"detail": "invalid or expired code"}`

---

## Database Schema

### LoginOtp Model
```python
class LoginOtp(models.Model):
    phone = CharField(max_length=20)           # E.164 format
    code_hash = CharField(max_length=64)       # HMAC-SHA256 hash
    created_at = DateTimeField(auto_now_add)
    expires_at = DateTimeField()               # created_at + 5 minutes
    attempts = IntegerField(default=0)         # Verification attempts
    consumed_at = DateTimeField(null=True)     # Set when verified
```

**Indexes**: `(phone, expires_at, consumed_at)` for fast lookups.

---

## Security Features

1. **OTP Hashing**: Codes stored as HMAC-SHA256 hashes (not plaintext)
2. **TTL**: OTPs expire after 5 minutes
3. **Attempt Limiting**: Max 5 verification attempts per OTP
4. **Atomic Verification**: Database transaction prevents race conditions
5. **One-Time Use**: OTP marked `consumed_at` after successful verification
6. **JWT Tokens**: Access token (30min) + Refresh token (7 days)

---

## Dependency Injection (Container Pattern)

**`src/container.py`** is the **composition root**:
- Only place that instantiates infrastructure classes
- Wires ports (interfaces) to implementations
- Views call `get_container()` to get use cases
- Follows **Dependency Inversion Principle**

**Example**:
```python
# View never creates infrastructure directly
use_case = get_container().request_login_otp()  # ✅
# Not: use_case = RequestLoginOtpUseCase(otp_repo=DjangoLoginOtpRepository(...))  # ❌
```

---

## Testing Flow

**Test File**: `src/tests/test_otp_auth_flow.py`

1. **Request OTP**: `POST /api/auth/request-otp/` with phone
2. **Verify OTP**: `POST /api/auth/verify-otp/` with phone + code
3. **Assert**: Response contains `access` and `refresh` JWT tokens

**Note**: In tests, `TWILIO_ENABLED=0` uses `DevLoggingWhatsAppOtpSender` (no external calls).

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `TWILIO_ENABLED` | Enable/disable Twilio | `1` or `0` |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | `AC...` |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | `...` |
| `TWILIO_WHATSAPP_FROM` | WhatsApp sender number | `+14155238886` |
| `OTP_SECRET` | HMAC secret for OTP hashing | `your-secret-key` |

---

## Summary

**Request OTP Flow**:
```
HTTP → View → Serializer → Use Case → Domain (normalize) → Infrastructure (save + send)
```

**Verify OTP Flow**:
```
HTTP → View → Serializer → Use Case → Infrastructure (verify) → Infrastructure (user) → Infrastructure (JWT) → Response
```

**Key Principle**: Each layer only knows about the layer directly below it. Infrastructure never imports Domain, Application never imports Infrastructure directly (only via ports).
