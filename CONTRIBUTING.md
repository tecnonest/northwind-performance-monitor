# Contributing to Northwind Performance Monitor

Thank you for your interest in contributing to Northwind Performance Monitor! We welcome contributions from the community.

## 🚀 How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/YOUR_USERNAME/northwind-performance-monitor.git
cd northwind-performance-monitor
```

### 2. Set Up Development Environment
```bash
# Start the development stack
docker-compose up -d

# Install Python dependencies
cd performance-monitor
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Make Your Changes
- Create a feature branch: `git checkout -b feature/amazing-feature`
- Make your changes
- Add tests if applicable
- Update documentation

### 4. Code Quality
```bash
# Format code
black app/
isort app/

# Run tests
pytest

# Check linting
flake8 app/
```

### 5. Submit Pull Request
- Push your changes: `git push origin feature/amazing-feature`
- Create a Pull Request with a clear description

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use Black for code formatting
- Use type hints where possible
- Write clear, descriptive commit messages

### Testing
- Add tests for new features
- Ensure all tests pass before submitting
- Test your changes with the full Docker stack

### Documentation
- Update README.md if needed
- Add docstrings to new functions
- Update API documentation

## 🐛 Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Docker version, etc.)
- Relevant logs or error messages

## 💡 Feature Requests

For new features:
- Describe the use case
- Explain why it would be valuable
- Consider implementation complexity
- Discuss in Issues before starting work

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Focus on constructive feedback
- Follow the Code of Conduct

## 📞 Questions?

- Open an Issue for discussion
- Check existing Issues and Discussions
- Review the documentation

Thank you for contributing! 🎉
