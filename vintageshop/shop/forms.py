from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    # ช่องให้กรอกหมวดหมู่ใหม่
    new_category = forms.CharField(
        required=False,
        label="New Category",
        help_text="พิมพ์หมวดหมู่ใหม่ ถ้ายังไม่มีในระบบ"
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'size', 'image', 'new_category']

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # เช็คว่าผู้ใช้กรอกหมวดหมู่ใหม่หรือไม่
        new_cat_name = self.cleaned_data.get('new_category')
        if new_cat_name:
            category_obj, created = Category.objects.get_or_create(name=new_cat_name)
            instance.category = category_obj  # ✅ แก้ปัญหา ให้เก็บเป็น instance ของ `Category`
        
        if commit:
            instance.save()
        return instance
