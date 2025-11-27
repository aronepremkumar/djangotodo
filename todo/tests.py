from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo

class TodoModelTest(TestCase):
    def test_todo_creation(self):
        todo = Todo.objects.create(title="Test todo", completed=False)
        self.assertEqual(todo.title, "Test todo")
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo.created_at)

    def test_todo_str(self):
        todo = Todo.objects.create(title="Buy milk")
        self.assertEqual(str(todo), "Buy milk")


class TodoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo1 = Todo.objects.create(title="Learn Django", completed=True)
        self.todo2 = Todo.objects.create(title="Write tests")

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Learn Django")
        self.assertContains(response, "Write tests")
        self.assertTemplateUsed(response, 'todo/list.html')

    def test_add_todo_view_get(self):
        response = self.client.get(reverse('add_todo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add.html')

    def test_add_todo_view_post(self):
        response = self.client.post(reverse('add_todo'), {'title': 'New todo from test'})
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(Todo.objects.filter(title='New todo from test').exists())
        # Check it redirects to the list
        self.assertRedirects(response, reverse('todo_list'))
