from dataclasses import dataclass
from typing import Set, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QuizAnswers:
    """A class representing a user's quiz answers.
    
    Attributes:
        age_group (str): The user's age group preference
        support_types (Set[str]): Set of support types the user is interested in
        learning_style (str): The user's preferred learning style
        wants_diverse (bool): Whether the user wants diverse representation
        specific_community (Optional[str]): The specific community of interest if wants_diverse is True
    """
    age_group: str
    support_types: Set[str]
    learning_style: str
    wants_diverse: bool
    specific_community: Optional[str] = None
    
    @classmethod
    def from_form_data(cls, form_data: dict) -> 'QuizAnswers':
        """Create a QuizAnswers instance from form data.
        
        Args:
            form_data (dict): The form data from the quiz submission
            
        Returns:
            QuizAnswers: A new QuizAnswers instance
        """
        logger.info("\nProcessing quiz form data:")
        logger.info(f"Raw form data: {dict(form_data)}")
        
        # Handle support_types which can be multiple values
        support_types = form_data.getlist('support_types') if hasattr(form_data, 'getlist') else form_data.get('support_types', [])
        if isinstance(support_types, str):
            support_types = [support_types]
            
        # Get wants_diverse and specific_community from form data
        wants_diverse_value = form_data.get('wants_diverse', '').lower()
        wants_diverse = wants_diverse_value in ['true', 'yes', '1', 'on']
        specific_community = form_data.get('specific_community') if wants_diverse else None
        
        logger.info(f"Processed support types: {support_types}")
        logger.info(f"Wants diverse value: {wants_diverse_value}")
        logger.info(f"Wants diverse: {wants_diverse}")
        logger.info(f"Specific community: {specific_community}\n")
            
        return cls(
            age_group=form_data.get('age_group', '').lower(),
            support_types=set(support_types),
            learning_style=form_data.get('learning_style', ''),
            wants_diverse=wants_diverse,
            specific_community=specific_community
        ) 