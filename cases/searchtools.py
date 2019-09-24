from .models import Case
from math import ceil
from django.db.models import Q


def basic_search(search_term, page_number):
	results_per_page = 10
	lower_bound_results = 0
	latest_cases = list()
	search_term_clean = search_term.split("%20")
	search_term_clean = search_term_clean[0].split(" ")
	if page_number != 0:
		result_number = page_number * results_per_page
		lower_bound_results = (page_number - 1) * results_per_page
	else:
		result_number = results_per_page
	query_title = Q()
	query_author = Q()
	for term in search_term_clean:
		query_title = query_title | Q(title__contains=term)
	for term in search_term_clean:
		query_author = query_title | Q(author__contains=term)
	latest_cases = Case.objects.filter(query_title)
	total_results = len(latest_cases)
	latest_cases = latest_cases[lower_bound_results:result_number]
	previous_page = page_number - 1
	next_page = page_number + 1
	context = {
		'latest_cases': latest_cases,
		'current_page': page_number,
		'search_term': search_term,
		'search_term_clean': search_term_clean,
		'total_pages': ceil(total_results / results_per_page),
		'next_page': next_page,
		'previous_page': previous_page,
	}

	return context
