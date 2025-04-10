from pathlib import Path
from src.utils.data_loader import DataLoader
from src.utils.combination_analyzer import CombinationAnalyzer

def main():
    """Run the combination analysis and generate a report."""
    # Load books data
    books_file = Path(__file__).parent.parent / 'books.md'
    with open(books_file, 'r') as f:
        books = DataLoader.parse_books(f.read())
    
    # Analyze combinations
    analyzer = CombinationAnalyzer(books)
    analyzer.analyze_all_combinations()
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save report
    report_file = Path(__file__).parent.parent / 'results.md'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"Analysis complete. Report saved to {report_file}")

if __name__ == '__main__':
    main() 