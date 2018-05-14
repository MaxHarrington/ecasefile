from django.contrib import admin
from django.db import models
from .models import Case, CaseFile

admin.site.register(Case)
admin.site.register(CaseFile)