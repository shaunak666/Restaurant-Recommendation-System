from fuzzywuzzy import process


class RestaurantRecommendationSystem:
    def __init__(self):
        """Store the data about restaurants in a Dictionary
        The key represents the type of food while the value associated with the key is
        a dictionary where keys are restaurant names, and values are a tuple of (ratings, proximity)"""
        self.restaurants = {
            "Indian": {
                "Hotel Balaji": (4.5, "Downtown"),
                "Rosewood": (4.2, "Suburb"),
                "Purnabrahma": (4.7, "Downtown"),
                "Hotel Savali": (4.0, "Suburb"),
                "Ratnalok": (4.3, "Downtown"),
                "Annapoorna": (4.1, "Suburb"),
                "Vaishali Restaurant": (4.6, "Downtown"),
                "Savya Rasa": (4.8, "Suburb"),
                "Puran da Dhaba": (4.4, "Downtown"),
            },
            "Italian": {
                "Little Italy": (4.2, "Downtown"),
                "Squisito": (4.0, "Suburb"),
                "Sorriso Italian": (4.5, "Downtown"),
                "Boun Cibo - The Italian Cafe": (4.3, "Suburb"),
                "La Gustosa": (4.1, "Downtown"),
                "Toscano Pune": (4.6, "Suburb"),
                "The Blue Plate": (4.4, "Downtown"),
            },
            "Chinese": {
                "Sizzling China": (3.8, "Downtown"),
                "Jagdamb Chinese Corner": (4.1, "Suburb"),
                "The Chinese House": (4.3, "Downtown"),
                "The Tasty Wok": (4.0, "Suburb"),
                "Ruchi Chinese": (4.2, "Downtown"),
                "Samarth Chinese": (4.5, "Suburb"),
                "Ni Hao China": (4.4, "Downtown"),
            },
            "Japanese": {
                "Kinki Kitchen": (4.7, "Downtown"),
                "Soy Samurai": (4.6, "Suburb"),
                "Asia Seven": (4.5, "Downtown"),
                "Umami": (4.4, "Suburb"),
                "Sushi Mushi": (4.3, "Downtown"),
                "The Sushi Factory": (4.2, "Suburb"),
                "Koji": (4.6, "Downtown"),
                "Shizusan": (4.7, "Suburb"),
                "Ichiraku's Bistro": (4.5, "Downtown"),
                "Mamagoto": (4.4, "Suburb"),
            },
            "Mexican": {
                "Taco Alfresco": (4.2, "Downtown"),
                "Taco Bell": (4.4, "Suburb"),
                "Taco Modiapps": (4.0, "Downtown"),
                "Rojo Nueve": (4.3, "Suburb"),
                "Senorita's": (4.1, "Downtown"),
                "The Mexican Wrap": (4.5, "Suburb"),
                "Iya's Mexican Kitchen": (4.6, "Downtown"),
                "The Mexican Tapas": (4.4, "Suburb"),
            }
        }

    def recommend_restaurants(self, food_type, user_location):
        try:
            # Search for the "food_type" in the dictionary and fetch the dictionary of restaurants, ratings, and proximity
            restaurants_data = self.restaurants[food_type]

            # Filter restaurants based on proximity
            filtered_recommendations = {restaurant: (rating, proximity) for restaurant, (rating, proximity) in
                                        restaurants_data.items() if proximity == user_location}

            # Check if there are no restaurants in the specified proximity
            if not filtered_recommendations:
                return []

            # Sort the filtered recommendations based on ratings
            sorted_recommendations = sorted(filtered_recommendations.items(), key=lambda x: x[1][0], reverse=True)

            # Extract only the restaurant names for recommendations
            recommended_restaurants = [f"-> {restaurant} (Rating: {rating})" for restaurant, (rating, proximity) in sorted_recommendations]

            return recommended_restaurants
        except KeyError:
            # Handle the situation where the user enters a wrong spelling for a food type
            suggestions = self.correct_food_type_typo(food_type)
            return suggestions



    def correct_proximity_typo(self, mistyped_proximity):
        #The proximity could also be typed wrong by the user so we need to check
        #if there is any kind of typo in the proximity
        valid_proximities = ["Downtown", "Suburb"]
        suggestions = process.extractOne(mistyped_proximity, valid_proximities)

        if suggestions and suggestions[1] >= 50:
            return suggestions[0]
        else:
            return None

    def correct_food_type_typo(self, mistyped_food_type):
        # This function tries to search for a similar food type to the wrong input
        # Suppose the user types "India" or "Mezican" then we should give the user a prompt
        # The prompt should tell the user "Did you mean Indian?" or "Did you mean Mexican?"
        food_types = list(self.restaurants.keys())
        suggestions = process.extractOne(mistyped_food_type, food_types)
        # The mistyped input should at least resolve  70% with one of the cuisines in dictonary
        if suggestions and suggestions[1] >= 70:
            return suggestions[0]
        else:
            return None

def get_input(recommendation_system):
    while True:
        # Get User Input for proximity
        user_location = input("Enter your location (Downtown or Suburb): ")
        corrected_location = recommendation_system.correct_proximity_typo(user_location)
        if corrected_location:
            break
        else:
            print(f"Invalid proximity: {user_location}. Please enter a valid proximity.")

    while True:
        # Get User Input for food type
        food_type = input("Enter the type of food you want: ")

        # Check if food_type is None (i.e., correction not found)
        if food_type not in recommendation_system.restaurants:
            corrected_food_type = recommendation_system.correct_food_type_typo(food_type)
            if corrected_food_type:
                print(f"Did you mean {corrected_food_type}?")
                # Set food_type to the corrected value
                food_type = corrected_food_type
            else:
                print(f"Sorry, no recommendations found for {food_type}. Please enter a valid food type.")
                continue

        break

    return food_type, corrected_location


def main():
    recommendation_system = RestaurantRecommendationSystem()

    food_type, user_location = get_input(recommendation_system)

    recommendations = recommendation_system.recommend_restaurants(food_type, user_location)

    if recommendations is not None:
        if not recommendations:
            print(f"No restaurants found in {user_location} for {food_type}. Please try a different proximity.")
        else:
            print(f"Recommended restaurants for {food_type} cuisine with ratings and proximity:")
            for restaurant in recommendations:
                print(restaurant)


if __name__ == "__main__":
    main()