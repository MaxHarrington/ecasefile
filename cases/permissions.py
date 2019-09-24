from .models import Case, CaseFile


# Checks to see if the user making a request matches the case author.
# Returns True if it does, False if it doesn't.
# Superusers can edit it regardless of ownership.
def check_ownership(request, case_id):
	unverified_case = Case.objects.get(pk=case_id)
	unverified_username = request.user.username
	if str(unverified_case.author) == str(unverified_username):
		return True
	else:
		return False


def check_casefile_ownership(request, casefile_id):
	unverified_casefile = CaseFile.objects.get(pk=casefile_id)
	unverified_username = request.user.username
	if str(unverified_casefile.author) == str(unverified_username):
		return True
	else:
		return False


# Returns all cases 'owned' by the logged-in user.
def owned_cases(request):
	username = request.user
	users_cases = Case.objects.filter(author=username)
	return users_cases


# Returns all casefiles 'owned' by the logged-in user.
def owned_casefiles(request):
	username = request.user
	users_casefiles = CaseFile.objects.filter(author=username)
	return users_casefiles
