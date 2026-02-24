from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Portfolio użytkownika {self.user.username}"
    def total_value(self):
        """Oblicza całkowitą wartość portfolio"""
        total = sum(instance.price for instance in self.card_instances.all() if instance.price)
        return total

class CardSet(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa setu")
    release_date = models.DateField(null=True, blank=True, verbose_name="Data wydania")
    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa karty")
    card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE, related_name='cards', verbose_name="Set")
    card_number = models.CharField(max_length=50, verbose_name="Numer karty")
    def __str__(self):
        return f"{self.name} ({self.card_set.name} #{self.card_number})"

class CardInstance(models.Model):
    CONDITION_CHOICES = [
        ('mint', 'Mint'),
        ('near_mint', 'Near Mint'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('played', 'Played'),
        ('poor', 'Poor'),
    ]
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='card_instances')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='instances')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Stan")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Cena")
    notes = models.TextField(blank=True, verbose_name="Notatki")
    image = models.ImageField(upload_to='cards/', null=True, blank=True, verbose_name="Zdjęcie")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")
    def __str__(self):
        return f"{self.card.name} ({self.condition}) - {self.portfolio.user.username}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Zakup'),
        ('sale', 'Sprzedaż'),
        ('trade', 'Wymiana'),
    ]
    card_instance = models.ForeignKey(CardInstance, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="Typ transakcji")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kwota")
    date = models.DateField(verbose_name="Data transakcji")
    notes = models.TextField(blank=True, verbose_name="Notatki")
    def __str__(self):
        return f"{self.transaction_type} - {self.card_instance.card.name} ({self.date})"