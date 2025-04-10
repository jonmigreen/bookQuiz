from typing import List
from ..models.book import Book

class DataLoader:
    """A utility class for loading book data from markdown files."""
    
    @staticmethod
    def parse_books(markdown_content: str) -> List[Book]:
        """Parse books from markdown content.
        
        Args:
            markdown_content (str): The content of the books markdown file
            
        Returns:
            List[Book]: A list of parsed Book objects
        """
        books = []
        current_book = None
        current_title = None
        
        for line in markdown_content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line[0].isdigit() and '.' in line:
                # New book entry
                if current_book:
                    books.append(current_book)
                    
                current_title = line.split('. ', 1)[1]
                current_book = {
                    'title': current_title,
                    'age_group': '',
                    'support_types': set(),
                    'learning_style': '',
                    'diverse_communities': set()
                }
            elif current_book:
                if line.startswith('Age Group:'):
                    current_book['age_group'] = line.split(': ')[1].lower()
                elif line.startswith('Support Type:'):
                    current_book['support_types'].add(line.split(': ')[1])
                elif line.startswith('Learning Style:'):
                    current_book['learning_style'] = line.split(': ')[1]
                elif line.startswith('Diverse Communities:'):
                    current_book['diverse_communities'].add(line.split(': ')[1])
                    
        if current_book:
            books.append(current_book)
            
        return [
            Book(
                title=book['title'],
                age_group=book['age_group'],
                support_types=book['support_types'],
                learning_style=book['learning_style'],
                diverse_communities=book['diverse_communities']
            )
            for book in books
        ] 