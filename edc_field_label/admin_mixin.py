import re
import json
from datetime import datetime, date


class ModifyFormLabelMixin(object):
    """Replace a from label datetime placeholder with a datetime value."""
    label_replacements = {}

    def get_form(self, request, obj=None, **kwargs):
        form = super(ModifyFormLabelMixin, self).get_form(request, obj, **kwargs)
        self.label_replacements = json.loads((request.GET.get(
            'label_replacements', json.dumps({}, cls=DatetimeEncoder))))
        return self.replace_labels(form)

    def replace_labels(self, form):
        """Replace a place holder on a label with a value."""
        WIDGET = 1
        place_holder_value = None
        for _, fld in enumerate(form.base_fields.items()):
            for _, values in self.label_replacements.items():
                if values['field_attr'] == fld[0]:
                    place_holder_value = values['place_holder_value']
                    if place_holder_value:
                        # Convert the value for the place holder to string
                        if re.search(r'{}'.format(values['place_holder']), str(fld[WIDGET].label)):
                            fld[WIDGET].label = re.sub(
                                '{}'.format(values['place_holder']),
                                place_holder_value, fld[WIDGET].label)
        return form


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%A, %B %d, %Y at %H:%M hours')
        elif isinstance(obj, date):
            return obj.strftime('%A, %B %d, %Y')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
