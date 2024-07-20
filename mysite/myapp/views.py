from django.shortcuts import render
from .algorithms import train_model, get_recommendations
from .models import User
from collections import Counter

def index(request):
    model = train_model()

    search_query = request.GET.get('q', '')

    search_terms = ['protein powder', 'dumbbells', 'yoga mat', 'protein powder', 'dumbbells']
    purchased_items = ['protein powder', 'dumbbells', 'treadmill', 'protein powder']

    if search_query:
        search_terms = [term for term in search_terms if search_query.lower() in term.lower()]
        purchased_items = [item for item in purchased_items if search_query.lower() in item.lower()]

    most_frequent_searches = Counter(search_terms).most_common(5)
    most_frequent_purchases = Counter(purchased_items).most_common(5)

    return render(request, 'index.html', {
        'most_frequent_searches': most_frequent_searches,
        'most_frequent_purchases': most_frequent_purchases,
        'search_query': search_query
    })

def recommendations(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, 'recommendations.html', {'error': 'User not found'})

    model = train_model()
    recommended_items = get_recommendations(user_id, model)
    return render(request, 'recommendations.html', {'user': user, 'recommendations': recommended_items})
