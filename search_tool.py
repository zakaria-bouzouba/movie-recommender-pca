import pandas as pd
import sys

# Load just the movies file for speed
df = pd.read_csv('data/ml-latest-small/movies.csv')

def search_movie(query):
    # Search for the string (case insensitive)
    results = df[df['title'].str.contains(query, case=False, na=False)]
    
    if results.empty:
        print(f"\nNo movies found matching '{query}'")
    else:
        print(f"\nFound {len(results)} matches:")
        print("-" * 40)
        # Print top 10 results
        for title in results['title'].head(10):
            print(title)
        print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_tool.py <partial_name>")
        print("Example: python search_tool.py star")
    else:
        # Join arguments to handle spaces (e.g. "star wars")
        search_term = " ".join(sys.argv[1:])
        search_movie(search_term)