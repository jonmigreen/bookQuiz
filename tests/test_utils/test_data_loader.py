from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock.plugin import MockerFixture

from src.utils.data_loader import DataLoader

def test_parse_books():
    """Test that books are correctly parsed from markdown content."""
    markdown_content = """
1. Test Book 1
Age Group: Adult
Support Type: Healing from past trauma
Learning Style: Stories and personal experiences
Diverse Communities: General

2. Test Book 2
Age Group: Teen
Support Type: Managing stress
Learning Style: Clear, practical advice I can use in my own life
Diverse Communities: General
"""
    
    books = DataLoader.parse_books(markdown_content)
    
    assert len(books) == 2
    assert books[0].title == "Test Book 1"
    assert books[0].age_group == "adult"
    assert "Healing from past trauma" in books[0].support_types
    assert books[0].learning_style == "Stories and personal experiences"
    assert "General" in books[0].diverse_communities
    
    assert books[1].title == "Test Book 2"
    assert books[1].age_group == "teen"
    assert "Managing stress" in books[1].support_types
    assert books[1].learning_style == "Clear, practical advice I can use in my own life"
    assert "General" in books[1].diverse_communities

def test_parse_books_with_multiple_support_types():
    """Test that books with multiple support types are correctly parsed."""
    markdown_content = """
1. Test Book
Age Group: Adult
Support Type: Healing from past trauma
Support Type: Managing stress
Learning Style: Stories and personal experiences
Diverse Communities: General
"""
    
    books = DataLoader.parse_books(markdown_content)
    
    assert len(books) == 1
    assert len(books[0].support_types) == 2
    assert "Healing from past trauma" in books[0].support_types
    assert "Managing stress" in books[0].support_types 