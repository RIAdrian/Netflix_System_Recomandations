import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

#read the database 
database_csv = pd.read_csv('netflix_titles.csv')

#obtain the name of headers
header_names = database_csv.columns

# Calculate the number of movies and TV shows
num_movies = database_csv[database_csv['type'] == 'Movie'].shape[0]
num_tv_shows = database_csv[database_csv['type'] == 'TV Show'].shape[0]

# Create a list with the counts of movies and TV shows
counts = [num_movies, num_tv_shows]

# Labels for the pie chart
labels = ['Movies', 'TV Shows']

# Create a pie chart with percentages
plt.figure(figsize=(6, 6))
plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Percentage of Movies and TV Shows')
plt.axis('equal')  # Ensure the chart looks circular
plt.show()
# End of code 


# Find unique directors and count how many movies/TV shows each director has directed
movie_directors = database_csv[database_csv['type'] == 'Movie']['director'].str.split(', ').explode().value_counts()
tv_show_directors = database_csv[database_csv['type'] == 'TV Show']['director'].str.split(', ').explode().value_counts()

# Combine the results to get the total number of movies and TV shows for each director
total_directors = movie_directors.add(tv_show_directors, fill_value=0).astype(int)

# Open a text file for writing the results
with open('directors_results.txt', 'w') as file:
    for director, num_movies in total_directors.items():
        file.write(f"Director: {director}\n")
        file.write(f"Total Movies/TV Shows Directed: {num_movies}\n")
        movies = database_csv[(database_csv['director'].str.contains(director)) & (database_csv['type'] == 'Movie')]['title'].tolist()
        tv_shows = database_csv[(database_csv['director'].str.contains(director)) & (database_csv['type'] == 'TV Show')]['title'].tolist()
        if movies:
            file.write("Movies Directed:\n")
            for movie in movies:
                file.write(f"- {movie}\n")
        if tv_shows:
            file.write("TV Shows Directed:\n")
            for tv_show in tv_shows:
                file.write(f"- {tv_show}\n")
        file.write('\n')

print("Results have been saved to 'directors_results.txt'.")

# End of code


# Initialize a dictionary to store actor information
actors_info = {}

# Iterate through each row and split the 'cast' column by comma for non-missing values
for index, row in database_csv[database_csv['cast'].notna()].iterrows():
    cast_list = row['cast'].split(', ')
    for actor in cast_list:
        actor = actor.strip()  # Remove leading/trailing spaces
        if actor in actors_info:
            actors_info[actor]['appearances'] += 1
            actors_info[actor]['movies'].append(row['title'])
        else:
            actors_info[actor] = {'appearances': 1, 'movies': [row['title']]}

# Sort actors by the number of appearances in descending order
sorted_actors = sorted(actors_info.items(), key=lambda x: x[1]['appearances'], reverse=True)

# Open a text file for writing the results
with open('actors_results.txt', 'w') as file:
    for actor, info in sorted_actors:
        file.write(f"Actor: {actor}\n")
        file.write(f"Number of Appearances: {info['appearances']}\n")
        file.write("Movies/TV Shows:\n")
        for movie in info['movies']:
            file.write(f"- {movie}\n")
        file.write('\n')

print("Results have been saved to 'actors_results.txt'.")

# end of code 

# Split the 'listed_in' column to create a list of genres for each row
database_csv['listed_in'] = database_csv['listed_in'].str.split(', ')

# Create a list of all genres
all_genres = [genre for sublist in database_csv['listed_in'] for genre in sublist]

# Count the occurrences of each genre
genre_counts = pd.Series(all_genres).value_counts()

# Create a bar chart
plt.figure(figsize=(12, 6))
genre_counts.plot(kind='bar')
plt.title('Number of Movies/TV Shows by Genre')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
plt.show()