from django.conf.urls import patterns, url
from lifestudies.views import DisciplineListView, DisciplineCreateView, DisciplineDetailView, \
                            SummaryCreateView, SummaryUpdateView, SummaryApproveView, ReportListView, \
                            CreateHouseDiscipline
from lifestudies import views

urlpatterns = patterns('',
    url(r'^$', DisciplineListView.as_view(), name='discipline-list'),
    url(r'^reportview$', ReportListView.as_view(), name='reportview'),
    url(r'^(?P<pk>\d+)/create_summary$', SummaryCreateView.as_view(), name='summary-create'),
    url(r'^(?P<pk>\d+)/detail_summary$', SummaryUpdateView.as_view(), name='summary-detail'),
    url(r'^(?P<pk>\d+)/approve_summary$', SummaryApproveView.as_view(), name='summary-approve'),
    url(r'^create_discipline_house$', CreateHouseDiscipline.as_view(), name='discipline-house'),
    url(r'^create_discipline$', DisciplineCreateView.as_view(), name='discipline-create'),
    url(r'^(?P<pk>\d+)/detail_discipline$', DisciplineDetailView.as_view(), name='discipline-detail'),
    #url(r'^transfer$', views.transfer, name ='transfer'),
)



