
from django.test import TestCase, SimpleTestCase
import datetime
from django.utils import timezone
from .models import Post, PartyTestimonial, Status
from django.urls import reverse


class SimpleUrlTest(TestCase):
    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class PostModelTests(TestCase):

    def test_was_published_recently_with_future_post(self):

        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(create_at=time)
        self.assertIs(future_post.was_published_recently(), False)


class TestimonialModelTests(TestCase):
    def test_rating_greater_than_five(self):
        """
        If rating greater than 5, an appropriate message is displayed.
        """
        rate_five_testimonial = PartyTestimonial(rating=5)
        self.assertIs(rate_five_testimonial.was_rated_more_than_five(), False)


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)


class UserListPageTests(TestCase):

    def test_user_page_status_code(self):
        response = self.client.get('/users/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('user-list'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'politricks/userList.html')

    def test_users_page_contains_correct_html(self):
        response = self.client.get('/users/')
        self.assertContains(response, '<h2>User List</h2>')


class StatusFixtureTest(TestCase):
    fixtures = ["status.json"]

    def test_should_create_post(self):
        status = Status.objects.get(pk=1)
        self.assertEqual(status.label, "Active")
