from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from .models import Portfolio, CardInstance
from .forms import CardInstanceForm


from django.db.models import Sum, Value


from .models import Portfolio, CardInstance, CardSet


def home(request):
    qs = Portfolio.objects.select_related('user').annotate(
        cards_count=Count('card_instances'),
        total_value_annot=Coalesce(
            Sum('card_instances__price'),
            Value(0),
            output_field=models.DecimalField(max_digits=10, decimal_places=2),
        )
    ).order_by('user__username')

    
    if request.user.is_authenticated:
        qs = qs.exclude(user=request.user)

    return render(request, 'portfolio/home.html', {'public_portfolios': qs})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Portfolio.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Konto zostało utworzone! Witaj!')
            return redirect('portfolio_view')
    else:
        form = UserCreationForm()
    return render(request, 'portfolio/register.html', {'form': form})

def apply_filters(request, cards_qs):
    selected_set = (request.GET.get("set") or "").strip()
    selected_condition = (request.GET.get("condition") or "").strip()

    if selected_set:
        cards_qs = cards_qs.filter(card__card_set_id=selected_set)

    if selected_condition:
        cards_qs = cards_qs.filter(condition=selected_condition)

    filtered_total = cards_qs.aggregate(
        total=Coalesce(
            Sum("price"),
            Value(0),
            output_field=models.DecimalField(max_digits=10, decimal_places=2),
        )
    )["total"]

    return cards_qs, selected_set, selected_condition, filtered_total

@login_required
def portfolio_view(request):
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    cards = portfolio.card_instances.all().select_related('card', 'card__card_set')

    # --- FILTRY (GET) ---
    selected_set = (request.GET.get("set") or "").strip()
    selected_condition = (request.GET.get("condition") or "").strip()

    if selected_set:
        cards = cards.filter(card__card_set_id=selected_set)
    if selected_condition:
        cards = cards.filter(condition=selected_condition)

    # --- SORT (GET) ---
    sort = (request.GET.get("sort") or "date_desc").strip()

    sort_map = {
    "date_desc": "-added_at",
    "date_asc": "added_at",
    "price_desc": "-price",
    "price_asc": "price",
    "name_asc": "card__name",
    "name_desc": "-card__name",
    "set_asc": "card__card_set__name",
    "set_desc": "-card__card_set__name",
    "condition_asc": "condition",
    "condition_desc": "-condition",
}

    cards = cards.order_by(sort_map.get(sort, "-added_at"))

    # wartość po filtrach (sort nie ma znaczenia)
    filtered_total_value = sum((c.price or 0) for c in cards)

    return render(request, "portfolio/portfolio.html", {
        "portfolio": portfolio,
        "cards": cards,
        "total_value": filtered_total_value,
        "portfolio_total_value": portfolio.total_value(),
        "filters_active": bool(selected_set or selected_condition),

        "sets": CardSet.objects.order_by("name"),
        "conditions": CardInstance.CONDITION_CHOICES,
        "selected_set": selected_set,
        "selected_condition": selected_condition,

        "sort": sort,
        "is_owner": True,
    })


@login_required
def card_add(request):
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CardInstanceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.portfolio = portfolio
            obj.save()
            messages.success(request, "Karta dodana do portfolio.")
            return redirect("portfolio_view")
    else:
        form = CardInstanceForm()

    return render(request, "portfolio/card_form.html", {"form": form, "mode": "add"})


@login_required
def card_edit(request, pk: int):
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    card_instance = get_object_or_404(CardInstance, pk=pk, portfolio=portfolio)

    if request.method == "POST":
        form = CardInstanceForm(request.POST, request.FILES, instance=card_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Karta zaktualizowana.")
            return redirect("portfolio_view")
    else:
        form = CardInstanceForm(instance=card_instance)

    return render(request, "portfolio/card_form.html", {"form": form, "mode": "edit"})


@login_required
def card_delete(request, pk: int):
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    card_instance = get_object_or_404(CardInstance, pk=pk, portfolio=portfolio)

    if request.method == "POST":
        card_instance.delete()
        messages.success(request, "Karta usunięta z portfolio.")
        return redirect("portfolio_view")

    return render(request, "portfolio/card_confirm_delete.html", {"card_instance": card_instance})

def user_portfolio(request, username: str):
    user = get_object_or_404(User, username=username)
    portfolio, _ = Portfolio.objects.get_or_create(user=user)
    cards = portfolio.card_instances.all().select_related('card', 'card__card_set')

    # --- FILTRY (GET) ---
    selected_set = (request.GET.get("set") or "").strip()
    selected_condition = (request.GET.get("condition") or "").strip()

    if selected_set:
        cards = cards.filter(card__card_set_id=selected_set)
    if selected_condition:
        cards = cards.filter(condition=selected_condition)

    # --- SORT (GET) ---
    sort = (request.GET.get("sort") or "date_desc").strip()

    sort_map = {
    "date_desc": "-added_at",
    "date_asc": "added_at",
    "price_desc": "-price",
    "price_asc": "price",
    "name_asc": "card__name",
    "name_desc": "-card__name",
    "set_asc": "card__card_set__name",
    "set_desc": "-card__card_set__name",
    "condition_asc": "condition",
    "condition_desc": "-condition",
}

    cards = cards.order_by(sort_map.get(sort, "-added_at"))

    filtered_total_value = sum((c.price or 0) for c in cards)

    is_owner = request.user.is_authenticated and request.user == user

    return render(request, "portfolio/portfolio.html", {
        "portfolio": portfolio,
        "cards": cards,
        "total_value": filtered_total_value,
        "portfolio_total_value": portfolio.total_value(),
        "filters_active": bool(selected_set or selected_condition),

        "sets": CardSet.objects.order_by("name"),
        "conditions": CardInstance.CONDITION_CHOICES,
        "selected_set": selected_set,
        "selected_condition": selected_condition,

        "sort": sort,
        "is_owner": is_owner,
    })