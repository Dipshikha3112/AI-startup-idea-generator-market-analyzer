# 🚀 AI Startup Idea Generator + Market Analyzer

> 📌 **Note**: All source code files are in the `master` branch.

This Streamlit app generates innovative startup ideas and provides market analysis for user-specified domains (e.g., EdTech) and regions (e.g., India, college students). It leverages the Hugging Face Inference API to generate 10 unique startup ideas using LLMs and provides market scope, revenue potential, target audience, competitors, and saturation level with interactive visualizations.

---

## ✨ Features

- 💡 **Idea Generator**: Uses `mistralai/Mistral-7B-Instruct-v0.3` with 5 fallback models for reliable LLM-based generation.
- 📊 **Market Analyzer**: Provides insights like scope, audience, revenue potential, top competitors, and market saturation.
- 🧠 **Idea Details**: Breaks down each idea into problem, solution, revenue model, and marketing strategy.
- 📂 **Save & Export**: Save ideas as `.json` or export as a `.md` report.
- 🕒 **Idea History**: View past generated and saved startup ideas with timestamps.
- 🧰 **Advice Section**: Offers actionable startup advice including tools, domains, and funding tips.
- 🔄 **Fallback & Error Handling**: Auto-switches between models and competitors for reliability.

---

## 🧰 Prerequisites

- Python ≥ 3.8
- Hugging Face API token (free or PRO account)
- Recommended: Use a virtual environment

### 🧪 Dependencies

```bash
streamlit==1.39.0
plotly==5.24.1
huggingface_hub==0.24.7
requests==2.32.3
beautifulsoup4==4.12.3
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd ai-startup-idea-generator
```

### 2. Set Up Virtual Environment

```bash
python -m venv ai_startup_env
# Activate it:
# Windows:
.i_startup_env\Scriptsctivate
# macOS/Linux:
source ai_startup_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Hugging Face Token

### Option 1: Directly in `app.py`

```python
client = InferenceClient(token="hf_your_actual_token")
```

### Option 2: Secure via `.streamlit/secrets.toml`

```
HF_TOKEN = "hf_your_actual_token"
```

And access it via:
```python
client = InferenceClient(token=st.secrets["HF_TOKEN"])
```

---

## 📂 File Structure

```
ai-startup-idea-generator/
├── app.py                # Main Streamlit app
├── prompts.py            # Prompt logic for LLMs
├── market_analyzer.py    # Market analysis functions
├── utils/
│   └── scraper.py        # Competitor scraper via DuckDuckGo
├── data/
│   └── ideas.json        # Saved ideas
├── .streamlit/
│   └── secrets.toml      # (optional) Hugging Face Token
└── README.md             # This file
```

---

## ▶️ Usage

```bash
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💬 Supported Models

The app automatically rotates among these models:

- `mistralai/Mistral-7B-Instruct-v0.3` ✅
- `meta-llama/Llama-3.2-3B-Instruct`
- `mistralai/Mixtral-8x7B-Instruct-v0.1`
- `google/gemma-2-9b-it`
- `EleutherAI/gpt-neo-2.7B`
- `bigscience/bloom-7b1`

---

## 🧪 Troubleshooting

- **402 Payment Required**: Use a backup model or upgrade token.
- **No competitors found**: Try again with broader queries. DuckDuckGo is used for scraping.
- **Too few ideas**: Relax filtering or increase `max_attempts` in `app.py`.
- **API credit issue**: Check Hugging Face dashboard or use local transformers model.

---

## 🧪 Local Model (Optional)

```bash
pip install transformers torch
```

```python
from transformers import pipeline
generator = pipeline("text2text-generation", model="google/flan-t5-base")
print(generator("Generate one EdTech idea", max_length=200))
```

---

## 🧑‍💻 Developer's Note

🎓 *I'm building this project as part of my AI & LLM learning journey.*  
💡 It integrates real-world APIs, LLMs, and data visualizations to simulate entrepreneurial use-cases.  
🙏 Feedback and suggestions are welcome!



## 📬 Contact

For bugs, suggestions, or collaborations, please create a GitHub issue or reach out via Linkedin


--Dipshikha
