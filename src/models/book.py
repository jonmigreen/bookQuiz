from dataclasses import dataclass
from typing import Set
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        - Age group match: 1 point (mandatory filter)
        - Support type matches: 0.5 points per match (max 1 point for 2 matches)
        - Learning style match: 1 point
        - Diverse communities match: 1 point for specific community match,
          0.25 points for general representation if diverse is desired,
          0.5 points if general representation is acceptable
        
        The final score is normalized to a 0-1 range by dividing by 4.0.
        
        Args:
            quiz_answers (QuizAnswers): The user's quiz answers
            
        Returns:
            float: A score between 0 and 1 indicating how well the book matches
        """
        score = 0.0
        
        logger.info(f"\nScoring book: {self.title}")
        logger.info(f"Quiz answers: age={quiz_answers.age_group}, support={quiz_answers.support_types}, style={quiz_answers.learning_style}")
        logger.info(f"Diverse: wants={quiz_answers.wants_diverse}, community={quiz_answers.specific_community}")
        logger.info(f"Book communities: {self.diverse_communities}")
        
        # Age group match (1 point) - mandatory filter
        if self.age_group.lower() == quiz_answers.age_group.lower():
            score += 1.0
            logger.info("Age group match: +1.0")
        else:
            logger.info("Age group mismatch: returning 0")
            return 0.0
            
        # Support type matches (0.5 points per match, max 1 point)
        matches = self.support_types.intersection(quiz_answers.support_types)
        support_score = min(len(matches) * 0.5, 1.0)  # Cap at 1.0 point
        if support_score > 0:
            score += support_score
            logger.info(f"Support type matches {matches}: +{support_score}")
        
        # Learning style match (1 point)
        if self.learning_style == quiz_answers.learning_style:
            score += 1.0
            logger.info("Learning style match: +1.0")
            
        # Diverse communities match
        if quiz_answers.wants_diverse:
            if quiz_answers.specific_community:
                # Only give point for exact community match
                if quiz_answers.specific_community in self.diverse_communities:
                    score += 1.0
                    logger.info(f"Specific community match ({quiz_answers.specific_community}): +1.0")
                else:
                    logger.info(f"No specific community match for {quiz_answers.specific_community}")
            else:
                # Give points for general representation if no specific community requested
                if "General" in self.diverse_communities:
                    score += 0.5
                    logger.info("General representation match: +0.5")
        
        final_score = score / 4.0
        logger.info(f"Final score: {final_score}\n")
        return final_score 