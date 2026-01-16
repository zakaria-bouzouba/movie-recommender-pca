from flask import Flask, render_template, request
from recommender import PCARecommender

app = Flask(__name__)

# Initialize recommender globally (Load once, serve many)
rec_engine = PCARecommender()
rec_engine.load_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    error = None
    search_query = ""

    if request.method == 'POST':
        search_query = request.form.get('movie_name', '').strip()
        
        # Input Validation
        if not search_query:
            error = "Please enter a movie name."
        elif len(search_query) > 100:
            error = "Input too long."
        else:
            results = rec_engine.recommend(search_query)
            if results:
                recommendations = results
            else:
                error = f"Movie '{search_query}' not found in database. Try exact spelling (e.g., 'Toy Story (1995)')."

    return render_template('index.html', recommendations=recommendations, error=error, last_search=search_query)

if __name__ == '__main__':
    # Debug=True is okay for dev, NEVER for production
    app.run(debug=True, port=5000)