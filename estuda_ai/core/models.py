from django.db import models
from django.contrib.auth.models import User

class NotasENEM(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linguagens_nota = models.FloatField(null=True, blank=True)
    linguagens_peso = models.FloatField(null=True, blank=True)
    matematica_nota = models.FloatField(null=True, blank=True)
    matematica_peso = models.FloatField(null=True, blank=True)
    natureza_nota = models.FloatField(null=True, blank=True)
    natureza_peso = models.FloatField(null=True, blank=True)
    humanas_nota = models.FloatField(null=True, blank=True)
    humanas_peso = models.FloatField(null=True, blank=True)
    redacao_nota = models.FloatField(null=True, blank=True)
    redacao_peso = models.FloatField(null=True, blank=True)

    def calcular_media_ponderada(self):
        notas_pesos = [
            (self.linguagens_nota, self.linguagens_peso),
            (self.matematica_nota, self.matematica_peso),
            (self.natureza_nota, self.natureza_peso),
            (self.humanas_nota, self.humanas_peso),
            (self.redacao_nota, self.redacao_peso),
        ]
        soma_notas_pesos = sum(nota * peso for nota, peso in notas_pesos if nota is not None and peso is not None)
        soma_pesos = sum(peso for nota, peso in notas_pesos if nota is not None and peso is not None)
        return soma_notas_pesos / soma_pesos if soma_pesos else 0

    def __str__(self):
        return f"Notas do ENEM de {self.user.username}"
