from django import forms
from .models import CardInstance

class CardInstanceForm(forms.ModelForm):
    class Meta:
        model = CardInstance
        fields = ["card", "condition", "price", "notes", "image"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        for name, field in self.fields.items():
            if name in ("card", "condition"):
                field.widget.attrs.update({"class": "form-select"})
            else:
                field.widget.attrs.update({"class": "form-control"})