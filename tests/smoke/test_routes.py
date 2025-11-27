import pytest


async def test_hello_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.smoke
class TestAuthEndpointResponses:
    """Тесты структуры ответов эндпоинтов аутентификации"""

    async def test_auth_endpoints_respond(self, async_client, endpoints):
        """Проверяем что эндпоинты отвечают"""
        api_endpoints = [
            ("POST", endpoints.AUTH_REGISTER),
            ("GET", endpoints.AUTH_REGISTER_CONFIRM),
            ("POST", endpoints.AUTH_LOGIN),
            ("GET", endpoints.AUTH_LOGOUT),
            ("GET", endpoints.AUTH_GET_USER),
        ]

        for method, endpoint in api_endpoints:
            if method == "GET":
                response = await async_client.get(endpoint)
            else:
                response = await async_client.post(endpoint, json={})

            # Главное - не 5xx и не 404
            assert response.status_code != 500, f"{endpoint} returns 500"
            assert response.status_code != 404, f"{endpoint} returns 404"
