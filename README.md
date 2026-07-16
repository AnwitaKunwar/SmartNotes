# College Notes AI

A Streamlit application for building a lightweight Retrieval-Augmented Generation (RAG) workflow for PDF study notes.

## Features
- Upload one or more PDF notes
- Extract text from PDFs
- Clean and chunk content for retrieval
- Retrieve relevant passages using semantic-style similarity
- Answer questions using retrieved context

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Optional: set an OpenAI API key in a `.env` file to enable GPT-powered answers.

## Deploy on GitHub / public hosting
This project is structured for public deployment through GitHub-backed platforms such as Streamlit Community Cloud.

### What is ready for deployment
- [app.py](app.py) is the main entry point.
- [requirements.txt](requirements.txt) contains the runtime dependencies.
- [.streamlit/config.toml](.streamlit/config.toml) binds the app to `0.0.0.0` for hosted environments.
- [Procfile](Procfile) enables container-style deployment setups.
- [.github/workflows/ci.yml](.github/workflows/ci.yml) runs automated tests on push.
- [runtime.txt](runtime.txt) pins the Python version for hosting platforms.

### Deployment steps
1. Push this repository to GitHub.
2. Open your hosting platform and connect the repo.
3. Set the app entry point to `app.py`.
4. Ensure the environment has Python and the dependencies from [requirements.txt](requirements.txt).
5. Optional: add `OPENAI_API_KEY` as a secret for GPT-powered answers.

### GitHub push checklist
- Initialize Git if needed: `git init`
- Add files: `git add .`
- Commit: `git commit -m "Initial College Notes AI app"`
- Create a GitHub repo and connect it: `git remote add origin <your-repo-url>`
- Push: `git push -u origin main`

## Project structure
- [app.py](app.py) – Streamlit frontend and RAG workflow
- [requirements.txt](requirements.txt) – Python dependencies
- [tests/](tests/) – basic regression tests for chunking and retrieval
