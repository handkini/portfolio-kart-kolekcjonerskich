from django.contrib import admin
from .models import Portfolio, CardSet, Card, CardInstance, Transaction

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_value')
    search_fields = ('user__username',)

@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date')
    search_fields = ('name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_set', 'card_number')
    list_filter = ('card_set',)
    search_fields = ('name', 'card_number')

@admin.register(CardInstance)
class CardInstanceAdmin(admin.ModelAdmin):
    list_display = ('card', 'portfolio', 'condition', 'price', 'added_at')
    list_filter = ('condition', 'card__card_set')
    search_fields = ('card__name', 'portfolio__user__username')
    ordering = ('-added_at',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('card_instance', 'transaction_type', 'amount', 'date')
    list_filter = ('transaction_type', 'date')
    search_fields = ('card_instance__card__name',)
    ordering = ('-date',)

from django.contrib.admin.sites import NotRegistered

try:
    admin.site.unregister(Transaction)
except NotRegistered:
    pass

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.models import Group

try:
    admin.site.unregister(Group)
except NotRegistered:
    pass