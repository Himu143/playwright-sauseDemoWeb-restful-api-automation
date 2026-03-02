# Playwright
# Web & API Automation Project

This repository contains automated tests for both web UI (SauceDemo) and RESTful API (Restful Booker) using Python-based frameworks.

## 🔧 Tools & Technologies

- **Python 3** – primary programming language
- **pytest** – test runner and framework
- **Playwright** – browser automation for UI tests
- **requests** – HTTP client for API interactions
- **pytest-html** – generate HTML reports

## 🚀 How to Run the Project

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Playwright_Task_SQA
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv playwright-env
   source playwright-env/bin/activate   # Linux/macOS
   # or playwright-env\\Scripts\\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install   # download browser binaries
   ```

## 🧪 Running Tests

- **API tests only**
  ```bash
  pytest tests/test_restful_api.py -v
  ```

- **Web (UI) tests only**
  ```bash
  PYTHONPATH=. pytest tests/test_sauce.py --headed --html=report.html
  ```


Reports will be generated in the workspace root (e.g., `report.html`).

## ✅ Project Structure

```
├── pages/                # page object models for UI and API helpers
│   ├── sauce_pages.py
│   └── restfulapi_page.py
├── tests/                # pytest test modules
│   ├── test_sauce.py
│   └── test_restful_api.py
├── requirements.txt      # Python dependencies
├── README.md             # (this file)
└── api_responses.log     # logged API request/response details
```
## **Report**
Web Automation Report:
<img width="1900" height="1039" alt="image" src="https://github.com/user-attachments/assets/0ef008a8-b31a-425d-98d5-8beb56f86de3" />


API Automation Report:
<img width="1900" height="1039" alt="image" src="https://github.com/user-attachments/assets/5f4efbce-0d97-4f2b-ac6f-5baf107f4d11" />
<img width="1900" height="1039" alt="image" src="https://github.com/user-attachments/assets/90366343-4a4a-4fd7-b692-676d49350f90" />


