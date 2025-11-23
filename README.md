🎤 Speech Scoring Tool – Cohere + Streamlit

An AI-powered tool that evaluates a student's spoken introduction transcript based on content, clarity, engagement, and structure.

✨ Features

🧠 Semantic similarity using Cohere embeddings

📌 Keyword detection

🎯 Flow scoring (greeting → intro → core → ending)

✨ Clarity scoring using filler-word analysis

📊 Score visualization using Plotly

🟩 Keyword highlighting

🎛 Simple Streamlit interface

📦 Installation
pip install streamlit cohere numpy scikit-learn plotly

🚀 Run the App
streamlit run app.py

🔧 Configuration

Set your Cohere API key:

cohere_api_key = "YOUR_API_KEY"

📜 How It Works

Extracts keywords

Detects speech flow

Calculates filler rate

Generates embeddings

Computes cosine similarity

Produces weighted overall score

📊 Output

Overall score

Content, clarity, engagement

Flow score

Semantic similarity

Graphs + colored keyword tags

JSON breakdown

