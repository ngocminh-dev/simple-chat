from fastapi import APIRouter, Path

router = APIRouter(tags=["Data"])


class Payload:
    query: str


class Response:
    result: str


# @router.post(path="/select-attributes/{sessionId}")
# async def select_attributes(payload: AttrPayload, authUser: AuthUser, sessionId=Path()):
#     """return select attributes"""
#     return {result}


@router.post(path="/data")
async def data():
    """return data"""

    return
L