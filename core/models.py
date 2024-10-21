from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nome = models.CharField(max_length=255)
    linguagens_peso = models.FloatField(default=1.0)
    matematica_peso = models.FloatField(default=1.0)
    natureza_peso = models.FloatField(default=1.0)
    humanas_peso = models.FloatField(default=1.0)
    redacao_peso = models.FloatField(default=1.0)

    def __str__(self):
        return self.nome

    
class NotasENEM(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    linguagens_nota = models.FloatField(null=True, blank=True)
    matematica_nota = models.FloatField(null=True, blank=True)
    natureza_nota = models.FloatField(null=True, blank=True)
    humanas_nota = models.FloatField(null=True, blank=True)
    redacao_nota = models.FloatField(null=True, blank=True)

    def calcular_media_ponderada(self):
        soma_notas_pesos = (
            (self.linguagens_nota or 0) * self.curso.linguagens_peso +
            (self.matematica_nota or 0) * self.curso.matematica_peso +
            (self.natureza_nota or 0) * self.curso.natureza_peso +
            (self.humanas_nota or 0) * self.curso.humanas_peso +
            (self.redacao_nota or 0) * self.curso.redacao_peso
        )
        soma_pesos = (
            self.curso.linguagens_peso +
            self.curso.matematica_peso +
            self.curso.natureza_peso +
            self.curso.humanas_peso +
            self.curso.redacao_peso
        )
        return soma_notas_pesos / soma_pesos if soma_pesos else 0

    def __str__(self):
        return f"Notas do ENEM de {self.user.username} para {self.curso.nome}"
