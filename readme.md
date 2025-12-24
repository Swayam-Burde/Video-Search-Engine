# ⚡ VideoIQ Pro

**Next-Gen Video Intelligence Platform**

VideoIQ Pro is an AI-powered video analysis dashboard that transforms raw video content into searchable, actionable intelligence. By leveraging multimodal AI (Audio + Vision), it allows users to perform semantic searches, extract exact spoken quotes, and generate narrative summaries from video files or YouTube links.

---

## 🚀 Features

* **🎥 Dual-Mode Ingestion**: Drag-and-drop local files (MP4/MP3) or paste a YouTube URL.
* **🔎 Semantic Search**: Search your video using natural language (e.g., *"Show me the red car"* or *"When do they talk about pricing?"*).
* **🧠 Multimodal Analysis**:
    * **Visual Search**: Uses CLIP-based embeddings to find specific visual scenes.
    * **Audio Intelligence**: Transcribes speech (Whisper) and performs semantic search on spoken content.
* **📝 AI Summarization**: Generates structured, context-aware summaries using the Groq LLaMA 3 70B model.
* **⚡ Real-time Processing**: Dynamic progress tracking for downloading, transcription, and embedding generation.

---

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/) (Custom CSS styling)
* **LLM Engine**: [Groq API](https://groq.com/) (Llama-3-70b-versatile)
* **Vision Model**: CLIP (Contrastive Language-Image Pre-Training) via `sentence-transformers`
* **Audio Model**: OpenAI Whisper
* **Vector Database**: [Qdrant](https://qdrant.tech/) (Local instance)
* **Video Processing**: `moviepy`, `yt-dlp`

---

## ⚙️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/VideoIQ-Pro.git](https://github.com/YOUR_USERNAME/VideoIQ-Pro.git)
    cd VideoIQ-Pro
    ```

2.  **Install dependencies**
    *(Recommended: Use a virtual environment)*
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys**
    You need a Groq API key for the summarization feature.
    * Create a `.env` file or set it as an environment variable: `GROQ_API_KEY=your_key_here`
    * Alternatively, enter it directly in the script (not recommended for production).

---

## 🏃‍♂️ Usage

Run the application locally:

```bash
streamlit run app.py