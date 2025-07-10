import enum


class HTTPStatus(enum.auto):
    HTTP_200_OK: int = 200
    HTTP_201_CREATED: int = 201
    HTTP_400_BAD_REQUEST: int = 400
    HTTP_500_SERVER_ERROR: int = 500
