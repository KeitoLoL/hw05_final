from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class InputDataClass(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='test_author')
        cls.not_author = User.objects.create_user(username='not_author')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client_no_author = Client()

        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test_group',
            description='Тестовая группа',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.author,
            pub_date=datetime.today(),
        )

    def setUp(self):
        # Создаем авторизованный клиент
        cache.clear()
        self.authorized_client.force_login(self.author)
        self.authorized_client_no_author.force_login(self.not_author)
