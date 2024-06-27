from django import forms

class TextForm(forms.Form):
    text1 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'مقدمة الشكر'})
    )
    text2 = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'اسم الممنوح له الشهاده او التكريم (او مجموعة اسماء)' , 'row':1000})
    )
    text3 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'عبارات الشكر'})
    )
    text4 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'عبارات الشكر (اختياري)'})
    )
    text5 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'عبارات الشكر (اختياري)'})
    )
    text6 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'الخاتمة'})
    )
    text7 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'المسؤول'})
    )
    text8 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'أسم المسؤول'})
    )
    text9 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'المسؤول'})
    )
    text10 = forms.CharField(
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
            'text9': '',
            'text10': '',
        }
        label_suffix = ''
