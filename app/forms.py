from django import forms

class UploadNotaFiscalForm(forms.Form):
    arquivo = forms.FileField(label="Arquivo da Nota Fiscal")