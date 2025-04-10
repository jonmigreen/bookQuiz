from typing import List, Dict, Optional
from ..models.book import Book
from ..models.quiz import QuizAnswers

class RecommendationService:
    """A service for generating book recommendations based on user preferences."""
    
    def __init__(self, books: List[Book]):
        """Initialize the recommendation service with a list of books.
        
        Args:
            books (List[Book]): The list of books to recommend from
        """
        self.books = books
        
    def get_recommendations(self, quiz_answers: QuizAnswers, limit: Optional[int] = 4) -> List[Dict]:
        """Get book recommendations based on quiz answers.
        
        Args:
            quiz_answers (QuizAnswers): The user's quiz answers
            limit (Optional[int]): The maximum number of recommendations to return.
                                 If None, returns all books.
            
        Returns:
            List[Dict]: A list of recommended books with their scores
        """
        # First filter books by age group
        age_group_books = [
            book for book in self.books 
            if book.age_group.lower() == quiz_answers.age_group.lower()
        ]
        
        # Calculate scores only for books in the correct age group
        scored_books = [
            {
                'book': book,
                'score': book.calculate_score(quiz_answers)
            }
            for book in age_group_books
        ]
        
        # Sort by score in descending order
        scored_books.sort(key=lambda x: x['score'], reverse=True)
        
        # Convert to response format
        books_to_process = scored_books if limit is None else scored_books[:limit]
        result = [
            {
                'title': book['book'].title,
                'age_group': book['book'].age_group,
                'support_types': list(book['book'].support_types),
                'learning_style': book['book'].learning_style,
                'diverse_communities': list(book['book'].diverse_communities),
                'score': book['score']
            }
            for book in books_to_process
        ]
        
        return result 