from typing import List, Dict, Set
from src.models.quiz import QuizAnswers
from src.models.book import Book
from src.services.recommendation_service import RecommendationService
from src.utils.data_loader import DataLoader

class CombinationAnalyzer:
    """Analyzes all possible combinations of quiz answers and their resulting recommendations."""
    
    # Define all possible values for each quiz question
    AGE_GROUPS = ["child", "teen", "adult"]
    SUPPORT_TYPES = [
        "Healing from past trauma",
        "Managing stress",
        "Building self-confidence",
        "Navigating and managing emotions"
    ]
    LEARNING_STYLES = [
        "Stories and personal experiences",
        "Clear, practical advice I can use in my own life",
        "Interesting science and mental health guidance from experts",
        "Activities like journaling or mindfulness"
    ]
    DIVERSE_OPTIONS = [True, False]
    COMMUNITIES = [
        "Black",
        "Native",
        "Latino",
        "Middle Eastern",
        "2SLGBTQIA+",
        "Women"
    ]

    def __init__(self, books: List[Book]):
        """Initialize the analyzer with a list of books.
        
        Args:
            books (List[Book]): The list of books to analyze
        """
        self.books = books
        self.recommendation_service = RecommendationService(books)
        self.low_result_combinations: List[Dict] = []

    def analyze_all_combinations(self) -> None:
        """Analyze all possible combinations of quiz answers."""
        for age_group in self.AGE_GROUPS:
            # Generate all possible pairs of support types
            for i in range(len(self.SUPPORT_TYPES)):
                for j in range(i + 1, len(self.SUPPORT_TYPES)):
                    support_types = {self.SUPPORT_TYPES[i], self.SUPPORT_TYPES[j]}
                    
                    for learning_style in self.LEARNING_STYLES:
                        for wants_diverse in self.DIVERSE_OPTIONS:
                            if wants_diverse:
                                for community in self.COMMUNITIES:
                                    self._analyze_combination(
                                        age_group, support_types, learning_style, 
                                        wants_diverse, community
                                    )
                            else:
                                self._analyze_combination(
                                    age_group, support_types, learning_style, 
                                    wants_diverse, None
                                )

    def _analyze_combination(
        self,
        age_group: str,
        support_types: Set[str],
        learning_style: str,
        wants_diverse: bool,
        specific_community: str
    ) -> None:
        """Analyze a specific combination of quiz answers.
        
        Args:
            age_group (str): The selected age group
            support_types (Set[str]): The selected support types
            learning_style (str): The selected learning style
            wants_diverse (bool): Whether diverse representation is desired
            specific_community (str): The specific community if diverse representation is desired
        """
        quiz_answers = QuizAnswers(
            age_group=age_group,
            support_types=support_types,
            learning_style=learning_style,
            wants_diverse=wants_diverse,
            specific_community=specific_community
        )
        
        recommendations = self.recommendation_service.get_recommendations(quiz_answers, limit=None)
        
        if len(recommendations) < 4:
            self.low_result_combinations.append({
                "quiz_answers": {
                    "age_group": age_group,
                    "support_types": list(support_types),
                    "learning_style": learning_style,
                    "wants_diverse": wants_diverse,
                    "specific_community": specific_community
                },
                "recommendation_count": len(recommendations),
                "recommendations": recommendations
            })

    def generate_report(self) -> str:
        """Generate a markdown report of combinations with fewer than 4 recommendations.
        
        Returns:
            str: A markdown formatted report
        """
        report = "# Quiz Answer Combinations with Fewer than 4 Recommendations\n\n"
        
        for combination in self.low_result_combinations:
            report += f"## Combination {self.low_result_combinations.index(combination) + 1}\n\n"
            report += "### Quiz Answers:\n"
            report += f"- Age Group: {combination['quiz_answers']['age_group']}\n"
            report += f"- Support Types: {', '.join(combination['quiz_answers']['support_types'])}\n"
            report += f"- Learning Style: {combination['quiz_answers']['learning_style']}\n"
            report += f"- Wants Diverse: {combination['quiz_answers']['wants_diverse']}\n"
            if combination['quiz_answers']['specific_community']:
                report += f"- Specific Community: {combination['quiz_answers']['specific_community']}\n"
            report += f"\n### Number of Recommendations: {combination['recommendation_count']}\n\n"
            report += "### Recommended Books:\n"
            for book in combination['recommendations']:
                report += f"- {book['title']} (Score: {book['score']:.2%})\n"
            report += "\n---\n\n"
        
        return report 