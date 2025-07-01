import streamlit as st
import json
from datetime import datetime
from prompts import get_idea_prompt, get_business_canvas_prompt
from market_analyzer import analyze_market
import plotly.express as px
from huggingface_hub import InferenceClient
import hashlib
import time

# Initialize Hugging Face client
#client = InferenceClient(token="USE token")  # Removed for secuitt purose as github doesn't allow it

# List of fallback models
MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "meta-llama/Llama-3.2-3B-Instruct",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "google/gemma-2-9b-it",
    "EleutherAI/gpt-neo-2.7B",
    "bigscience/bloom-7b1"
]

# Streamlit app
st.set_page_config(page_title="AI Startup Idea Generator", layout="wide")
st.title("AI Startup Idea Generator + Market Analyzer")

# Idea Generator Section
st.header("💡 Idea Generator")
user_interest = st.text_input("Enter your field of interest (e.g., healthcare, edtech):", value="edtech")
region = st.text_input("Target region or audience (e.g., USA, Gen Z):", value="india, college students")
num_ideas = 10  # Set to 10 as requested
if st.button("Generate Ideas"):
    if user_interest and region:
        prompt = get_idea_prompt(user_interest, region)
        with st.spinner("Generating ideas..."):
            ideas = []
            idea_hashes = set()
            attempts = 0
            max_attempts = 50  # Increased for more unique ideas
            retries = 3  # Retry on API failure
            model_index = 0  # Start with primary model
            while len(ideas) < num_ideas and attempts < max_attempts:
                current_model = MODELS[model_index]
                for _ in range(retries):
                    try:
                        idea = client.text_generation(
                            prompt=prompt,
                            model=current_model,
                            max_new_tokens=200,
                            temperature=1.2,
                            top_p=0.95,
                            top_k=50
                        )
                        # Clean and process idea
                        idea_text = idea.strip().split('\n')
                        for line in idea_text:
                            if len(ideas) >= num_ideas:
                                break
                            clean_idea = line.strip("•-1234567890. ")
                            if clean_idea and len(clean_idea) > 20:  # Ensure meaningful ideas
                                idea_hash = hashlib.md5(clean_idea.encode()).hexdigest()
                                if idea_hash not in idea_hashes:
                                    ideas.append(clean_idea)
                                    idea_hashes.add(idea_hash)
                        break
                    except Exception as e:
                        if "402 Client Error: Payment Required" in str(e):
                            model_index += 1  # Switch to next model
                            if model_index >= len(MODELS):
                                st.error("All models exhausted due to API credit limits. Please upgrade to a PRO account or try again later.")
                                break
                            st.warning(f"API error for {current_model}: {e}. Switching to {MODELS[model_index]}...")
                        else:
                            st.warning(f"API error for {current_model}: {e}. Retrying...")
                        time.sleep(2)
                if model_index >= len(MODELS):
                    break
                attempts += 1
            if len(ideas) < num_ideas:
                st.warning(f"Generated only {len(ideas)} unique ideas after {max_attempts} attempts.")
            st.session_state["current_ideas"] = [{
                "idea": idea,
                "interest": user_interest,
                "region": region,
                "timestamp": str(datetime.now())
            } for idea in ideas]
        st.write("**Generated Ideas**:")
        for i, idea in enumerate(ideas, 1):
            st.write(f"**Idea {i}**: {idea}")
    else:
        st.error("Please enter both interest and region.")

# Market Analyzer Section
st.header("📈 Market Analyzer")
if st.button("Analyze Market") and "current_ideas" in st.session_state:
    with st.spinner("Analyzing market..."):
        market_data = analyze_market(user_interest, region)
        st.write(f"**Market Scope**: {market_data['scope']}")
        st.write(f"**Estimated Revenue Potential**: {market_data['estimated_revenue']}")
        st.write(f"**Target Audience Size**: {market_data['target_audience']}")
        st.write(f"**Competitor Count**: {market_data['count']}")
        st.write(f"**Top Competitors**: {', '.join(market_data['competitors']) if market_data['competitors'] else 'No competitors found'}")
        st.session_state["market_analysis"] = market_data

        # Bar Chart
        if market_data["competitors"]:
            fig = px.bar(x=market_data["competitors"], y=[1]*len(market_data["competitors"]), title="Top Competitors")
            st.plotly_chart(fig)
        else:
            st.warning("No competitors found; bar chart not displayed.")

        # Pie Chart for Saturation
        fig_pie = px.pie(names=["Saturated", "Unsaturated"], values=[market_data["count"], max(100 - market_data["count"], 0)], title="Market Saturation")
        st.plotly_chart(fig_pie)

# Advice Section
st.header("🛠️ Advice for Starting Your Edtech Venture")
if "current_ideas" in st.session_state:
    st.write("""
    **Next Steps**:
    - **Validate Your Idea**: Conduct surveys or interviews with college students in India to confirm demand. Use platforms like Google Forms (forms.google.com) or Typeform (typeform.com).
    - **Build a Prototype**: Create a minimum viable product (MVP) using no-code platforms like Bubble (bubble.io) or Adalo (adalo.com) to test your concept.
    - **Domain Registration**: Secure a domain name via:
      - **GoDaddy** (godaddy.com, starting at ~$10/year).
      - **Namecheap** (namecheap.com, ~$9/year).
      - **Google Domains** (domains.google, ~$12/year).
    - **Free Website Tools**:
      - **Wix** (wix.com): Free drag-and-drop website builder with templates for edtech platforms.
      - **WordPress.com** (wordpress.com): Free hosting with customizable themes, ideal for blogs or course platforms.
      - **Webflow** (webflow.com): Free tier for responsive websites with advanced design control.
      - **Carrd** (carrd.co): Free for simple, one-page sites, perfect for landing pages.
      - **Google Sites** (sites.google.com): Free for basic websites with easy integration.
    - **Marketing**: Leverage social media (Instagram, LinkedIn) targeting Indian college students. Use Canva (canva.com) for visuals and Mailchimp (mailchimp.com) for email campaigns.
    - **Funding**: Explore angel investors or platforms like StartUp India (startupindia.gov.in) for grants. Pitch to edtech accelerators like GSV Ventures or Edugild.
    - **Compliance**: Ensure compliance with India’s National Education Policy (NEP) 2020 for content and accessibility.
    - **Tech Stack**: Use Firebase (firebase.google.com) for authentication, AWS (aws.amazon.com) for hosting, and Stripe (stripe.com) for payments. Consider open-source LMS like Moodle (moodle.org).
    """)

# Idea Details Section
st.header("🧠 Idea Details")
if "current_ideas" in st.session_state:
    for i, idea_data in enumerate(st.session_state["current_ideas"], 1):
        st.subheader(f"Idea {i}: {idea_data['idea'][:50]}...")
        tabs = st.tabs([f"Idea {i} - Problem", f"Idea {i} - Solution", f"Idea {i} - Revenue", f"Idea {i} - Marketing"])
        for j, section in enumerate(["problem", "solution", "revenue", "marketing"]):
            with tabs[j]:
                prompt = get_business_canvas_prompt(idea_data["idea"], section)
                with st.spinner(f"Generating {section} for Idea {i}..."):
                    details = client.text_generation(
                        prompt=prompt,
                        model=MODELS[model_index],  # Use the last successful model
                        max_new_tokens=150
                    )
                st.write(details)

# Save and Export
st.header("🗃️ Save & Export")
if "current_ideas" in st.session_state:
    if st.button("Save Ideas"):
        try:
            with open("data/ideas.json", "r") as f:
                ideas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            ideas = []
        ideas.extend(st.session_state["current_ideas"])
        with open("data/ideas.json", "w") as f:
            json.dump(ideas, f, indent=4)
        st.success("Ideas saved!")

    if st.button("Export as Markdown"):
        content = f"# Startup Ideas\n\n**Interest**: {user_interest}\n**Region**: {region}\n\n"
        for i, idea_data in enumerate(st.session_state["current_ideas"], 1):
            content += f"## Idea {i}\n{idea_data['idea']}\n"
        if "market_analysis" in st.session_state:
            content += (
                f"\n## Market Analysis\n"
                f"**Scope**: {st.session_state['market_analysis']['scope']}\n"
                f"**Estimated Revenue Potential**: {st.session_state['market_analysis']['estimated_revenue']}\n"
                f"**Target Audience Size**: {st.session_state['market_analysis']['target_audience']}\n"
                f"**Competitors**: {', '.join(st.session_state['market_analysis']['competitors']) if st.session_state['market_analysis']['competitors'] else 'No competitors found'}\n"
                f"**Saturation**: {st.session_state['market_analysis']['saturation']}\n"
            )
        st.download_button("Download Report", content, file_name="ideas_report.md", mime="text/markdown")

# Idea History
st.header("📌 Idea History")
try:
    with open("data/ideas.json", "r") as f:
        ideas = json.load(f)
    for idea in ideas:
        st.write(f"**{idea['timestamp']}** - {idea['interest']} ({idea['region']}): {idea['idea']}")
except (FileNotFoundError, json.JSONDecodeError):
    st.write("No ideas saved yet.")