from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect

from math import ceil

from .forms import TextForm, CasefileForm, UploadCase, AddCasesForm
from .models import Case, CaseFile, RawFile
from .permissions import check_ownership, check_casefile_ownership, owned_cases, owned_casefiles
from .searchtools import basic_search 
from .imports import convert_docx

def index(request):

	context = {
	}

	return render(request, 'cases/index.html', context)

# shows the user a singular case via its case id
# offers the option to edit the case
def case(request, case_id):
	specific_case = Case.objects.get(pk=case_id)
	can_edit = check_ownership(request, case_id)
		
	context = {
	'specific_case': specific_case,
	'can_edit': can_edit,
	}

	return render(request, 'cases/case.html', context)

def casefile(request, casefile_id):
	specific_casefile = CaseFile.objects.get(pk=casefile_id)

	context = {
		'specific_casefile': specific_casefile,
	}

	return render(request, 'cases/casefile.html', context)

# basic search function of site, displays cases matching query
# replaces %20 (the stand-in for a space in a url) with an actual space
# for the database query to avoid querying the database with nonsense
def search(request, search_term, page_number):
	users_casefiles = owned_casefiles(request)
	context = basic_search(search_term, page_number)
	context['users_casefiles'] = users_casefiles

	if request.method == 'POST':
		form = AddCasesForm(request.POST)
		if form.is_valid():
			casefile = CaseFile.objects.get(title=form.cleaned_data['title'])
			for cases in form.cleaned_data['cases']:
				casefile.cases.add(cases.id)

			return redirect('search', search_term=search_term, page_number=page_number)
	else:
		form = AddCasesForm()
		context['form'] = form

	return render(request, 'cases/display_cases.html', context)

# shows the currently logged-in user all of their cases
# displays them ten pages at a time - eventually will add ability to 
# have the user set how many results per page they want globally
@login_required
def my_cases(request, page_number):
	results_per_page = 20
	users_cases = owned_cases(request)
	users_casefiles = owned_casefiles(request)
	number_of_cases = len(users_cases)
	number_of_pages = ceil(number_of_cases / results_per_page)

	if page_number != 0:
		result_number = page_number * results_per_page
		lower_bound_results = (page_number - 1) * results_per_page
	else:
		result_number = results_per_page

	next_page = page_number + 1
	previous_page = page_number - 1

	if request.method == 'POST':
		form = AddCasesForm(request.POST)
		if form.is_valid():
			casefile = CaseFile.objects.get(title=form.cleaned_data['title'])
			for cases in form.cleaned_data['cases']:
				casefile.cases.add(cases.id)

			return redirect('my_cases', page_number=page_number)
	else:
		form = AddCasesForm()

	context = {
		'latest_cases': users_cases[lower_bound_results:result_number],
		'total_pages': number_of_pages,
		'current_page': page_number,
		'next_page': next_page,
		'previous_page': previous_page,
		'users_casefiles': users_casefiles,
		'form': form,
	}

	return render(request, 'cases/display_cases.html', context)

# shows a list of all the user's owned casefiles
# contains link to allow user to add details to or edit fields
@login_required
def my_casefiles(request):
	users_casefiles = owned_casefiles(request)

	context = {
		'users_casefiles': users_casefiles,
	}

	return render(request, 'cases/display_casefiles.html', context)

# creates a new case using similar code to edit, using the
# ckeditor plugin, and saves it as a new case to the database
@login_required
def create_case(request):
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			text = form.cleaned_data['text']
			author = request.user
			new_case = Case.objects.create_case(title, text, author)
			return redirect('case', casefile_id=new_case.pk)
	else:
		form = TextForm()

	return render(request, 'cases/edit_cases.html', {'form': form})

# creates an empty casefile and description for a casefile
# user must edit in additional data
@login_required
def create_casefile(request):
	if request.method == 'POST':
		form = CasefileForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			author = request.user
			new_casefile = CaseFile.objects.create_casefile(title, description, author)
			return redirect('casefile', case_id=new_casefile.pk)
	else:
		form = CasefileForm()
	return render(request, 'cases/create_casefile.html', {'form': form})

# takes and uploads a file, then calls the process_case url to complete the file
@login_required
def upload_case(request):
	if request.method == 'POST':
		form = UploadCase(request.POST, request.FILES)
		if form.is_valid():
			title = form.cleaned_data['title']
			file = form.cleaned_data['file']
			author = request.user
			new_file = RawFile.objects.upload_file(title, file, author)
			file_id = new_file.id
			return redirect('process_case', file_id=file_id)
	else:
		form = UploadCase()
	return render(request, 'cases/upload_case.html', {'form': form})

# uses the mammoth library to convert an uploaded docx file into html
# deletes the file after attempting to convert it, to conserve disk space
@login_required
def process_case(request, file_id):
	file = RawFile.objects.get(id=file_id)
	converted_file = convert_docx(file.file.url)

	title = file.title
	text = converted_file[0]
	author = request.user
	new_case = Case.objects.create_case(title, text, author)
	file.delete()

	return redirect('edit', case_id=new_case.id)

# basic case text editor which uses the TinyMCE plugin within the form
# form will be prefilled with the previous case text, allowing user to edit
@login_required
def edit(request, case_id):
	can_edit = check_ownership(request, case_id)
	specific_case = Case.objects.get(pk=case_id)
	default_text = specific_case.text
	default_title = specific_case.title

	if can_edit:
		if request.method == 'POST':
			form = TextForm(request.POST)
			if form.is_valid():
				new_title = form.cleaned_data['title']
				new_text = form.cleaned_data['text']
				old_case = Case.objects.get(pk=case_id)
				old_case.text = new_text
				old_case.title = new_title
				old_case.save()
				return redirect('case', case_id=specific_case.pk)	
		else:
			form = TextForm(initial={'title': default_title,
				'text': default_text})
		context = {
			'form': form,
			'case_id': specific_case.pk
		}
		return render(request, 'cases/edit_cases.html', context)
	else:
		raise PermissionDenied

@login_required
def add_cases(request, casefile_id):
	specific_casefile = CaseFile.objects.get(pk=casefile_id)
	can_edit = check_casefile_ownership(request, casefile_id)
	cookie_unfiltered = list()
	cases = list()

	return render(request, 'cases/add_cases.html', context)
