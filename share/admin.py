from django.contrib import admin

from .models import PlantTip
from .models import PlantBuddy
from .models import Publishing

admin.site.register(PlantTip)
admin.site.register(PlantBuddy)
admin.site.register(Publishing)
