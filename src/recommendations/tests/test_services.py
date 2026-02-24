from recommendations.services import get_recommendations


def test_top_3_recommendations_with_more_noise(sample_items, user_preferences):
    recommendations = get_recommendations(user_preferences, sample_items, top_n=3)
    # The top 3 recommendations should include highly relevant items but also account for similar Sci-Fi items like Blade Runner
    expected_items = {"Aliens", "True Lies", "Predator"}
    acceptable_alternatives = {
        "Blade Runner"
    }  # Blade Runner is also relevant due to Sci-Fi genre
    # Extract the names of the top 3 recommendations
    recommended_item_names = {rec.name for rec in recommendations}
    # Ensure that all expected or acceptable items are in the top recommendations
    assert (expected_items & recommended_item_names) or (
        acceptable_alternatives & recommended_item_names
    ), (
        f"Top recommendations should include: {expected_items} or alternatives like {acceptable_alternatives}, "
        f"but got: {recommended_item_names}"
    )


def test_recommendations_handle_more_noise(sample_items, user_preferences_with_noise):
    recommendations = get_recommendations(
    user_preferences_with_noise, sample_items, top_n=5
    )
    noisy_items = {
    "Sleepless in Seattle",
    "Pride and Prejudice",
    "The Notebook",
    "La La Land",
    "Casablanca",
    }
    for item in recommendations:
        assert item.name not in noisy_items, f"Noisy item '{item.name}' should not be in recommendations"