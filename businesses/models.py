from django.db import models


class Business(models.Model):
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('club', 'Club'),
        ('real_estate', 'Agenzia Immobiliare'),
        ('travel_agency', 'Agenzia Viaggi'),
        ('medical', 'Studio Medico'),
        ('technical_studio', 'Studio Tecnico'),
        ('dentist', 'Dentista'),
        ('physiotherapist', 'Fisioterapista'),
        ('private_school', 'Scuola Privata'),
        ('beauty_center', 'Centro Estetico'),
        ('artisan', 'Artigiano'),
        ('other', 'Altro'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=64, blank=True)
    website = models.URLField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['country', 'city', 'category']),
        ]
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name} ({self.city}, {self.country})"

