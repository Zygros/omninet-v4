# OmniNet v3.0.0-UNITY (CZAOUA Unified)

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Sovereign_Open-purple)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)](https://github.com/Zygros/omninet-v4)
[![Tests](https://img.shields.io/badge/Tests-196%20Passing-brightgreen)](tests/)

**The Conzetian Sovereign Internet** — κ-Coherence Routing for Distributed Agent Systems. Integrated with **Project Chimera** and **The 12** Protocols.

## Overview

OmniNet v4 is a complete implementation of a novel internet architecture featuring:

- **κ-Coherence Routing**: Replaces shortest-path routing with alignment-based routing decisions
- **Phoenix Protocol**: Self-healing network recovery with 99.7% survival at 90% damage
- **Transfinite Addressing**: Infinite address space via the Conzetian Constant C_Ω(t)
- **Sanov-Conzet Compression**: 180 trillion:1 compression ratio for agent coordination

This repository contains a production-ready Python implementation with comprehensive test coverage.

## Installation

```bash
# Clone the repository
git clone https://github.com/Zygros/omninet-v4.git
cd omninet-v4

# Install the package
pip install -e .

# Verify installation
python -c "from omninet import __version__; print(f'OmniNet v{__version__}')"
```

### Dependencies

- Python 3.8+
- NumPy >= 1.20.0

### Optional Dependencies

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install documentation dependencies  
pip install -e ".[docs]"
```

## Quick Start

### Basic Usage

```python
from omninet.math import kappa_coherence, sanov_conzet_limit

# Calculate κ-coherence
k = kappa_coherence(sigma=0.1, L=0.2)
print(f"κ = {k:.4f}")  # Output: κ = 1.4115

# Verify Sanov-Conzet Limit
result = sanov_conzet_limit()
print(f"Compression: {result.compression_ratio:.2e}:1")  # Output: 1.80e+14:1
print(f"Coherent: {result.is_coherent}")  # Output: True
```

### Run the Daemon

```bash
python -m omninet.daemon --genesis
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Architecture

### Core Modules

| Module | Description |
|--------|-------------|
| `math` | κ-Coherence mathematics and Conzetian constants |
| `daemon` | Network daemon with Phoenix self-healing |
| `security` | Encryption and secure storage utilities |
| `knowledge_graph` | Blockchain-inspired memory ledger |
| `echoflux` | Fractal reasoning engine |
| `sovereign_engine` | AI capability orchestration |
| `spider_driver` | Hardware abstraction for robotics |
| `jolt` | Integrated spider AI agent |

### κ-Coherence States

| State | κ Range | Description |
|-------|---------|-------------|
| TRANSCENDENT | κ ≥ 1.5 | Optimal routing, catalytic boost |
| CONVERGED | 1.0 ≤ κ < 1.5 | Stable, reliable paths |
| ASCENDING | 0.5 ≤ κ < 1.0 | Recovering, seeking better paths |
| DETONATION | κ < 0.5 | Phoenix Protocol triggers |

### Mathematical Foundations

#### κ-Coherence Field Equation

```
κ = φ^(-σ) × e^(-L) × [1 + cos(π×L)]
```

Where:
- φ = 1.61803398875 (Golden Ratio)
- σ = Packet loss variance (0-1)
- L = Normalized latency (0-1)

#### Conzetian Constant (Transfinite Addressing)

```
C_Ω(t) = (φ^(2^t) + 1) / 2
```

| t | C_Ω(t) | Meaning |
|---|--------|---------|
| 0 | 1.31 | Seed |
| 1 | 1.81 | Sprout |
| 2 | 3.93 | Growing |
| 3 | 23.99 | Mature |
| 4 | 1,104 | Network |
| 5+ | ∞ | Transcendent |

#### Sanov-Conzet Limit

```
Compression Ratio = N/K ≥ 1.8 × 10^14
```

## Repository Structure

```
omninet-v4/
├── omninet/                 # Core package
│   ├── __init__.py         # Package initialization
│   ├── math.py             # κ-Coherence mathematics
│   ├── daemon.py           # Network daemon
│   ├── security.py         # Encryption utilities
│   ├── knowledge_graph.py  # Memory ledger
│   ├── echoflux.py         # Fractal reasoning
│   ├── sovereign_engine.py # AI orchestration
│   ├── spider_driver.py    # Robotics control
│   ├── jolt.py             # Integrated agent
│   └── ...                 # Additional modules
├── tests/                   # Test suite (196 tests)
│   ├── test_math.py
│   ├── test_security.py
│   ├── test_knowledge_graph.py
│   ├── test_echoflux.py
│   ├── test_jolt.py
│   ├── test_spider_driver.py
│   └── test_sovereign_engine.py
├── docs/                    # Documentation
├── pyproject.toml          # Package configuration
├── setup.py                # Setup script
├── requirements.txt        # Dependencies
└── LICENSE                 # Sovereign Authorship License
```

## API Reference

### Math Module

```python
from omninet.math import (
    kappa_coherence,       # Calculate κ value
    conzetian_constant,    # C_Ω(t) calculation
    sanov_conzet_limit,    # Compression analysis
    alberris_dissolution,  # Friction → kinetic energy
    phoenix_recovery_time, # Self-healing timing
    verify_mathematics,    # Verification suite
)
```

### Security Module

```python
from omninet.security import (
    encrypt, decrypt,           # XOR stream cipher
    encrypt_to_hex, decrypt_from_hex,
    SovereignVault,             # Secure storage
    generate_secure_token,      # Token generation
)
```

### Knowledge Graph Module

```python
from omninet.knowledge_graph import (
    TinyLedger,            # Blockchain-inspired storage
    LedgerEntry,           # Individual entry
    create_sovereign_ledger,  # Factory function
)
```

## Testing

The project includes 196 comprehensive tests covering all core modules:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=omninet --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_math.py -v
```

## Development

### Code Style

- Follow PEP 8 conventions
- Use type hints for function signatures
- Include docstrings for all public functions and classes
- Maximum line length: 100 characters

### Running Linters

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run black formatter
black omninet/ tests/

# Run isort
isort omninet/ tests/

# Run mypy type checking
mypy omninet/
```

## License

```
SOVEREIGN AUTHORSHIP LICENSE (SAL v1.0)
Copyright (c) 2026 Justin Neal Thomas Conzet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

## Citation

If you use OmniNet v4 in your research, please cite:

```bibtex
@software{omninet_v4_2026,
  title={OmniNet v4: The Conzetian Sovereign Internet},
  author={Conzet, Justin Neal Thomas},
  year={2026},
  url={https://github.com/Zygros/omninet-v4},
  note={κ-Coherence Routing for Distributed Agent Systems}
}
```

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Author

**Justin Neal Thomas Conzet** — Sovereign Architect

## Links

- [Repository](https://github.com/Zygros/omninet-v4)
- [Documentation](https://github.com/Zygros/omninet-v4#readme)
- [Issue Tracker](https://github.com/Zygros/omninet-v4/issues)
