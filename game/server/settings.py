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

    # If you for some reason change the port, you'll need to also update map.js and
    # client/src/api/backend.ts.
    server_port: int = 1688

    # Disable to allow requests to be made to the backend without an API key.
    require_api_key: bool = True

    # Enable to allow cross-origin requests from http://localhost:3000.
    cors_allow_debug_server: bool = False

    @classmethod
    @lru_cache
    def get(cls) -> ServerSettings:
        return cls()
