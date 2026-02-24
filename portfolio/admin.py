from django.contrib import admin
from .models import Portfolio, CardSet, Card, CardInstance, Transaction
# Rejestracja modelu Portfolio
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_value')
    search_fields = ('user__username',)
# Rejestracja modelu CardSet
@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date')
    search_fields = ('name',)
# Rejestracja modelu Card
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_set', 'card_number')
    list_filter = ('card_set',)
    search_fields = ('name', 'card_number')
# Rejestracja modelu CardInstance
@admin.register(CardInstance)
class CardInstanceAdmin(admin.ModelAdmin):
    list_display = ('card', 'portfolio', 'condition', 'price', 'added_at')
    list_filter = ('condition', 'card__card_set')
    search_fields = ('card__name', 'portfolio__user__username')
    ordering = ('-added_at',)
# Rejestracja modelu Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('card_instance', 'transaction_type', 'amount', 'date')
    list_filter = ('transaction_type', 'date')
    search_fields = ('card_instance__card__name',)
    ordering = ('-date',)