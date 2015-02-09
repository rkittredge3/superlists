from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import List, Item

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        
        self.assertEqual(found.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        
        response = home_page(request)
        expected_html = render_to_string('home.html')
        
        self.assertEqual(response.content.decode(), expected_html)

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(list = correct_list, text = 'itemey 1')
        Item.objects.create(list = correct_list, text = 'itemey 2')

        other_list = List.objects.create()
        Item.objects.create(list = other_list, text = 'other item 1')
        Item.objects.create(list = other_list, text = 'other item 2')

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_passes_correct_list_id_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        response = self.client.post(
            '/lists/new/',
            data = { 'item_text' : 'A new list item' },
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new/',
            data = { 'item_text' : 'A new list item' },
        )

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):

    def test_saving_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        new_item_text = 'A new item for an existing list'

        self.client.post(
            '/lists/%d/add_item/' % (correct_list.id,),
            data = { 'item_text' : new_item_text }
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, correct_list)
        self.assertEqual(new_item.text, new_item_text)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        new_item_text = 'A new item for an existing list'

        response = self.client.post(
            '/lists/%d/add_item/' % (correct_list.id,),
            data = { 'item_text' : new_item_text }
        )
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id),)

class ResetListsTest(TestCase):

    def test_reset_redirects_to_home_page(self):
        response = self.client.post('/lists/reset/')

        self.assertRedirects(response, '/')

    def test_reset_clears_all_existing_items_and_lists(self):
        some_list = List.objects.create()
        another_list = List.objects.create()
        response1 = self.client.post(
            '/lists/%d/add_item/' % (some_list.id,),
            data = { 'item_text' : 'number one item on some list' }
        )
        response2 = self.client.post(
            '/lists/%d/add_item/' % (another_list.id,),
            data = { 'item_text' : 'top item on another list' }
        )
        self.client.post(
            '/lists/reset/'
        )
        
        self.assertEqual(Item.objects.count(), 0, 'Items have not been cleared following reset')
        self.assertEqual(List.objects.count(), 0, 'Lists have not been cleared following reset')
