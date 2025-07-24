from .models import UserProfile

def coins_processor(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'coins': profile.coins}
        except UserProfile.DoesNotExist:
            return {'coins': 0}
    return {'coins': 0}
