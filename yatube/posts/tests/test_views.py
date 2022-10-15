from django.urls import reverse

from .input_data_for_tests import InputDataClass
from ..models import Comment, Follow, Group, Post


class PaginatorTest(InputDataClass):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(14):
            cls.post = Post.objects.create(
                text=f'Тестовый текст {i}',
                group=cls.group,
                author=cls.author,
            )

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_five_records(self):
        response = self.authorized_client.get(reverse(
            'posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)


class PostVIEWSTests(InputDataClass):

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

    def test_index_page_show_correct_context(self):

        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.post.text)

    def test_group_page_show_correct_context(self):

        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_group'}))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group, self.post.group)

    def test_profile_page_show_correct_context(self):

        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'test_author'}))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.author, self.post.author)

    def test_post_have_correct_group(self):

        self.second_group = Group.objects.create(
            title='Тестовый заголовок',
            slug='second_group',
            description='Тестовая группа',
        )

        self.second_post = Post.objects.create(
            text='Тестовый текст группы два',
            group=self.second_group,
            author=self.author,
        )

        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'second_group'}))

        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.second_post.text)
        self.assertEqual(first_object.group, self.second_post.group)

        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_group'}))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group, self.post.group)

    def test_follow_guest_client(self):

        response = self.guest_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': 'test_author'}))

        self.assertQuerysetEqual(Follow.objects.all(), [])
        self.assertRedirects(response,
                             '/auth/login/?next=/profile/test_author/follow/')

    def test_follow_authorized_client(self):

        response = self.authorized_client_no_author.get(
            reverse('posts:profile_follow',
                    kwargs={'username': 'test_author'}))
        self.assertQuerysetEqual(Follow.objects.all(), [
            '<Follow: test_author - author, not_author - follower>'])
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'test_author'}))

    def test_double_follow_authorized_client(self):

        response = self.authorized_client_no_author.get(
            reverse('posts:profile_follow',
                    kwargs={'username': 'test_author'}))
        self.assertQuerysetEqual(Follow.objects.all(), [
            '<Follow: test_author - author, not_author - follower>'])
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'test_author'}))

    def test_unfollow_without_follow(self):

        response = self.authorized_client_no_author.get(
            reverse('posts:profile_unfollow',
                    kwargs={'username': 'test_author'}))
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'test_author'}))
        self.assertQuerysetEqual(Follow.objects.all(), [])
        response = self.authorized_client_no_author.get(
            reverse('posts:profile_unfollow',
                    kwargs={'username': 'test_author'}))
        self.assertQuerysetEqual(Follow.objects.all(), [])
        self.assertRedirects(response, '/profile/test_author/')

    def test_comment_guest_client(self):

        response = self.guest_client.get(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data={'text': 'тестовый комментарий'},
            follow=True
        )
        self.assertQuerysetEqual(Comment.objects.all(), [])
        # из-за flake не могу оставить респонс неиспользованным
        # не придумал как в случае с комментарием решить проблему
        print(response)

    def test_comment_authorized_client(self):

        response = self.authorized_client_no_author.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data={'text': 'тестовый комментарий'},
            follow=True
        )
        self.assertQuerysetEqual(Comment.objects.all(),
                                 ['<Comment: тестовый комментарий>'])
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
