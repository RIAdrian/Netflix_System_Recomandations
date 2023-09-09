import pandas as pd
import requests

# Replace with your OMDB API key
api_key = 'YOUR_OMDB_API_KEY'

# Read the original CSV file
df = pd.read_csv('netflix_titles.csv')

# Function to GET IMDb rating for a movie/TV show
def get_imdb_rating(title):
    try:
        # API request to OMDB
        url = f'http://www.omdbapi.com/?t={title}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        # Check if the API response contains a valid rating
        if 'imdbRating' in data and data['imdbRating'] != 'N/A':
            return float(data['imdbRating'])
        else:
            return None
    except Exception as e:
        print(f"Error fetching rating for {title}: {e}")
        return None

df['imdb_rating'] = df['title'].apply(get_imdb_rating)

df.to_csv('movies_with_imdb_ratings.csv', index=False)

print("IMDb ratings fetched and saved to 'movies_with_imdb_ratings.csv'")
