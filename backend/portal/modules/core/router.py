"""Config router"""
from fastapi import APIRouter

from portal.modules.core import config, schema

router = APIRouter(tags=["System"])


@router.get(
    path="/_info", response_model=schema.InfoResponse, summary="Get okta auth configs"
)
async def info(env: config.Env):
    """Handle info"""
    return {"oktaDomain": env.OKTA_DOMAIN, "oktaClientId": env.OKTA_CLIENT_ID}


@router.get(path="/", include_in_schema=False)
async def main():
    """Handle root"""
    return {"Hello": "World"}
