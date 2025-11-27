from fastapi import status


class TestAuthContract:
    """Тестирует контракты аутентификации"""

    async def test_register_validation_error(self, async_client, endpoints):
        """Тест валидации данных при регистрации"""

        # Пустой запрос
        response = await async_client.post(endpoints.AUTH_REGISTER, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        # Только email
        response = await async_client.post(endpoints.AUTH_REGISTER, json={"email": "test@example.com"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        # Только password
        response = await async_client.post(endpoints.AUTH_REGISTER, json={"password": "password123"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        # Невалидный email
        response = await async_client.post(endpoints.AUTH_REGISTER, json={
            "email": "invalid-email",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        # Дополнительное поле
        # response = await async_client.post("/api/v1/auth/register", json={
        #     "email": "test@example.com",
        #     "password": "password123",
        #     "error": "error!"
        # })
        # assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
