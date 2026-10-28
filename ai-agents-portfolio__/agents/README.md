# AI Business Agents: 14 Simple Streamlit Apps

Each folder is one agent (its own GitHub repository). Every app is a single `app.py` that generates sample data, analyses it and shows results.

## Run one agent
```
cd marketing-budget-optimizer
pip install -r requirements.txt
streamlit run app.py
```
(Needs Python 3.9+.)

## Folders
Marketing: marketing-budget-optimizer, churn-retention-intelligence, marketing-revenue-attribution, ai-customer-segmentation
HR: attrition-rootcause-intelligence, workforce-skill-gap-intelligence, productivity-workload-analyzer
Operations: supply-chain-disruption-predictor, predictive-maintenance-ai, inventory-optimization-agent, delivery-performance-rootcause
Analytics: executive-decision-intelligence, profitability-decline-investigator, what-if-business-simulator

## Fastest way: upload all 14 at once
1. Install Git (git-scm.com) and GitHub CLI (cli.github.com).
2. Run `gh auth login` and follow the prompts (log in with the browser).
3. In this folder run `./push_all.sh` (Mac/Linux/Git Bash) or `.\push_all.ps1` (Windows PowerShell).
It creates 14 public repos on your account and pushes each folder.

## Or do it manually, one agent at a time
1. On github.com click + > New repository. Name it exactly like the folder. Public. Do NOT add a README (the folder already has one).
2. In a terminal inside that folder:
```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/FOLDER-NAME.git
git push -u origin main
```

## Free live demo (optional)
Sign in at share.streamlit.io with GitHub, pick the repository, set the main file to `app.py`, and deploy. Paste the link in the repository's About section.

## What the apps do NOT do (be honest in your report)
They use synthetic data and simple rules/models. Nothing here calls an LLM. For problems 4 and 12 (which mention LLMs) you can add an optional LLM step later that explains the calculated numbers.
