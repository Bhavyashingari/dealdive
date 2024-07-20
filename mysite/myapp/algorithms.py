from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

def train_model():
    reader = Reader(rating_scale=(1, 5))  # Assuming ratings are 1-5
    data = Dataset.load_from_df(Rating.objects.all().values('user_id', 'item_id', 'rating'), reader)
    trainset = data.build_full_trainset()

    algo = SVD()  # Use the SVD algorithm
    cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)  # Evaluate
    algo.fit(trainset)
    return algo

def get_recommendations(user_id, algo):
    # Get all items the user has not rated
    rated_items = set(Rating.objects.filter(user_id=user_id).values_list('item_id', flat=True))
    all_items = set(Item.objects.values_list('item_id', flat=True))
    unrated_items = all_items - rated_items

    # Predict ratings for unrated items
    predictions = [algo.predict(user_id, item_id) for item_id in unrated_items]

    # Sort predictions and return top-N
    top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:10]  # Get top 10
    return [Item.objects.get(item_id=pred.iid) for pred in top_n]  # Return Item objects
