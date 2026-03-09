from .models import UserProfile

def coins_context(request):
    coins = 0
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user, defaults={'coins': 250})
        if not created and profile.coins == 0:
            profile.coins = 250
            profile.save(update_fields=['coins'])
        coins = profile.coins
    return {'coins': coins}
