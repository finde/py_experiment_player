from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from typing import Any, Dict, List, Optional, Union
from fastapi.templating import Jinja2Templates

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Stress and Addiction"
    SENTRY_DSN: Optional[HttpUrl] = None
    
    EXP_ROOT_DIR = "experiments"
    EXP_OUTPUT_DIR = "results"
    EXP_TEMPLATE_DIR = "templates"
    EXP_ASSETS_DIR = "assets"

    TEMPLATES = Jinja2Templates(directory="dist")

    class Config:
        case_sensitive = True


settings = Settings()