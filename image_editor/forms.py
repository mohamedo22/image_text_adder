from django import forms

class TextForm(forms.Form):
    text1 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'مقدمة الشكر'})
    )
    text2 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'اسم الممنوح له الشهاده او التكريم (او مجموعة اسماء)'})
    )
    text3 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'عبارات الشكر'})
    )
    text4 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'الخاتمة'})
    )
    text5 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'المسؤول'})
    )
    text6 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'أسم المسؤول'})
    )
    text7 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'المسؤول'})
    )
    text8 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'أسم المسؤول'})
    )

    class Meta:
        labels = {
            'text1': '',
            'text2': '',
            'text3': '',
            'text4': '',
            'text5': '',
            'text6': '',
            'text7': '',
            'text8': '',
        }
        label_suffix = ''
