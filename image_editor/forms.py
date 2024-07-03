from django import forms
from django.contrib.auth.forms import AuthenticationForm
class TextForm(forms.Form):
    text1 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(...تتقدم ادارة المدرسة) مقدمة الشكر'})
    )
    text2 = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'اسم الممنوح له الشهادة او التكربم (او مجموعة اسماء) كل اسم في سطر' , 'row':1000})
    )
    text3 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(...علي جهودة المبذولة في) عبارات الشكر'})
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
        widget=forms.TextInput(attrs={'placeholder': ' (متمنيين له دوام التوفيق والنجاح) الخاتمة'})
    )
    text7 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': ' (أو المدير) المسؤول'})
    )
    text8 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'أسم المسؤول'})
    )
    text9 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': ' (أو المعلم) المسؤول'})
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