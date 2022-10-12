from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.author = User.objects.create_user(username='test_author')
        cls.authorized_client = Client()

        cls.not_author = User.objects.create_user(username='not_author')
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
        self.authorized_client_no_author.force_login(self.not_author)
        self.authorized_client.force_login(self.author)
        #cache.clear()
        #self.authorized_client.force_login(self.user)

    def test_urls(self):
        tested_urls_all = {
            'index.html': '',
            'group_list.html': '/group/test_group/',
            #'profile.html': '/profile/test_author/',
            'post_detail.html': f'/posts/{self.post.pk}/',
        }
        tested_urls_auth = {
            'post_create': '/create/',
            'post_edit': f'/posts/{self.post.pk}/edit/',
        }

        for name, url in tested_urls_all.items():
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'posts/{name}')

            response = self.authorized_client.get(url)
            self.assertEqual(response.status_code, 200)

        for name, url in tested_urls_auth.items():
            response = self.guest_client.get(url)
            self.assertRedirects(response, f'/auth/login/?next={url}')

            response = self.authorized_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'posts/create_post.html')

        response = self.authorized_client_no_author.get(
            f'/posts/{self.post.pk}/edit/')
        self.assertRedirects(response, f'/posts/{self.post.pk}/')
        response = self.authorized_client_no_author.post(
            f'/posts/{self.post.pk}/edit/')
        self.assertRedirects(response, f'/posts/{self.post.pk}/')
