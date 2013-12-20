from django.forms.models import modelformset_factory
from absent_trainee_roster.forms import AbsentTraineeForm, NewEntryFormSet
from django.shortcuts import render, render_to_response, redirect

from django.views.generic.edit import FormView
from django.core.context_processors import csrf
from django.template import RequestContext # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet

from django.contrib.auth.decorators import user_passes_test

from absent_trainee_roster.forms import AbsentTraineeForm
from absent_trainee_roster.models import Entry, Roster
from absent_trainee_roster.forms import AbsentTraineeForm, NewEntryFormSet

from datetime import date

from django.http import HttpResponse

@user_passes_test(lambda u: u.groups.filter(name='house_coordinator').count() == 1, login_url = '/')
def absent_trainee_form(request):
	EntryFormSet = modelformset_factory(Entry, AbsentTraineeForm, formset=NewEntryFormSet, max_num=10, extra=1, can_delete=True)
	
	# get today's roster. create it if it doesn't exist.
	if Roster.objects.filter(date=date.today()).exists():
		roster = Roster.objects.get(date=date.today())
	else:
		roster = Roster.objects.create_roster(date=date.today())

	if request.method == 'POST':
		formset = EntryFormSet(request.POST, request.FILES, user=request.user)
		if formset.is_valid():
			for form in formset.forms:
				if form.cleaned_data: # only save entry if it's not empty
					entry = form.save(commit=False)
					entry.roster = roster
					entry.save()
			roster.unreported_houses.remove(request.user.trainee.house)
			return redirect('/')
		
		else:
			c = {'formset': formset, 'user': request.user}
			c.update(csrf(request))
			
			return render_to_response('absent_trainee_roster/absent_trainee_form.html', c)

	else:
		formset = EntryFormSet(user=request.user, queryset=roster.entry_set.filter(absentee__account__trainee__house=request.user.trainee.house))

	c = {'formset': formset, 'user': request.user}
	c.update(csrf(request))

	return render_to_response('absent_trainee_roster/absent_trainee_form.html', c)
