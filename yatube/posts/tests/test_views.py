from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse


from ..models import Group, Post

User = get_user_model()


class PostVIEWSTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_author')
        cls.authorized_client = Client()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test_group',
            description='Тестовая группа',
        )

        for i in range(15):
            cls.post = Post.objects.create(
                text=f'Тестовый текст {i}',
                group=cls.group,
                author=cls.user,
                pub_date=datetime.today(),
            )

    def setUp(self):
        # Создаем авторизованный клиент
        cache.clear()
        self.authorized_client.force_login(self.user)

    def test_views_template(self):

        tested_urls_all = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'test_group'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'test_author'}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}),
            'posts/create_post.html': reverse('posts:post_create'),

        }

        for html, name in tested_urls_all.items():
            response = self.authorized_client.get(name)
            self.assertTemplateUsed(response, html)

        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}),)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_five_records(self):
        response = self.authorized_client.get(reverse(
            'posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)
