from django.test import TestCase, Client
from django.urls import reverse
from .models import BaseSites


class BaseSitesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test object
        cls.site = BaseSites.objects.create(title="Example Site", url_sites="https://example.com/")

    def test_title_label(self):
        site = BaseSites.objects.get(id=self.site.id)
        field_label = site._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_url_sites_label(self):
        site = BaseSites.objects.get(id=self.site.id)
        field_label = site._meta.get_field("url_sites").verbose_name
        self.assertEqual(field_label, "url_sites")

    def test_object_string_representation(self):
        expected_str = f"{self.site.title}"
        self.assertEqual(str(self.site), expected_str)
   


class ShowBaseSitesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two test objects
        cls.site1 = BaseSites.objects.create(title="Site 1", url_sites="https://site1.com/")
        cls.site2 = BaseSites.objects.create(title="Site 2", url_sites="https://site2.com/")

    def setUp(self):
        self.client = Client()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/base-sites/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('show_base_sites'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('show_base_sites'))
        self.assertTemplateUsed(response, 'basesiteapp/showbasesites.html')

