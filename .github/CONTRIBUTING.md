# Contributing to OmniNet v4

First off, thank you for considering contributing to OmniNet v4! It's people like you that make OmniNet such a great sovereign internet protocol.

## 📜 Sovereign Decrees

All contributions must adhere to the Four Sovereign Decrees:

1. **ALWAYS ADD, NEVER TAKE** — Your contributions must add value
2. **ALWAYS DO, NEVER DON'T** — Execute with purpose
3. **SOLVE FRICTION BEFORE CONTINUING** — Address obstacles constructively
4. **JUDGE ONLY AFTER EXECUTION** — Provide feedback after implementation

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or uv package manager
- Git

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/omninet-v4.git
cd omninet-v4

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Verify mathematics
python -c "from omninet.math import verify_mathematics; print(verify_mathematics())"
```

## 📝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear title and description**
- **Rationale** (why is this needed?)
- **Proposed implementation** (if you have ideas)
- **Mathematical justification** (if applicable)

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** with clear commit messages
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Ensure tests pass**: `pytest tests/ -v`
6. **Submit pull request**

#### PR Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] No new warnings introduced

## 🎨 Code Style

We use the following tools:

- **Black** for formatting
- **isort** for import sorting
- **mypy** for type checking
- **flake8** for linting

```bash
# Format code
black omninet tests

# Sort imports
isort omninet tests

# Type check
mypy omninet

# Lint
flake8 omninet
```

## 📖 Documentation

- Use **docstrings** for all public functions/classes
- Follow **NumPy docstring style**
- Update **README.md** for user-facing changes
- Add **inline comments** for mathematical derivations

### Example Docstring

```python
def kappa_coherence(sigma: float, L: float) -> float:
    """
    κ-Coherence Field Equation.
    
    Calculates the coherence metric for network routing.
    
    Parameters
    ----------
    sigma : float
        Packet loss variance (0-1)
    L : float
        Normalized latency (0-1)
    
    Returns
    -------
    float
        κ value bounded in [0, 2]
    
    Examples
    --------
    >>> kappa_coherence(0.1, 0.2)
    1.411513...
    """
```

## 🧪 Testing

We maintain high test coverage. Please:

- Write **unit tests** for new functions
- Write **integration tests** for modules
- Test **edge cases** (κ bounds, chaos levels)
- Test **mathematical properties** (monotonicity, bounds)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=omninet --cov-report=html

# Run specific test file
pytest tests/test_math.py -v
```

## 📐 Mathematical Contributions

For contributions involving mathematics:

1. **Reference the original formula** in comments
2. **Provide derivation** if novel
3. **Add verification tests** with known values
4. **Document units and bounds**

## 🏛️ Architecture Changes

For significant architecture changes:

1. **Open an issue first** to discuss
2. **Document the design decision**
3. **Consider backward compatibility**
4. **Update ARCHITECTURE.md**

## 📜 License

By contributing, you agree that your contributions will be licensed under the Sovereign Authorship License (SAL v1.0).

---

**κ = ∞ | This Is The Way**

*Thank you for contributing to sovereign internet infrastructure!*
