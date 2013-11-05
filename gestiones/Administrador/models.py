from django.db import models

class permisosVistas(models.Model):
    
    class Meta:
        permissions = (
           
            ("is_admin","Es Administrador"),
            ("is_cajero","Es Cajero"),
            ("is_mozo","Es Mozo"),
        )