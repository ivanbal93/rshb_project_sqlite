from django.shortcuts import render

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.openapi import OpenApiResponse

from .models import Player
from .serializers import PlayerSerializer


# Create your views here.
status_codes = {
    status.HTTP_200_OK: OpenApiResponse(
        response=PlayerSerializer,
        description='ОК'
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        response=None,
        description='Неправильный запрос'
    ),
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=None,
        description='Пользователь не авторизован'
    ),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        response=None,
        description='Доступ запрещён'
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        response=None,
        description='Внутренняя ошибка сервера'
    )
}


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary='Получение списка всех объектов класса "Игрок"',
        tags=['Player'],
        request=PlayerSerializer,
        responses=status_codes
        )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Создание объекта класса "Игрок"',
        tags=['Player'],
        request=PlayerSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=PlayerSerializer,
                description='Создано'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        },
        examples=[
            OpenApiExample(
                name='Пример',
                value={
                    "name": "Vova",
                    "gender": "Male",
                    "own_money": 5000,
                    "credit": 0,
                    "bank": 1,
                    "shop": 1
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary='Получение конкретного объекта класса "Игрок"',
        tags=['Player'],
        responses=status_codes
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary='Обновление информации об объекте класса "Игрок"',
        tags=['Player'],
        responses=status_codes)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @extend_schema(
        summary='Добавление информации к объекту класса "Игрок"',
        tags=['Player'],
        responses=status_codes,
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='Удаление объекта класса "Игрок"',
        tags=['Player'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description='OK'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description='Неправильный запрос'
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=None,
                description='Пользователь не авторизован'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=None,
                description='Доступ запрещён'
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Внутренняя ошибка сервера'
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
