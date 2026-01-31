from django.conf import settings
from django.db import models


class Tag(models.Model):
	name = models.CharField(max_length=64, unique=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name


class Project(models.Model):
	name = models.CharField(max_length=128)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="projects",
	)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Task(models.Model):
	STATUS_TODO = "todo"
	STATUS_IN_PROGRESS = "in_progress"
	STATUS_DONE = "done"
	STATUS_CHOICES = [
		(STATUS_TODO, "To Do"),
		(STATUS_IN_PROGRESS, "In Progress"),
		(STATUS_DONE, "Done"),
	]

	title = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
	due_date = models.DateField(null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
	assigned_to = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="assigned_tasks",
	)
	tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.title} [{self.get_status_display()}]"


class Comment(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="task_comments",
	)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Comment by {self.author or 'Anonymous'} on {self.task.title}"
