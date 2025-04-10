from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock.plugin import MockerFixture

from src.models.book import Book
from src.models.quiz import QuizAnswers

def test_book_creation():
    """Test that a Book can be created with all required attributes."""
    book = Book(
        title="Test Book",
        age_group="adult",
        support_types={"Healing from past trauma"},
        learning_style="Stories and personal experiences",
        diverse_communities={"General"}
    )
    
    assert book.title == "Test Book"
    assert book.age_group == "adult"
    assert "Healing from past trauma" in book.support_types
    assert book.learning_style == "Stories and personal experiences"
    assert "General" in book.diverse_communities

def test_book_score_calculation():
    """Test that book scores are calculated correctly based on quiz answers."""
    book = Book(
        title="Test Book",
        age_group="adult",
        support_types={"Healing from past trauma", "Managing stress"},
        learning_style="Stories and personal experiences",
        diverse_communities={"General"}
    )
    
    quiz_answers = QuizAnswers(
        age_group="adult",
        support_types={"Healing from past trauma", "Managing stress"},
        learning_style="Stories and personal experiences",
        wants_diverse=False
    )
    
    score = book.calculate_score(quiz_answers)
    assert score == 1.0  # Perfect match should give 100% score
    
    # Test with different age group
    quiz_answers.age_group = "teen"
    score = book.calculate_score(quiz_answers)
    assert score < 1.0  # Different age group should reduce score 