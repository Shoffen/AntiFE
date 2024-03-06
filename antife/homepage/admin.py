from django.contrib import admin
from .models import TodoItem
from .models import Naudotojai, Product, Receptai, Forumai, Irasai, Kraujo_tyrimai, Recepto_produktai, Naudotojo_receptai, Valgiarasciai, Komentarai, Valgymai, Valgomas_produktas, Valgymo_receptas

admin.site.register(TodoItem)
admin.site.register(Naudotojai)
admin.site.register(Receptai)
admin.site.register(Forumai)
admin.site.register(Irasai)
admin.site.register(Kraujo_tyrimai)
admin.site.register(Recepto_produktai)
admin.site.register(Naudotojo_receptai)
admin.site.register(Valgiarasciai)
admin.site.register(Komentarai)
admin.site.register(Valgymai)
admin.site.register(Valgomas_produktas)
admin.site.register(Valgymo_receptas)
