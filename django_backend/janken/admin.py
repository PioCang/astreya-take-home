""" For admin UI debugging """

from django.contrib import admin
from .models import Match, Player, Round

# Register your models here.
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(Round)
