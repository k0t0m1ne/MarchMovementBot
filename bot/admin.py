from django.contrib import admin
from .models import PlayerTask, Player, Tasks, QrCodes

admin.site.register(Player)
admin.site.register(PlayerTask)
admin.site.register(Tasks)
admin.site.register(QrCodes)

