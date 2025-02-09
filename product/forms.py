from django import forms
from .models import Comment,Product,CartItem,Cart
class CommentForm(forms.ModelForm):
  def __init__(self, *arg,**kwargs):
    self.author=kwargs.pop('author',None)
    self.product=kwargs.pop('product',None)
    super().__init__(*arg,**kwargs)
  def save(self, commit=True):
    comment=super().save(commit=False)
    comment.author=self.author
    comment.product=self.product
    comment.save()
  class Meta:
    model =Comment
    fields = ["body"]



