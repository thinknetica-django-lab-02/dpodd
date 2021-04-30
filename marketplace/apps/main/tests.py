from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings

from apps.main.models import Goods, Tag, Category


class GoodsListViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_no_items_in_DB(self):
        """If there is no items in DB, a placeholder should be shown."""
        response = self.client.get(reverse('main:goods-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No items.")

    def test_items_found_by_tag(self):
        """ListView can filter items by tag in query string."""
        tag1 = Tag.objects.create(name="tag_1")
        item1 = Goods.objects.create(
            title="Item #1",
        )
        item1.tags.add(tag1)

        response = self.client.get(reverse('main:goods-list') + f'?tag={tag1.name}' )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item #1")

    def test_items_not_found_by_tag(self):
        """Filter by non-existent tag; a message should be shown."""
        item1 = Goods.objects.create(
            title="Item #1",
        )

        response = self.client.get(reverse('main:goods-list') + '?tag=non_existent_tag')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No items found with tags <strong>[&#x27;non_existent_tag&#x27;]")

    def test_chaining_tags(self):
        """Filter items by multiple tags."""
        tag1 = Tag.objects.create(name="tag_1")
        tag2 = Tag.objects.create(name="tag_2")
        item1 = Goods.objects.create(
            title="Item #1",
        )
        item1.tags.add(tag1, tag2)

        response = self.client.get(reverse('main:goods-list') + f'?tag={tag1.name}&tag={tag2.name}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item #1")


class GoodsDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_item_displayed(self):
        """Test that an item displayed correctly by their URL."""
        item1 = Goods.objects.create(
            title="Item #1",
        )

        response = self.client.get(reverse('main:goods-detail', kwargs={'slug': item1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item #1")


class AddItemOfGoodsViewTests(TestCase):
    """Tests for a view that allow users to add items of goods."""
    def setUp(self):
        self.client = Client()
        # create a group for signals to work correctly
        Group.objects.create(name="common users")
        # create test user
        self.user = get_user_model().objects.create_user(username="TestUser", password="pass")
        # add permissions to test user to access the view
        perm = Permission.objects.get(codename='add_goods')
        self.user.user_permissions.add(perm)
        # add category
        Category.objects.create(name="Cat 1")

    def test_access_for_authenticated_users_only(self):
        """Test that unauthenticated user is redirected to the login page."""
        response = self.client.get(reverse('main:goods-add'))
        self.assertRedirects(response=response,
                             expected_url=reverse('account_login') + '?next=' + reverse('main:goods-add'),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_item_created_successfully(self):
        # authenticate user
        self.client.login(username=self.user.username, password="pass")

        # create an item via POST request
        with open(settings.BASE_DIR / 'static/favicon.ico', 'rb') as test_image:
            response = self.client.post(reverse("main:goods-add"), {'title': 'test item 1', 'price': 100,
                                                                    'image': test_image,
                                                                    'description': 'sadasd',
                                                                    'category': ['1']}, follow=True)

        self.assertRedirects(response=response,
                             expected_url=reverse('main:goods-detail', kwargs={'slug': 'test-item-1'}),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_special_case_user_input(self):
        """Test a special case: user creates an item with a title `add`.
        It should not affect URL dispatcher logic and redirecting should proceed correctly."""

        # authenticate user
        self.client.login(username=self.user.username, password="pass")

        # create an item via POST request
        with open(settings.BASE_DIR / 'static/favicon.ico', 'rb') as test_image:
            response = self.client.post(reverse("main:goods-add"), {'title': 'add', 'price': 100,
                                                                    'image': test_image,
                                                                    'description': 'sadasd',
                                                                    'category': ['1']}, follow=True)

        self.assertRedirects(response=response,
                             expected_url=reverse('main:goods-detail', kwargs={'slug': '_add'}),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

        # create yet another item
        with open(settings.BASE_DIR / 'static/favicon.ico', 'rb') as test_image:
            response = self.client.post(reverse("main:goods-add"), {'title': 'add', 'price': 100,
                                                                    'image': test_image,
                                                                    'description': 'sadasd',
                                                                    'category': ['1']}, follow=True)

        self.assertRedirects(response=response,
                             expected_url=reverse('main:goods-detail', kwargs={'slug': '_add-2'}),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)


class EditItemOfGoodsViewTests(TestCase):
    """Tests for a view that allow users to edit items of goods."""
    def setUp(self):
        self.client = Client()
        # create a group for signals to work correctly
        Group.objects.create(name="common users")
        # create test user
        self.user = get_user_model().objects.create_user(username="TestUser", password="pass")
        # add permissions to test user to access the view
        perm = Permission.objects.get(codename='change_goods')
        self.user.user_permissions.add(perm)
        # add category
        Category.objects.create(name="Cat 1")
        # add test item
        self.item = Goods.objects.create(title="Item #1", seller=self.user)

    def test_anonymous_user_get_redirected_2_detail_view(self):
        """Test that unregistered users get redirected to the detail view."""
        response = self.client.get(reverse('main:goods-edit', kwargs={'slug': self.item.slug}))
        self.assertRedirects(response=response,
                             expected_url=reverse('main:goods-detail', kwargs={'slug': self.item.slug}),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_not_owner_redirected_2_detail_view(self):
        """Test that registered users get redirected to the detail view if they're not the owner."""
        user2 = get_user_model().objects.create_user(username="TestUser2", password="passw")
        self.client.force_login(user2)

        response = self.client.get(reverse('main:goods-edit', kwargs={'slug': self.item.slug}))
        self.assertRedirects(response=response,
                             expected_url=reverse('main:goods-detail', kwargs={'slug': self.item.slug}),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_owner_has_access(self):
        """Test that owner has access."""
        self.client.force_login(self.user)

        response = self.client.get(reverse('main:goods-edit', kwargs={'slug': self.item.slug}))
        self.assertEqual(response.status_code, 200)
