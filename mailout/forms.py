from django import forms

from mailout.models import Mailout, Message, Client


class StyleFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailoutForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailout
        exclude = ('auth_user', 'is_active')
        # fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('auth_user',)


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('auth_user',)
