from django import forms
from .models import Camera
from .get_queryset import get_queryset


class CameraForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Camera
        fields = ('name', 'ip_address', 'port', 'username', 'password')
        password = forms.CharField(widget=forms.PasswordInput)

        widgets = {
            "ip_address" : forms.TextInput(attrs={'class': "form-control", 'placeholder':""}),
            "name" : forms.TextInput(attrs={'class': "form-control", 'placeholder':""})
        }
    
    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     filter_condition1 = {"name": data}
    #     queryset = get_queryset(querytype="filter", filter_condition1=filter_condition1)
    #     name_match = False
    #     for name in queryset:
    #         if data == name:
    #             name_match = True

    #     if name_match:
    #             self.fields['name'].widget.attrs['class'] = "form-control is-invalid"
    #             raise forms.ValidationError('Name cannot be null')
    #     else:
    #         self.fields['name'].widget.attrs['class'] = "form-control is-valid"
    #         return data
            
        
    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     if data == None:
    #         self.fields['name'].widget.attrs['class'] = "form-control is-invalid"
    #         raise forms.ValidationError("name cannot be null")

        
    def clean_ip_address(self):
        ip_data = self.cleaned_data['ip_address']
        if any(char.isalpha() for char in ip_data):
            self.fields['ip_address'].widget.attrs['class'] = "form-control is-invalid"
            raise forms.ValidationError("ip_address cannot contain letter")
        else:
            self.fields['ip_address'].widget.attrs['class'] = "form-control is-valid"
            return ip_data

    def clean_port(self):
        data = self.cleaned_data['port']
        if any(char.isalpha() for char in data):
            self.fields['port'].widget.attrs['class'] = "form-control is-invalid"
            raise forms.ValidationError("port cannot contain letter")
        return data
    
    def __init__(self, *args, **kwargs):
        super(CameraForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'id': 'name',
            'class': 'form-control',
            'name': 'myCustomName',
            'placeholder': 'Name'})
        
        self.fields['ip_address'].widget = forms.TextInput(attrs={
            'id': 'ip_address',
            'class': 'form-control',
            'name': 'myCustomName',
            'placeholder': 'IPaddress'})
        
        self.fields['port'].widget = forms.TextInput(attrs={
        'id': 'port',
        'class': 'form-control',
        'name': 'myCustomName',
        'placeholder': 'Port'})

        self.fields['username'].widget = forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control',
        'name': 'myCustomName',
        'placeholder': 'Username'})

        self.fields['password'].widget = forms.TextInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'name': 'myCustomName',
        'placeholder': 'Password'})

        
        
