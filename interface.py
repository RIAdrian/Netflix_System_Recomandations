import tkinter as tk
import pandas as pd
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Read data from the CSV file
data = pd.read_csv('netflix_titles.csv')

# Combine selected columns into a single text column and replace NaN with an empty string
data['combined'] = data['type'] + ' ' + data['title'] + ' ' + data['director'] + ' ' + data['cast'] + ' ' + data['country'] + ' ' + data['date_added'] + ' ' + data['release_year'].astype(str) + ' ' + data['rating'] + ' ' + data['duration'] + ' ' + data['listed_in'] + ' ' + data['description'].fillna('')

# Function for searching by keywords
def search_by_keywords():
    keywords = keywords_entry.get().strip()
    if not keywords:
        messagebox.showerror("Error", "Please enter keywords for the search.")
        return

    # Replace NaN values with an empty string in the 'combined' column
    data['combined'] = data['combined'].fillna('')

    # Calculate TF-IDF vectors for the combined text
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined'])

    # Calculate cosine similarities between keywords and descriptions
    keyword_vector = tfidf_vectorizer.transform([keywords])
    cosine_similarities = linear_kernel(keyword_vector, tfidf_matrix)

    # Get top recommendations based on cosine similarities
    top_indices = cosine_similarities.argsort()[0][-10:][::-1]
    top_recommendations = data.iloc[top_indices]

    # Hide the search button and keywords entry
    search_button.grid_forget()
    keywords_entry.grid_forget()

    # Display the "Back to Search" button
    back_button.grid(row=2, column=0, columnspan=4, pady=(10, 0))

    # Create a new frame for displaying recommendations using pack()
    recommendations_frame = tk.Frame(frame)
    recommendations_frame.grid(row=3, column=0, columnspan=4, pady=10)

    # Display the top recommendations with clickable titles
    for title_data in top_recommendations.itertuples(index=False):
        title_label = tk.Label(recommendations_frame, text=title_data.title, cursor="hand2")
        title_label.bind("<Button-1>", lambda event, data=title_data: on_title_click(data._asdict()))
        title_label.pack()

# Function to display the top 10 recommendations
def get_top_results(dataframe):
    if dataframe.empty:
        return "No results found."

    results_message = "Top 10 recommended results:\n"
    for index, row in dataframe.iterrows():
        results_message += f"{row['title']} - Score: {row['score']}\n"
    return results_message

def back_to_search():
    # Hide the "Back to Search" button and results
    back_button.grid_forget()
    results_label.config(text="")

    # Display the search button and keywords entry again
    search_button.grid(row=2, column=0, columnspan=4, pady=(10, 0))
    keywords_entry.grid(row=1, column=0, columnspan=4, pady=(10, 0))

def show_title_details(title_data):
    details_window = tk.Toplevel(root)
    details_window.title(title_data['title'])

    # Add widgets to display detailed information about the title in the details window
    detail_labels = [
        f"Type: {title_data['type']}",
        f"Title: {title_data['title']}",
        f"Director: {title_data['director']}",
        f"Cast: {title_data['cast']}",
        f"Country: {title_data['country']}",
        f"Date Added: {title_data['date_added']}",
        f"Release Year: {title_data['release_year']}",
        f"Rating: {title_data['rating']}",
        f"Duration: {title_data['duration']}",
        f"Listed In: {title_data['listed_in']}",
        f"Description: {title_data['description']}"
    ]

    for detail_label in detail_labels:
        label = tk.Label(details_window, text=detail_label)
        label.pack()

def on_title_click(title_data):
    show_title_details(title_data)

# Create the main window
root = tk.Tk()
root.title("Netflix Recommendation App")

# Display the window in the center of the screen
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a frame for organizing GUI elements
frame = tk.Frame(root)
frame.pack(pady=20)

# Text for asking the user's query
query_label = tk.Label(frame, text="What would you like to watch?")
query_label.grid(row=0, column=0, columnspan=4)

# Entry field for entering keywords
keywords_entry = tk.Entry(frame)
keywords_entry.grid(row=1, column=0, columnspan=4, pady=(10, 0))

# Button for searching
search_button = tk.Button(frame, text="Search", command=search_by_keywords, height=2, width=10)
search_button.grid(row=2, column=0, columnspan=4, pady=(10, 0))

# Label for displaying results
results_label = tk.Label(frame, text="", justify="left")
results_label.grid(row=3, column=0, columnspan=4, pady=10)

# Button to go back to the search screen
back_button = tk.Button(frame, text="Back to Search", command=back_to_search, height=2, width=15)

# Configure additional alignment and anchors
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.rowconfigure(3, weight=1)

# Start the main application loop
root.mainloop()
