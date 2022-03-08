from __future__ import annotations

from functools import lru_cache

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    """Settings controlling server behavior.

    The values listed here will be automatically modified based on the environment. e.g.
    running with SERVER_BIND_ADDRESS=0.0.0.0 will cause the server to bind to all
    interfaces.

    https://fastapi.tiangolo.com/advanced/settings
    """

    # WARNING: Be extremely cautious exposing the server to other machines. As there is
    # no client/server workflow yet, security has not been a focus.
    server_bind_address: str = "::1"

    # This (and the address) will be passed the the front end as a query parameter.
    server_port: int = 16880

    # Enable to allow cross-origin requests from http://localhost:3000.
    cors_allow_debug_server: bool = False

    class Config:
        env_file = "serverconfig.env"

    @classmethod
    @lru_cache
    def get(cls) -> ServerSettings:
        return cls()
