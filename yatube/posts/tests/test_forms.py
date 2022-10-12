from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_author')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test_group',
            description='Тестовая группа',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user,
            pub_date=datetime.today(),
        )

    def test_create_post_form(self):

        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': '',
            'author': self.user,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={
                                               'username': 'test_author'}))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_update_post_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст обновлен',
            'group': '',
            'author': self.user,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.post.refresh_from_db()
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertContains(response, 'Тестовый текст обновлен')
