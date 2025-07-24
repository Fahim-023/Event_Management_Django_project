from django import forms
from events.models import Event, Category, Participant

form_input_class = "w-full px-4 py-2 border-2 border border-gray-300 rounded-lg  shadow-sm focus:border-rose-500 focus:ring-rose-500"
form_textarea_class = "w-full px-4 py-2  border-2 border  border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
form_select_class = "w-full px-4 py-2 border border-gray-300 rounded-lg bg-white  focus:ring-2 focus:ring-rose-500"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': form_input_class,'placeholder':"name"}),
            'description': forms.Textarea(attrs={'class': form_textarea_class,'placeholder':"description"}),
        }
     

class EventForm(forms.ModelForm):  
    class Meta:
        model = Event
        fields = ['name', 'category', 'date', 'time', 'location']  
        widgets = {
            'name': forms.TextInput(attrs={'class': form_input_class}),
            'category': forms.Select(attrs={'class': form_select_class}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': form_input_class}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': form_input_class}),  
            'location': forms.TextInput(attrs={'class': form_input_class}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': form_input_class}),
            'email': forms.EmailInput(attrs={'class': form_input_class}),
        }

