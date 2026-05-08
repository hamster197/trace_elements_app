from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

from apps.questionnaire.constants import QuestionEstimateChoises
from apps.questionnaire.models import Questionnaire, QuestionQuide


class QuestionnaireForm(forms.ModelForm):

    class Meta:
        model = Questionnaire
        exclude = ['user_id', 'creation_date',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['favorite_foods_id'].queryset = self.instance.get_favorite_foods_queruset()
            self.fields['not_favorite_foods_id'].queryset = self.instance.get_not_favorite_foods_id_queruset()

    def clean(self):
        cleaned_data = super(QuestionnaireForm, self).clean()

        list1 = cleaned_data['favorite_foods_id'].values_list('pk')
        list2 = cleaned_data['not_favorite_foods_id'].values_list('pk')

        common_elements = set(list1) & set(list2)
        if common_elements:
            raise ValidationError('Delete double in favorite and not favorite foods elemnts!', code='invalid')

        return cleaned_data


class QuestionForm(forms.ModelForm):
    answer_field = forms.ChoiceField(choices=QuestionEstimateChoises.choices,
                                     widget=forms.RadioSelect(attrs={"required": True}), label='Answer choises',)
    text = forms.CharField(required=False)

    class Meta:
        model = QuestionQuide
        exclude = ['elements_id', ]

QuestionsFormset = modelformset_factory(QuestionForm.Meta.model, form=QuestionForm,
                                              can_delete=False, extra=0)
