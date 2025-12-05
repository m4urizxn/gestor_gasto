from django.db import models


class Gasto(models.Model):
    PERSONAS = [
        ('mama', 'Mamá'),
        ('mauricio', 'Mauricio'),
        ('papa', 'Papá'),
    ]
    
    ESTADO_CHOICES = [
        ('falta', 'Falta Pagar'),
        ('pagado', 'Pagado'),
        ('no_pago', 'No se Pagó'),
    ]
    
    persona = models.CharField(max_length=20, choices=PERSONAS)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nota = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='falta')
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_persona_display()} - {self.descripcion}: S/ {self.monto}"


class DineroEnviado(models.Model):
    DESTINO_CHOICES = [
        ('mama', 'Mamá'),
        ('mauricio', 'Mauricio'),
    ]
    
    destino = models.CharField(max_length=20, choices=DESTINO_CHOICES)
    monto_euros = models.DecimalField(max_digits=10, decimal_places=2)
    monto_soles = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_cambio = models.DecimalField(max_digits=10, decimal_places=4)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_destino_display()} - €{self.monto_euros} (S/ {self.monto_soles})"
