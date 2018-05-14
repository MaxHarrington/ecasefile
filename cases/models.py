from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def user_directory_path(instance, filename):
	return 'user{0}/{1}'.format(instance.author, filename)

def validate_file_extension(value):
    if not value.name.endswith('.docx'):
        raise ValidationError(u'Only .docx files can be uploaded.')

class CaseManager(models.Manager):
	def create_case(self, title, text, user):
		case = self.create(title=title, text=text, author=user)
		return case

class Case(models.Model):
	title = models.CharField(max_length=100)
	time_posted = models.DateTimeField(auto_now=False, auto_now_add=True)
	text = models.CharField(max_length=4000)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100)
	description = ""

	objects = CaseManager()

	def __str__(self):
		return self.title

class CaseFileManager(models.Manager):
	def create_casefile(self, title, cases, user):
		casefile = self.create(title=title, author=user)
		return casefile

	def add_case(self, case):
		self.add(case)

class CaseFile(models.Model):
	title = models.CharField(max_length=100)
	time_posted = models.DateTimeField(auto_now=False, auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	cases = models.ManyToManyField(Case)
	description = models.CharField(max_length=150)
	description = ""

	objects = CaseFileManager()

	def __str__(self):
		return self.title

class RawFileManager(models.Manager):
	def upload_file(self, title, file, user):
		raw_file = self.create(title=title, file=file, author=user)
		return raw_file

class RawFile(models.Model):
	file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
	title = models.CharField(max_length=100)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	objects = RawFileManager()

	def __str__(self):
		return self.title
