from django.forms.forms import Form
from django import forms
from crispy_forms.layout import Layout, Fieldset, Submit, Field
import logging
from crispy_forms.helper import FormHelper

__author__ = 'stefanotranquillini'

log = logging.getLogger(__name__)


class RitardiForm(Form):
    partenza = forms.CharField(label=(u'Partenza '), required=True)
    arrivo = forms.CharField(label=(u'Arrivo '), required=True)


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'form'
        self.helper.layout = Layout(Fieldset('Cerca treni', 'partenza', 'arrivo'))
        submit = Submit('submit', 'Invia', data_loading_text="Loading...")

        self.helper.add_input(submit)
        self.helper.form_class = 'form-signin'
        super(RitardiForm, self).__init__(*args, **kwargs)


class StazioneForm(Form):
    stazione = forms.CharField(label=(u'Stazione '), required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'form'
        self.helper.layout = Layout(Fieldset('Cerca treni', Field('stazione', css_class="search")))
        submit = Submit('submit', 'Invia', data_loading_text="Loading...")

        self.helper.add_input(submit)
        self.helper.form_class = 'form-signin'
        super(StazioneForm, self).__init__(*args, **kwargs)


class StazioneFormChoices(Form):
    stazione = forms.ChoiceField(label=(u'Stazione '), required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        stazioni = kwargs.pop('stazioni')
        log.debug(stazioni)
        self.helper.form_method = 'post'
        self.helper.form_id = 'form'
        self.helper.layout = Layout(Fieldset('Cerca treni', 'stazione'))
        submit = Submit('submit', 'Invia', data_loading_text="Loading...")
        self.helper.add_input(submit)
        self.helper.form_class = 'form-signin'
        super(StazioneFormChoices, self).__init__(*args, **kwargs)
        self.fields['stazione'].choices = stazioni