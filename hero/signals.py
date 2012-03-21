from django.dispatch import Signal

achievement_unlocked = Signal(providing_args=['achievement'])
achievement_locked = Signal(providing_args=['achievement'])