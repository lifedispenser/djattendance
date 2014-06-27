from itertools import chain

from tastypie import fields, utils
from tastypie.resources import ModelResource
from tastypie.validation import Validation, CleanedDataFormValidation
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization


from leaveslips.models import LeaveSlip, IndividualSlip, GroupSlip, MealOutSlip, NightOutSlip, IndividualSlipForm
from schedules.models import Event
from accounts.models import Profile, User, Trainee, TrainingAssistant


''' leaveslip_api resources.py

All the API resources for leaveslips. For each model, GET, POST, and PUT are supported.

See schemas.txt for sample formats.

'''

class EventResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = Event.objects.all()
        resource_name = 'events'

class TraineeResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = Trainee.objects.all()
        resource_name = 'trainee'


class TrainingAssistantResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = TrainingAssistant.objects.all()
		resource_name = 'TA'
		

class IndividualSlipResource(ModelResource):
	trainee = fields.ForeignKey(TraineeResource, 'trainee')
	TA = fields.ForeignKey(TrainingAssistantResource, 'TA')
	events = fields.ToManyField(EventResource, 'events')

	class Meta:
		queryset = IndividualSlip.objects.all()
		allowed_methods = ['get', 'post', 'put', 'delete']
		authentication = BasicAuthentication()
		authorization = Authorization()
		form = CleanedDataFormValidation(form_class=IndividualSlipForm)

	def get_object_list(self, bundle, **kwargs):
		if hasattr(bundle, 'request'):
			query = bundle.request.GET.get('event-id', None)
			if query:
				objects_one = IndividualSlip.objects.filter(events__id=query)[:1]
				# Note: currently not dealing with other kinds of leave slips; below is roughly how it would be 
				# done. If more than one leaveslip covers an event, we only display the first one. (All would
				# appear if viewing the list page).

				# objects_two = MealOutSlip.objects.filter(events__id=query)
				# objects_three = NightOutSlip.objects.filter(events__id=query)
				# objects_four = GroupSlip.objects.filter(events__id=query)
				# return chain(objects_one, objects_two, objects_three, objects_four)[:1]
				return objects_one
		return super(IndividualSlipResource, self).get_object_list(bundle, **kwargs)
		
	def obj_get_list(self, bundle, **kwargs):
		return self.get_object_list(bundle, **kwargs)

class MealOutSlipResource(ModelResource):
	leaveslip = fields.OneToOneField(IndividualSlipResource, 'leaveslip', null=False, full=True)

	class Meta:
		queryset = MealOutSlip.objects.all()
		allowed_methods = ['get', 'post', 'put']

class NightOutSlipResource(ModelResource):
	leaveslip = fields.OneToOneField(IndividualSlipResource, 'leaveslip', null=False, full=True)

	class Meta:
		queryset = NightOutSlip.objects.all()
		allowed_methods = ['get', 'post', 'put']

class GroupSlipResource(ModelResource):
	class Meta:
		queryset = GroupSlip.objects.all()
		allowed_methods = ['get', 'post', 'put']
