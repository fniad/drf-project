""" Пагинаторы приложения training_courses """
from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    """ Пагинатор для вывода курсов """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class LessonPagination(PageNumberPagination):
    """ Пагинатор для вывода уроков """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class SubscriptionPagination(PageNumberPagination):
    """ Пагинатор для вывода подписок """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
