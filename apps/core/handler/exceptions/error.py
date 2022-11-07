from rest_framework import status


class AlreadyExists(Exception):
    status = status.HTTP_409_CONFLICT
    message = '이미 존재하는 데이터가 있습니다.'
