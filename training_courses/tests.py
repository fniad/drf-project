""" Тесты для приложения training_courses """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from training_courses.models import Course, Lesson, Subscription
from users.models import User, UserRoles


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='test',
            role=UserRoles.MEMBER)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name_course='тест',
            description_course='тест',
            owner=self.user
        )

    def test_get_course_list(self):
        """ Тест получение списка курсов """
        response = self.client.get(
            '/courses/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK, )

        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {
                     'lessons_count': 0,
                     'name_course': self.course.name_course,
                     'subscription': "не подписан"
                 }
             ]
             }
        )

    def test_course_create(self):
        """ Тест создание курса """

        data = {
            'name_course': 'тест',
            'description_course': 'тест',
        }

        response = self.client.post(
            '/courses/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Course.objects.all().count(),
            2
        )

    def test_course_retrieve(self):
        """ Тест получение курса """

        response = self.client.get(
            f'/courses/{self.course.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.course.id,
                "lesson_in_this_course": [],
                "name_course": self.course.name_course,
                "preview_img_course": None,
                "description_course": self.course.description_course,
                "owner": self.user.id
            }
        )

    def test_course_update_patch(self):
        """ Тест обновление курса (изменение одного поля) """

        data = {
            'name_course': 'тест1'
        }

        response = self.client.patch(
            f'/courses/{self.course.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_update_put(self):
        """ Тест полного замещения курса, изменение всех полей """

        data = {
            "name_course": "тест2",
            "description_course": "тест test2",
        }
        response = self.client.put(
            f'/courses/{self.course.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_delete(self):
        """ Тест удаления курса """

        response = self.client.delete(
            f'/courses/{self.course.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()


class LessonTestCase(APITestCase):
    """ Тест класса Lesson """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='test',
            role=UserRoles.MEMBER)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name_course='тест',
            description_course='тест',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name_lesson='тест',
            description_lesson='тест',
            owner=self.user,
            course=self.course
        )

    def test_lesson_list(self):
        """ Тест получение списка уроков """

        response = self.client.get(
            reverse('courses:list-lessons'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name_lesson": self.lesson.name_lesson,
                        "subscription": "не подписан"
                    },
                ]
            }
        )

    def test_lesson_create(self):
        """ Тест создания урока """

        data = {
            "name_lesson": "тест",
            "description_lesson": "тест"
        }

        response = self.client.post(
            reverse('courses:create-lessons'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_retrieve(self):
        """ Тест получение урока """

        response = self.client.get(
            reverse('courses:view-lesson', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "name_lesson": self.lesson.name_lesson,
                "description_lesson": self.lesson.description_lesson,
                "preview_img_lesson": self.lesson.preview_img_lesson,
                "video_url_lesson": self.lesson.video_url_lesson,
                "course": self.course.id,
                "owner": self.user.id
            }
        )

    def test_lesson_update_patch(self):
        """ Тест обновление урока (изменение одного поля) """

        data = {
            "name_lesson": "тест1"
        }

        response = self.client.patch(
            reverse('courses:update-lessons', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update_url_is_valid(self):
        """ Тест обновление url урока (проверка на валидность ссылки проходит)"""

        data = {
            "video_url_lesson": "https://www.youtube.com/watch?v=ChEdFh7Q-Vw&pp=ygUDb29w"
        }

        response = self.client.patch(
            reverse('courses:update-lessons', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update_url_not_is_valid(self):
        """ Тест обновление url урока (проверка на валидность ссылки не проходит)"""

        data = {
            "video_url_lesson": "https://www.outub.com/watch?v=ChEdFh7Q-Vw&pp=ygUDb29w"
        }

        response = self.client.patch(
            reverse('courses:update-lessons', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


    def test_lesson_update_description_is_valid(self):
        """ Тест обновление описания урока (проверка на валидность ссылки проходит)"""

        data = {
            "description_lesson": "www.youtube.com"
        }

        response = self.client.patch(
            reverse('courses:update-lessons', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update_description_is_not_valid(self):
        """ Тест обновление описания урока (проверка на валидность ссылки не проходит)"""

        data = {
            "description_lesson": "www.outub.com"
        }

        response = self.client.patch(
            reverse('courses:update-lessons', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_lesson_update_put(self):
        """ Тест полного замещения урока, изменение всех полей """

        data = {
            "name_lesson": "тест",
            "description_lesson": "Тест https://www.youtube.com/watch?v=ChEdFh7Q-Vw&pp=ygUDb29w",
            "video_url_lesson": "https://www.youtube.com/watch?v=ChEdFh7Q-Vw&pp=ygUDb29w",
            "course": self.course.id,
            "owner": self.user.id
        }

        response = self.client.put(
            reverse('courses:update-lessons', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        """ Тест удаление курса """
        response = self.client.delete(
            reverse('courses:delete-lessons', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Lesson.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()


class SubscriptionTestCase(APITestCase):
    """ Тест класса подписки """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='test',
            role=UserRoles.MEMBER)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name_course='тест',
            description_course='тест',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name_lesson='тест',
            description_lesson='тест',
            owner=self.user,
            course=self.course
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            lesson=None,
            is_active=False
        )

    def test_subscription_list(self):
        """Тест получение списка подписок"""
        response = self.client.get(
            '/subscription/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.subscription.id,
                        "is_active": self.subscription.is_active,
                        "user": self.user.id,
                        "course": self.course.id,
                        "lesson": None
                    },
                ]
            }
        )

    def test_subscription_create_for_lesson(self):
        """ Тест создание подписки на урок"""
        data = {
            "user": self.user.id,
            "lesson": self.lesson.id
        }
        response = self.client.post(
            '/subscription/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            2
        )

    def test_subscription_create_for_course(self):
        """ Тест создание подписки на курс"""
        data = {
            "user": self.user.id,
            "course": self.course.id
        }
        response = self.client.post(
            '/subscription/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            2
        )

    def test_subscription_update(self):
        """ Тест активации или деактивации подписки """
        data = {
            "is_active": True
        }
        response = self.client.patch(
            f'/subscription/{self.subscription.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_subscription_delete(self):
        """ Тест удаления подписки """
        response = self.client.delete(
            f'/subscription/{self.subscription.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Subscription.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()
