# Contributing to Universal-Market-Scanner

We welcome pull requests from quantitative developers, algorithmic traders, and backend engineers.

## Development Workflow
1. Fork the repository and create your feature branch (`git checkout -b feat/scanner-orderbook-imbalance`).
2. Ensure code passes syntax and linting checks:
   ```bash
   flake8 src cli.py main.py --count --select=E9,F63,F7,F82,F824
   ```
3. Test terminal scanner suite:
   ```bash
   python cli.py demo
   ```
4. Submit a descriptive Pull Request referencing any open issue.
