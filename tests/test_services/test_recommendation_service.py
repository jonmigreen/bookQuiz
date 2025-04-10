from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock.plugin import MockerFixture

from src.models.book import Book
from src.models.quiz import QuizAnswers
from src.services.recommendation_service import RecommendationService

def test_recommendation_service_creation():
    """Test that RecommendationService can be created with a list of books."""
    books = [
        Book(
            title="Test Book 1",
            age_group="adult",
            support_types={"Healing from past trauma"},
            learning_style="Stories and personal experiences",
            diverse_communities={"General"}
        ),
        Book(
            title="Test Book 2",
            age_group="teen",
            support_types={"Managing stress"},
            learning_style="Clear, practical advice I can use in my own life",
            diverse_communities={"General"}
        )
    ]
    
    service = RecommendationService(books)
    assert len(service.books) == 2

def test_get_recommendations():
    """Test that recommendations are returned in correct order and format."""
    books = [
        Book(
            title="Perfect Match",
            age_group="adult",
            support_types={"Healing from past trauma", "Managing stress"},
            learning_style="Stories and personal experiences",
            diverse_communities={"General"}
        ),
        Book(
            title="Partial Match",
            age_group="adult",
            support_types={"Healing from past trauma"},
            learning_style="Clear, practical advice I can use in my own life",
            diverse_communities={"General"}
        ),
        Book(
            title="No Match",
            age_group="teen",
            support_types={"Building self-confidence"},
            learning_style="Activities like journaling or mindfulness",
            diverse_communities={"General"}
        )
    ]
    
    service = RecommendationService(books)
    quiz_answers = QuizAnswers(
        age_group="adult",
        support_types={"Healing from past trauma", "Managing stress"},
        learning_style="Stories and personal experiences",
        wants_diverse=False
    )
    
    recommendations = service.get_recommendations(quiz_answers, limit=2)
    
    assert len(recommendations) == 2
    assert recommendations[0]["title"] == "Perfect Match"
    assert recommendations[0]["score"] > recommendations[1]["score"]
    assert "age_group" in recommendations[0]
    assert "support_types" in recommendations[0]
    assert "learning_style" in recommendations[0]
    assert "diverse_communities" in recommendations[0] 