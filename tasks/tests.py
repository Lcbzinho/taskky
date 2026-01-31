from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Project, Task, Tag, Comment


class ModelsTestCase(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(username="tester", password="pass123")
		self.project = Project.objects.create(name="Demo Project", owner=self.user)
		self.tag_bug = Tag.objects.create(name="bug", slug="bug")
		self.tag_ui = Tag.objects.create(name="ui", slug="ui")

	def test_task_creation_and_relations(self):
		task = Task.objects.create(
			title="Fix login",
			description="Resolve login redirect",
			status=Task.STATUS_TODO,
			project=self.project,
			assigned_to=self.user,
			due_date=timezone.now().date(),
		)
		task.tags.add(self.tag_bug, self.tag_ui)

		self.assertEqual(self.project.tasks.count(), 1)
		self.assertEqual(task.tags.count(), 2)
		self.assertIn(task, self.project.tasks.all())
		self.assertEqual(str(task), "Fix login [To Do]")

	def test_queryset_filters(self):
		Task.objects.create(title="A", project=self.project, status=Task.STATUS_TODO)
		Task.objects.create(title="B", project=self.project, status=Task.STATUS_DONE)
		Task.objects.create(title="C", project=self.project, status=Task.STATUS_IN_PROGRESS)

		todos = Task.objects.filter(status=Task.STATUS_TODO)
		done = Task.objects.filter(status=Task.STATUS_DONE)
		in_progress = Task.objects.filter(status=Task.STATUS_IN_PROGRESS)

		self.assertEqual(todos.count(), 1)
		self.assertEqual(done.count(), 1)
		self.assertEqual(in_progress.count(), 1)

	def test_comments(self):
		task = Task.objects.create(title="Write tests", project=self.project)
		Comment.objects.create(task=task, author=self.user, body="Add unit tests")
		Comment.objects.create(task=task, author=None, body="Anonymous feedback")

		self.assertEqual(task.comments.count(), 2)
		self.assertTrue(any("Anonymous" in str(c) for c in task.comments.all()))
