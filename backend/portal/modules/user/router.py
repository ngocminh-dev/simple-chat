"""User router"""
from fastapi import APIRouter, Depends

from portal.modules.core.security import AuthUser, auth_scheme
from portal.modules.user import schema

router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(auth_scheme)],
)


@router.get(path="/me", response_model=schema.User)
def me(user: AuthUser):
    """return me"""
    return user
