from django.test import Client, TestCase


class AboutTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_urls(self):

        tested_urls_all = {
            'author.html': '/about/author/',
            'tech.html': '/about/tech/',
        }

        for name, url in tested_urls_all.items():
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'about/{name}')
