from django.apps import apps as django_apps
from django.contrib.admin import AdminSite

# app_config = django_apps.get_app_config('edc_base')


class EdcFieldLabelAdminSite(AdminSite):
    #     site_title = app_config.project_name
    #     site_header = app_config.project_name
    #     index_title = app_config.project_name
    site_url = '/'


edc_field_label_admin = EdcFieldLabelAdminSite(name='edc_field_label_admin')
