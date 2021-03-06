from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce, TruncMonth


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
            .annotate(category_name=Coalesce('category__name', Value('-')))
            .order_by()
            .values('category_name')
            .annotate(s=Sum('amount'))
            .values_list('category_name', 's')
    ))


def summary_per_year_month(queryset):
    return OrderedDict(sorted(
        queryset
            .annotate(month=TruncMonth('date'))
            .order_by().values('month')
            .annotate(s=Sum('amount'))
            .values_list("month", 's')))


def total_spent(queryset):
    total = [d for a in queryset.values('amount') for d in a.values()]
    return sum(total)
