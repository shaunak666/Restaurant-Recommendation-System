import unittest
from unittest.mock import patch
import restaurant_recommendation
from restaurant_recommendation import RestaurantRecommendationSystem

class TestRestaurantRecommendationSystem(unittest.TestCase):
    def setUp(self):
        self.recommendation_system = RestaurantRecommendationSystem()

    def test_valid_food_type_and_proximity(self):
        recommendations = self.recommendation_system.recommend_restaurants("Italian", "Downtown")
        self.assertEqual(recommendations, ["-> Sorriso Italian (Rating: 4.5)", "-> The Blue Plate (Rating: 4.4)",
                                           "-> Little Italy (Rating: 4.2)", "-> La Gustosa (Rating: 4.1)"])

    def test_slightly_misstyped_proximity_and_food_type(self):
        recommendations = self.recommendation_system.recommend_restaurants("Itallian", "Downton")
        self.assertEqual(recommendations, ["-> Sorriso Italian (Rating: 4.5)", "-> The Blue Plate (Rating: 4.4)",
                                           "-> Little Italy (Rating: 4.2)", "-> La Gustosa (Rating: 4.1)"])

    def test_invalid_food_type(self):
        food_type = "Canadian"
        proximity = "Suburb"
        recommendations = self.recommendation_system.recommend_restaurants(food_type, proximity)
        self.assertEqual(recommendations, f"Sorry, no recommendations found for {food_type}. Please enter a valid food type.")

    def test_invalid_proximity_input(self):
        # Test case for invalid proximity input
        with patch('builtins.input', side_effect=['InvalidCity', 'Suburb', 'Italian']):
            food_type, user_location = restaurant_recommendation.get_input(self.recommendation_system)

        # Verify that the food type is accepted after the third attempt
        self.assertEqual(food_type, 'Italian')
        # Verify that the valid location is accepted after the second attempt
        self.assertEqual(user_location, 'Suburb')

    def test_recommendations_for_unknown_food_type_with_correction(self):
        # Test case where the user enters an unknown food type with a correction suggestion
        with patch('builtins.input', side_effect=['Suburb','Meksican']):
            food_type, user_location = restaurant_recommendation.get_input(self.recommendation_system)

        # Verify that the corrected food type is accepted
        self.assertEqual(food_type, 'Mexican')

    def test_get_input_valid_values(self):
        # Test case for valid user inputs
        with patch('builtins.input', side_effect=['Downtown', 'Italian']):
            food_type, user_location = restaurant_recommendation.get_input(self.recommendation_system)

        self.assertEqual(food_type, 'Italian')
        self.assertEqual(user_location, 'Downtown')

    def test_no_similar_food_type(self):
        # Test case where the user enters a non-existent or unrelated food type
        with patch('builtins.input', side_effect=['Zzzz']):
            food_type, user_location = restaurant_recommendation.get_input(self.recommendation_system)

        # Verify that the correct message is displayed
        self.assertIn("Sorry, no recommendations found for Zzzz. Please enter a valid food type.",
                      self.capturedOutput.getvalue())

if __name__ == "__main__":
    unittest.main()
