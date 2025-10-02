from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine

from portal.modules.core.config import Settings, configs


class PGConnection:
    def __init__(self, env: Annotated[Settings, Depends(configs)]) -> None:
        self.engine = create_engine(
            url=f"postgresql://{env.PGUSER}:{env.PGPASSWORD}@{env.PGHOST}/{env.PGDATABASE}",
            connect_args={"check_same_thread": False},
        )
