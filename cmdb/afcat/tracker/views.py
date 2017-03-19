from django.shortcuts import render
from afcat.api.libs.public import BaseView, Logger
# Create your views here.
logger = Logger(__name__)


class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/index.html')


class Login(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/tracker_login.html')


class ApplicationView(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/application_view.html')


class ApplicationDatabase(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/application_database.html')


class HostView(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/host_view.html')


class HostDetail(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/host_detail.html')


class HostEvents(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/host_events.html')


class NetworkView(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/network_view.html')


class NetworkPort(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/network_port.html')


class ReportView(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/report_view.html')


class ManagementGroups(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/management_groups.html')


class ManagementHosts(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/management_hosts.html')


class ManagementTemplates(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/management_templates.html')


class ManagementSettings(BaseView):

    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/management_settings.html')
