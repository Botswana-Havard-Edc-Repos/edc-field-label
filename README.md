[![Coverage Status](https://coveralls.io/repos/github/Botswana-Havard-Edc-Repos/edc-field-label/badge.svg?branch=develop)](https://coveralls.io/github/Botswana-Havard-Edc-Repos/edc-field-label?branch=develop)
# edc-field-label
Modify or replace a form field label

###Installation


pip install git+https://github.com/botswana-harvard/edc-field-label@develop#egg=edc_field_label

add to settings.py:


INSTALLED_APPS = [
....
'edc_field_lable.apps.AppConfig',
...]

###Usage


A field label on the form is a string that is specified as a verbose name on the models. The field label is usually
the question on the form field or or a description of what should be field on the form field.

This app provides a way to modify the field label on opening the form, but substituting a place holder with a value
provided for a specified field.

First use the admin_mixin that bring in the method that modifies a label. The label replacement value can be a datetime or any other type.

Step 1.

Defination of the custom model admin.

	class MyModelAdmin (ModifyFormLabelMixin, admin.ModelAdmin):

        form = MyModelForm

    	fields = ['my_first_field', 'my_second_field']

	admin.site.register(MyModel, MyModelAdmin)

The models look like this

	class MyModel (models.Model):
	
	    my_first_field = models.CharField(
	        verbose_name="We last spoke with you on last_visit_date and scheduled an appointment for you "
	                     "in an HIV care clinic on last_appt_date. Did you keep that appointment?",
	        default=None,
	        null=True,
	        blank=True,
	        max_length=50,
	        help_text=""
	    )
	
	    my_second_field = models.CharField(
	        verbose_name='Since we last saw you at last_seen_location, did you play soccer?',
	        default=None,
	        null=True,
	        blank=True,
	        max_length=50,
	        help_text=""
	    )
	
	    class Meta:
	        app_label = 'example'
	        verbose_name = "My Model"
	        verbose_name_plural = "My Model"
 
Step 2.

 In your views do the following in the get_context_data:
 
 		def get_context_data(self, **kwargs):
	        context = super(HomeView, self).get_context_data(**kwargs)
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
	        context.update(
	            label_replacements=json.dumps(label_replacements, cls=DatetimeEncoder),
	        )
	        return context
Step 3.

 In the template do the following:
  	
  		This is for an add url:
  		
  		<a href="{% url 'admin:example_mymodel_add' %}?label_replacements={{label_replacements}}">Add MyModel</a>
  
  		This is for a change url:
  		
  		<a href="{% url 'admin:example_mymodel_change' obj.pk %}?label_replacements={{label_replacements}}">Modify MyModel</a>
  		
 
