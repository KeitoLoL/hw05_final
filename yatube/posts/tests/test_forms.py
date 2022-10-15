from django.urls import reverse

from ..models import Post
from .input_data_for_tests import InputDataClass


class PostFormsTests(InputDataClass):

    def test_create_post_form(self):

        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': '',
            'author': self.author,
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
            'author': self.author,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.post.refresh_from_db()
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertContains(response, 'Тестовый текст обновлен')

    def test_create_comment_form(self):
        comment_count = self.post.comments.all().count()
        form_data = {
            'text': 'Тестовый комментарий',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(self.post.comments.all().count(), comment_count + 1)
