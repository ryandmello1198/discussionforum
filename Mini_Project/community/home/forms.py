from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from home.models import Answer, Question
#from uploads.core.models import Document

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ('username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
    )

    def save(self,commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
        'first_name',
        'last_name',
        'email',
        'password',
        )
#
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('description', 'document', )
class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields =(
        'title',
        'content',
        )

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = (
        'body',
        )
