import datetime
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month, total_spent


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date = form.cleaned_data.get('date')
            category = form.cleaned_data.get('category')
            if name:
                queryset = queryset.filter(name__icontains=name)
            if date:
                queryset = queryset.filter(date__gte=date,
                                           date__lte=datetime.datetime.now())
            if category:
                queryset = queryset.filter(category__name__icontains=category)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            total_spent=total_spent(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category

    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        category_q = object_list if object_list is not None else self.object_list
        expense_q = summary_per_category(Expense.objects.all())
        name_cat = [n.name for n in category_q]
        expenses_cat = {item: expense_q[str(item)] if item in expense_q else '0' for item in name_cat}
        return super().get_context_data(
            object_list=category_q,
            expenses=expenses_cat,
            **kwargs)

