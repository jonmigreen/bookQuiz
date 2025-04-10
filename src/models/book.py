from dataclasses import dataclass
from typing import Set

@dataclass
class Book:
    """A book that can be recommended based on user preferences.
    
    Attributes:
        title (str): The title of the book
        age_group (str): The target age group (child, teen, or adult)
        support_types (Set[str]): The types of support the book provides
        learning_style (str): The learning style the book uses
        diverse_communities (Set[str]): The diverse communities represented in the book
    """
    title: str
    age_group: str
    support_types: Set[str]
    learning_style: str
    diverse_communities: Set[str]

    def calculate_score(self, quiz_answers: 'QuizAnswers') -> float:
        """Calculate how well this book matches the user's preferences.
        
        Scoring breakdown:
        - Age group match: 1 point
        - Support type matches: 1 point each (max 2 points)
        - Learning style match: 1 point
        - Diverse communities match: 1 point for specific community match,
          0.25 points for general representation if diverse is desired,
          0.5 points if general representation is acceptable without specific community
        
        The final score is normalized to a 0-1 range by dividing by 5.0.
        
        Args:
            quiz_answers (QuizAnswers): The user's quiz answers
            
        Returns:
            float: A score between 0 and 1 indicating how well the book matches
        """
        score = 0.0
        
        # Age group match (1 point)
        if self.age_group.lower() == quiz_answers.age_group.lower():
            score += 1.0
            
        # Support type matches (1 point each, max 2 points)
        support_matches = len(self.support_types.intersection(quiz_answers.support_types))
        score += min(support_matches, 2.0)  # Cap at 2 points
        
        # Learning style match (1 point)
        if self.learning_style == quiz_answers.learning_style:
            score += 1.0
            
        # Diverse communities match
        if quiz_answers.wants_diverse:
            if quiz_answers.specific_community and quiz_answers.specific_community in self.diverse_communities:
                score += 1.0  # Exact match for specific community
            elif "General" in self.diverse_communities:
                score += 0.25  # General representation if specific community desired
        elif "General" in self.diverse_communities:
            score += 0.5  # General representation is acceptable
            
        # Normalize to 0-1 range
        return score / 5.0 