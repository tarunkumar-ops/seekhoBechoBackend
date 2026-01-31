import boto3
from django.conf import settings


class R2Service:
    """
    Simple wrapper around Cloudflare R2 (S3-compatible) for presigned URLs.
    Does not perform uploads — client uploads directly to R2 using returned URL.
    """

    def __init__(self):
        self._endpoint = getattr(settings, "R2_ENDPOINT_URL", None)
        self._bucket = getattr(settings, "R2_BUCKET", None)
        self._access_key = getattr(settings, "R2_ACCESS_KEY_ID", None)
        self._secret = getattr(settings, "R2_SECRET_ACCESS_KEY", None)
        self._region = getattr(settings, "R2_REGION", "")
        self._public_base = getattr(settings, "R2_PUBLIC_BASE_URL", None)
        self._client = boto3.client(
            "s3",
            endpoint_url=self._endpoint,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret,
            region_name=self._region or None,
        )

    def generate_presigned_put(self, key: str, content_type: str, expires: int = 300) -> str:
        return self._client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self._bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=expires,
        )

    def public_url_for_key(self, key: str) -> str:
        # If a public base is configured (Cloudflare custom domain), use it; otherwise compose from endpoint
        if self._public_base:
            return f"{self._public_base.rstrip('/')}/{key.lstrip('/')}"
        # fallback: best-effort S3-style URL (may not be accurate for R2)
        return f"{self._endpoint.rstrip('/')}/{self._bucket}/{key}"

