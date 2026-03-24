from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(
        max_length=500,
        label='text',
        required=True,
        error_messages={
            'required': 'Комментарий не должен быть пустым',
            'max_length': 'Комментарий должен быть не более 500 символов',
        }
    )
    is_anon = forms.BooleanField(
        label='is_anon',
        required=False,
    )