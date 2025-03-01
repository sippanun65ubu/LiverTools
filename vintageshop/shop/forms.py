from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    # Extra field for creating a new category
    new_category = forms.CharField(
        required=False,
        label="New Category",
        help_text="Type a new category if not in the dropdown."
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'size', 'category', 'image', 'new_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the existing category dropdown
        self.fields['category'].queryset = Category.objects.order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if the user typed a new category
        new_cat_name = self.cleaned_data.get('new_category')
        if new_cat_name:
            # Create or get the category
            category_obj, created = Category.objects.get_or_create(name=new_cat_name)
            instance.category = category_obj
        
        if commit:
            instance.save()
        return instance
