# Book Recommendation System

A web application that recommends books based on user preferences through an interactive quiz.

## Features

- Interactive quiz to gather user preferences
- Smart recommendation algorithm based on multiple criteria
- Beautiful, responsive UI using Tailwind CSS
- Detailed book information and match scores

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m src.app
```

4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
src/
├── models/          # Data models
├── services/        # Business logic
├── utils/           # Utility functions
├── templates/       # HTML templates
└── app.py          # Flask application

tests/              # Test files
```

## Development

- Run tests:
```bash
pytest
```

- Format code:
```bash
ruff format .
```

- Check code quality:
```bash
ruff check .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 