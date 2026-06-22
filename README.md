# Email Generator

An AI-powered Email Generator built using Python, LangChain, and Ollama. This application creates professional, personalized, and context-aware emails based on user requirements. It also generates professional summaries that can be used to enrich email content and improve personalization.

## Features

* Generate professional summaries from user profiles
* Create personalized emails for various purposes
* Multiple tone options (Formal, Friendly, Assertive, Empathetic, Persuasive, etc.)
* Powered by Ollama and Llama models
* Context-aware email generation
* Showcase logging for generated content
* Easy-to-use interface and customizable prompts

## Technologies Used

* Python
* LangChain
* Ollama
* Llama 3.2
* Prompt Engineering
* JSON for data storage

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Ensure Ollama is installed and running:

```bash
ollama run llama3.2
```

## Run the Application

```bash
python app.py
```

or if using Streamlit:

```bash
streamlit run app.py
```

## Project Workflow

1. Collect sender information.
2. Generate a professional summary.
3. Build personalized sender context.
4. Generate professional emails.
5. Save session details to showcase logs.

## Use Cases

* Job Application Emails
* Networking Emails
* Follow-up Emails
* Client Communication
* Business Outreach
* Professional Introductions
* Internship Applications

## Future Improvements

* Streamlit Web Interface
* Export Emails to PDF
* Email Templates Library
* Multi-language Support
* Email History Dashboard

## Author

Developed as an AI-powered email generation project using LangChain and Ollama.
