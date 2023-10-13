import json

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from example.admin import MyModelAdmin
from example.models import MyModel

from .admin_mixin import DatetimeEncoder


class MockRequest(object):
    pass


class TestReadonlyAdminMixin(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.GET = self.request.GET.copy()
        label_replacements = {
            'first_rep': {
                'field_attr': 'my_first_field',
                'place_holder': 'last_visit_date',
                'place_holder_value': timezone.datetime(1986, 7, 7, 13, 14),
            },
            'second_rep': {
                'field_attr': 'my_first_field',
                'place_holder': 'last_appt_date',
                'place_holder_value': timezone.datetime(1986, 7, 7, 13, 14),
            },
        }
        label_replacements = json.dumps(label_replacements, cls=DatetimeEncoder)
        self.request.GET['label_replacements'] = label_replacements
        self.site = AdminSite()
        self.custom_model_admin = MyModelAdmin(MyModel, self.site)

    def test_default_field_lable_not_changed(self):
        """Assert that the default field labels has not changed."""
        self.request.GET['label_replacements'] = json.dumps({}, cls=DatetimeEncoder)
        form = self.custom_model_admin.get_form(self.request)
        original_label = (
            'We last spoke with you on last_visit_date and scheduled an appointment for'
            ' you in an HIV care clinic on last_appt_date. Did you keep that appointment?')
        self.assertEqual(form.base_fields['my_first_field'].label, original_label)

    def test_replace_labels(self):
        """Assert that a place holder has been replaced with a value."""
        new_label = ('We last spoke with you on Monday, July 07, 1986 at 13:14 hours and scheduled'
                     ' an appointment for you in an HIV care clinic on Monday,'
                     ' July 07, 1986 at 13:14 hours. Did you keep that appointment?')
        form = self.custom_model_admin.get_form(self.request)
        self.assertEqual(form.base_fields['my_first_field'].label, new_label)
