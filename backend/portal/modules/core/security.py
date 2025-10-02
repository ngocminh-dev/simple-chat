"""Auth validation"""
from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from okta_jwt.jwt import validate_token
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

from portal.modules.core.config import configs
from portal.modules.postgres import models
from portal.modules.postgres.database import DB
from portal.modules.user.schema import UserBase


class OktaJWTPayload(BaseModel):
    """Okta JWT"""

    sub: str
    uid: str
    profile: Optional[dict[str, Any]]


class OktaJWTBearer(HTTPBearer):
    """OktaJWTBearer"""

    def __init__(
        self,
        auto_error: bool = True,
    ):
        super(OktaJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(OktaJWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )

            try:
                payload = await self.verify_jwt(credentials.credentials)
                res = OktaJWTPayload(
                    sub=payload["sub"],
                    uid=payload["uid"],
                    profile=getattr(payload, "profile", {}),
                )
                return res
            except Exception as cause:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail=f"Invalid authorization code: '{', '.join(cause.args)}'",
                ) from cause

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization code."
        )

    async def verify_jwt(self, token: str):
        """validate auth token"""
        env = configs()
        res = validate_token(
            access_token=token,
            issuer=f"https://{env.OKTA_DOMAIN}/oauth2/default",
            audience="api://default",
            client_ids=env.OKTA_CLIENT_ID,
        )
        return res


# Define the auth scheme and access token URL
auth_scheme = OktaJWTBearer()


async def auth_user(payload: Annotated[OktaJWTPayload, Depends(auth_scheme)], db: DB):
    """load auth user"""
    existing = db.query(models.User).filter(models.User.id == payload.uid).first()
    if not existing:
        existing = models.User(
            id=payload.uid,
            fullname=getattr(payload.profile, "fullname", payload.sub),
            email=payload.sub,
        )
        db.add(existing)
        db.commit()
        db.refresh(existing)
    return existing


AuthUser = Annotated[UserBase, Depends(auth_user)]
