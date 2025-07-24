from .models import UserProfile

def coins_context(request):
    coins = 0
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            coins = profile.coins
        except UserProfile.DoesNotExist:
            pass
    return {'coins': coins}
