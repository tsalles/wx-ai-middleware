from fastapi import FastAPI
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from app.routes import router


app = FastAPI(title="Text Generation API", description="A watsonx.Runtime based microservice for text generation.")
app.include_router(router, prefix='/api/v1')

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.0"

    openapi_schema["info"]["x-ibm-application-id"]: str = "watsonx.ai-text-gen"
    openapi_schema["info"]["x-ibm-application-name"]: str = "Text Generation API"
    openapi_schema["info"]["x-ibm-skill-type"]: str = "imported"
    openapi_schema["info"]["x-ibm-skill-subtype"]: str = "public"


    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["ApiKeyAuth"] = {
        "type": "apiKey",
        "in": "header",
        "name": "x-api-key",
    }

    openapi_schema["security"] = [{"ApiKeyAuth": []}]

    openapi_schema["servers"] = [
        {
            "url": "https://{hostname}:{port}",
            "variables": {
                "hostname": {
                    "default": "0.0.0.0",
                    "description": "Service hostname"
                },
                "port": {
                    "default": "8000",
                    "description": "Service port"
                }
            }
        }
    ]

    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

@app.get("/openapi.json", include_in_schema=False)
def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title=app.title, version="1.0.0", routes=app.routes)

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title=app.title)

