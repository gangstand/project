from datetime import timedelta
from typing import Optional, Union, Sequence, List
from pydantic import BaseModel, field_validator, StrictBool


class LoadConfig(BaseModel):
    authjwt_token_location: Optional[Sequence[str]] = {'headers'}
    authjwt_secret_key: Optional[str] = None
    authjwt_public_key: Optional[str] = None
    authjwt_private_key: Optional[str] = None
    authjwt_algorithm: Optional[str] = "HS256"
    authjwt_decode_algorithms: Optional[List[str]] = None
    authjwt_decode_leeway: Optional[Union[int, timedelta]] = 0
    authjwt_encode_issuer: Optional[str] = None
    authjwt_decode_issuer: Optional[str] = None
    authjwt_decode_audience: Optional[Union[str, Sequence[str]]] = None
    authjwt_denylist_enabled: Optional[StrictBool] = False
    authjwt_denylist_token_checks: Optional[Sequence[str]] = ['access', 'refresh']
    authjwt_header_name: Optional[str] = "Authorization"
    authjwt_header_type: Optional[str] = "Bearer"
    authjwt_access_token_expires: Optional[Union[StrictBool, int, timedelta]] = timedelta(days=1)
    authjwt_refresh_token_expires: Optional[Union[StrictBool, int, timedelta]] = timedelta(days=30)
    # option for create cookies
    authjwt_access_cookie_key: Optional[str] = "access_token_cookie"
    authjwt_refresh_cookie_key: Optional[str] = "refresh_token_cookie"
    authjwt_access_cookie_path: Optional[str] = "/"
    authjwt_refresh_cookie_path: Optional[str] = "/"
    authjwt_cookie_max_age: Optional[int] = None
    authjwt_cookie_domain: Optional[str] = None
    authjwt_cookie_secure: Optional[StrictBool] = False
    authjwt_cookie_samesite: Optional[str] = None
    # option for double submit csrf protection
    authjwt_cookie_csrf_protect: Optional[StrictBool] = True
    authjwt_access_csrf_cookie_key: Optional[str] = "csrf_access_token"
    authjwt_refresh_csrf_cookie_key: Optional[str] = "csrf_refresh_token"
    authjwt_access_csrf_cookie_path: Optional[str] = "/"
    authjwt_refresh_csrf_cookie_path: Optional[str] = "/"
    authjwt_access_csrf_header_name: Optional[str] = "X-CSRF-Token"
    authjwt_refresh_csrf_header_name: Optional[str] = "X-CSRF-Token"
    authjwt_csrf_methods: Optional[Sequence[str]] = ['POST', 'PUT', 'PATCH', 'DELETE']

    @field_validator('authjwt_access_token_expires')
    def validate_access_token_expires(cls, v):
        if v is True:
            raise ValueError("The 'authjwt_access_token_expires' only accepts False (bool) value")
        return v

    @field_validator('authjwt_refresh_token_expires')
    def validate_refresh_token_expires(cls, v):
        if v is True:
            raise ValueError("The 'authjwt_refresh_token_expires' only accept value False (bool)")
        return v

    @field_validator('authjwt_denylist_token_checks')
    def validate_denylist_token_checks(cls, v):
        if v not in ['access', 'refresh']:
            raise ValueError("The 'authjwt_denylist_token_checks' must be between 'access' or 'refresh'")
        return v

    @field_validator('authjwt_token_location')
    def validate_token_location(cls, v):
        if v not in ['headers', 'cookies']:
            raise ValueError("The 'authjwt_token_location' must be between 'headers' or 'cookies'")
        return v

    @field_validator('authjwt_cookie_samesite')
    def validate_cookie_samesite(cls, v):
        if v not in ['strict', 'lax', 'none']:
            raise ValueError("The 'authjwt_cookie_samesite' must be between 'strict', 'lax', 'none'")
        return v

    @field_validator('authjwt_csrf_methods')
    def validate_csrf_methods(cls, v):
        if v.upper() not in {"GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"}:
            raise ValueError("The 'authjwt_csrf_methods' must be between http request methods")
        return v.upper()

    class Config:
        str_min_length = 1
        str_strip_whitespace = True
