from subscriptions.models import Borrowing

def total_borrowed(request):
    if request.user.is_authenticated:
        return {
            'total_borrowed': Borrowing.objects.filter(user=request.user, is_returned=False).count()
        }
    return {'total_borrowed': 0}