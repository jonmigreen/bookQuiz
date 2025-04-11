from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
from .models.quiz import QuizAnswers
from .services.recommendation_service import RecommendationService
from .utils.data_loader import DataLoader
import signal
import sys

app = Flask(__name__)

# Load books data
books_file = Path(__file__).parent.parent / 'books.md'
with open(books_file, 'r') as f:
    books = DataLoader.parse_books(f.read())

recommendation_service = RecommendationService(books)

@app.route('/')
def index():
    """Render the quiz page."""
    return render_template('quiz.html')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get book recommendations based on quiz answers."""
    try:
        quiz_answers = QuizAnswers.from_form_data(request.form)
        # Get all books with their scores
        all_books = recommendation_service.get_recommendations(quiz_answers, limit=None)
        # Sort books by score in descending order
        all_books.sort(key=lambda x: x['score'], reverse=True)
        return jsonify({
            'top_recommendations': all_books[:4],  # Top 4 recommendations
            'all_books': all_books  # All books with scores
        })
    except Exception as e:
        print(f"Error processing recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Get port from environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

def signal_handler(sig, frame):
    print('\nShutting down gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port) 