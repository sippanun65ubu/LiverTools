from django import forms
from .models import Product, Category, ChatMessage
from user.models import Address

class ProductForm(forms.ModelForm):
    # Extra field for creating a new category if needed
    new_category = forms.CharField(
        required=False,
        label="New Category",
        help_text="Type a new category if not in the list."
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'size', 'category', 'image', 'new_category']
        widgets = {
            'category': forms.SelectMultiple(attrs={'style': 'width: 300px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the category queryset with all available categories
        self.fields['category'].queryset = Category.objects.order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # ✅ ตรวจสอบและบันทึก quantity ให้แน่ใจว่ามีการอัปเดตค่า
        instance.quantity = self.cleaned_data.get('quantity', instance.quantity)

        if commit:
            instance.save()  # ✅ บันทึก instance ก่อน
            self.save_m2m()  # ✅ บันทึก ManyToManyField

        # ✅ เพิ่ม category ใหม่หากมีการกรอก
        new_cat_name = self.cleaned_data.get('new_category')
        if new_cat_name:
            category_obj, created = Category.objects.get_or_create(name=new_cat_name)
            instance.category.add(category_obj)  # ✅ เพิ่ม category ใหม่ให้สินค้า

        return instance

class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'พิมพ์ข้อความของคุณ...'})
        }


class SelectAddressForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        label="เลือกที่อยู่"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show addresses belonging to this user
        self.fields['address'].queryset = user.addresses.all()

