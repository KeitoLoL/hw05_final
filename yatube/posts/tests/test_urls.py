from .input_data_for_tests import InputDataClass


class PostURLTests(InputDataClass):

    def test_urls_not_auth(self):
        tested_urls_all = {
            'index.html': '',
            'group_list.html': '/group/test_group/',
            'profile.html': '/profile/test_author/',
            'post_detail.html': f'/posts/{self.post.pk}/',
        }

        for name, url in tested_urls_all.items():
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'posts/{name}')

            response = self.authorized_client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_urls_auth(self):

        tested_urls_auth = {
            'create_post.html': '/create/',
            'create_post.html': f'/posts/{self.post.pk}/edit/',
            'follow.html': '/follow/',
        }

        for name, url in tested_urls_auth.items():
            response = self.guest_client.get(url)
            self.assertRedirects(response, f'/auth/login/?next={url}')
            response = self.authorized_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'posts/{name}')

        response = self.authorized_client_no_author.get(
            f'/posts/{self.post.pk}/edit/')
        self.assertRedirects(response, f'/posts/{self.post.pk}/')

        response = self.authorized_client_no_author.post(
            f'/posts/{self.post.pk}/edit/')
        self.assertRedirects(response, f'/posts/{self.post.pk}/')

        response = self.authorized_client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
