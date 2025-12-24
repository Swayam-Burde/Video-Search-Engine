import streamlit as st
import os
import time
from groq import Groq
from ml_engine.downloader import VideoDownloader
from ml_engine.processing import VideoProcessor
from ml_engine.audio import AudioTranscriber
from ml_engine.vision import VideoVision
from ml_engine.store import VectorDB

# --- 1. CONFIGURATION & ADVANCED STYLING ---
st.set_page_config(page_title="VideoIQ Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 THEME & ANIMATIONS INJECTION
st.markdown("""
    <style>
    /* 1. THE MOVING BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background: linear-gradient(-45deg, #fdfbfb, #ebedee, #f3e7e9, #e3eeff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. GLASSMORPHISM CARDS */
    /* REPLACE THE OLD .glass-card CSS WITH THIS: */
    .glass-card {
        background: #ffffff !important; /* Forces Solid White */
        border: 1px solid #e0e0e0;      /* Adds a clean grey border */
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        padding: 24px;
        margin-bottom: 24px;
    }

    /* 3. TEXT VISIBILITY FIX (Crucial) */
    h1, h2, h3, h4, h5, p, span, div {
        color: #333333 !important; /* Forces dark text */
        font-family: 'Inter', sans-serif;
    }
     
    /* Title Gradient Override */
    h2 {
        background: -webkit-linear-gradient(#4f46e5, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* 4. INPUT FIELD STYLING (Remove Black Boxes) */
    /* Text Input */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #333 !important;
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 12px;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 1px dashed rgba(0,0,0,0.2);
        border-radius: 12px;
        padding: 20px;
    }
    [data-testid="stFileUploader"] section {
        background-color: transparent !important; /* Removes inner black box */
    }
    [data-testid="stFileUploader"] button {
        background-color: #eee !important;
        color: #333 !important;
        border: none;
    }

    /* 5. BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white !important;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# API Key
GROQ_API_KEY = "Enter your GROQ API Key Here"

# Helper Function: Time Formatting
def format_time(seconds):
    minutes = int(seconds // 60)
    rem_seconds = int(seconds % 60)
    return f"{minutes}m {rem_seconds}s"

# --- 2. ENGINE SETUP ---
@st.cache_resource
def load_tools():
    return {
        "downloader": VideoDownloader(),
        "processor": VideoProcessor(),
        "audio": AudioTranscriber(),
        "vision": VideoVision(),
        "db": VectorDB(),
        "llm": Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    }

tools = load_tools()

# --- 3. STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = "landing"
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Navigation Functions
def go_to_main():
    st.session_state.page = "main"

def go_to_landing():
    st.session_state.page = "landing"
    st.session_state.analysis_complete = False

# ==========================================
# PAGE 1: LANDING PAGE (Animated)
# ==========================================
if st.session_state.page == "landing":
    
    # We use a container with the 'main-container' class to trigger the fade-in animation
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Spacing
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Glass Card for the Welcome Screen
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h1 style="font-size: 3.5rem; background: -webkit-linear-gradient(#4f46e5, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">VideoIQ</h1>
            <h3 style="color: #666; margin-top: -10px;">Next-Gen Video Intelligence</h3>
            <br>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Unlock the power of your video content. <br>
                Perform <b>semantic visual searches</b>, extract <b>spoken quotes</b>, 
                and generate <b>AI summaries</b> in seconds.
            </p>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        # Launch Button
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            st.button("Get Started", on_click=go_to_main, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True) # End Animation Container

# ==========================================
# PAGE 2: MAIN DASHBOARD (Animated)
# ==========================================
elif st.session_state.page == "main":
    
    # Animation Wrapper
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header Row with Back Button
    c1, c2 = st.columns([8, 1])
    with c1:
        st.markdown("## ⚡ VideoIQ Dashboard")
    with c2:
        if st.button("↩ Home"):
            go_to_landing()
            st.rerun()

    # --- 1. UPLOAD SECTION (Glass Cards) ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    # We hide the input section if analysis is done to keep it clean, or keep it to allow re-upload
    # Let's keep it but formatted nicely
    
    col_upload, col_link = st.columns(2, gap="large")
    
    file_path = None
    is_audio = False
    
    with col_upload:
        st.markdown("""<div class="glass-card"><h4>📂 Upload Local File</h4>""", unsafe_allow_html=True)
        uploaded = st.file_uploader("Drag and drop MP4/MP3", type=["mp4", "mp3", "wav"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded:
            os.makedirs("temp_data", exist_ok=True)
            save_path = os.path.join("temp_data", uploaded.name)
            with open(save_path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.session_state['temp_file_path'] = save_path
            st.session_state['temp_is_audio'] = uploaded.name.endswith(('mp3', 'wav'))
            st.success(f"Ready: {uploaded.name}")

    with col_link:
        st.markdown("""<div class="glass-card"><h4>🔗 YouTube Link</h4>""", unsafe_allow_html=True)
        yt_url = st.text_input("Paste URL here", placeholder="https://youtube.com/...", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if yt_url:
            st.session_state['yt_url'] = yt_url

    # --- ANALYZE BUTTON ---
    st.markdown("<br>", unsafe_allow_html=True)
    _, act_btn, _ = st.columns([3, 2, 3])
    with act_btn:
        start_analysis = st.button(" Analyze Content", use_container_width=True)

    # --- PROCESSING LOGIC ---
    # --- PROCESSING LOGIC (Updated with Progress Bar) ---
    # --- PROCESSING LOGIC (Updated for Smooth Dynamic Progress) ---
    if start_analysis:
        target_path = ""
        processing_audio_mode = False

        # 1. UI Setup: Progress Container
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Processing Video Intelligence")
        status_text = st.empty() 
        progress_bar = st.progress(0)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- STEP 1: DOWNLOAD (0% -> 10%) ---
        status_text.markdown("** Fetching media...**")
        if 'yt_url' in st.session_state and st.session_state['yt_url']:
            path, audio_mode = tools["downloader"].download_from_url(st.session_state['yt_url'])
            if not path:
                status_text.error("❌ Error: Download failed.")
                st.stop()
            target_path = path
            processing_audio_mode = audio_mode
        elif 'temp_file_path' in st.session_state:
            target_path = st.session_state['temp_file_path']
            processing_audio_mode = st.session_state['temp_is_audio']
        else:
            status_text.error("❌ Error: No file found.")
            st.stop()
        
        st.session_state['file_path'] = target_path
        st.session_state['is_audio'] = processing_audio_mode
        
        # Smooth fill to 10%
        for i in range(1, 11):
            progress_bar.progress(i)
            time.sleep(0.02) 

        # --- STEP 2: TRANSCRIPTION (10% -> 30%) ---
        status_text.markdown("** Transcribing audio track...**")
        # Reset DB first
        tools["db"].reset_db()
        clean_audio = tools["processor"].extract_audio(target_path)
        transcript = tools["audio"].transcribe(clean_audio)
        
        # Jump to 30% (Transcription is a single block process)
        progress_bar.progress(30)

        # --- STEP 3: AUDIO EMBEDDINGS (30% -> 50% SMOOTH LOOP) ---
        if transcript:
            status_text.markdown("** Processing speech intelligence...**")
            st.session_state['transcript_segments'] = transcript
            st.session_state['transcript_text'] = " ".join([s['text'] for s in transcript])
            
            # Process one by one for smooth bar movement
            total_segs = len(transcript)
            audio_vecs = []
            audio_payloads = []
            
            for idx, s in enumerate(transcript):
                # Generate embedding
                v = tools["vision"].get_text_embedding(s['text'])
                audio_vecs.append(v)
                audio_payloads.append({"timestamp": s['start'], "text": s['text'], "type": "speech"})
                
                # Calculate progress: Map 0-total_segs to 30-50 range
                prog = 30 + int((idx / total_segs) * 20)
                progress_bar.progress(prog)
            
            # Batch upload to DB
            tools["db"].upload_vectors(audio_vecs, audio_payloads, "audio_search")
        
        progress_bar.progress(50)

        # --- STEP 4: VISUAL PROCESSING (50% -> 100% SMOOTH LOOP) ---
        if not processing_audio_mode:
            status_text.markdown("** Analyzing visual frames (AI Vision)...**")
            
            # Extract Frames
            frames = tools["processor"].extract_keyframes(target_path, interval=1)
            
            if frames:
                total_frames = len(frames)
                frame_vecs = []
                frame_payloads = []
                
                # Loop through frames to update bar smoothly
                for idx, f in enumerate(frames):
                    # Generate embedding
                    v = tools["vision"].get_image_embedding(f)
                    frame_vecs.append(v)
                    frame_payloads.append({"timestamp": idx*1, "path": f, "type": "frame"})
                    
                    # Calculate progress: Map 0-total_frames to 50-100 range
                    prog = 50 + int((idx / total_frames) * 50)
                    progress_bar.progress(prog)
                
                tools["db"].upload_vectors(frame_vecs, frame_payloads, "visual_search")
        else:
            # If audio only, just fill to end
            status_text.info("Audio file detected. Skipping visual analysis.")
            progress_bar.progress(100)

        # FINISH
        progress_bar.progress(100)
        status_text.success("✅ Analysis Complete!")
        st.session_state.analysis_complete = True
        time.sleep(1)
        st.rerun()
        
        
    # ==========================================
    # RESULTS SECTION
    # ==========================================
    if st.session_state.analysis_complete:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Results Wrapper
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("###  Intelligence Results")
        
        # Video Player
        if 'file_path' in st.session_state:
            st.video(st.session_state['file_path'])

        tab1, tab2 = st.tabs(["🔎 Semantic Search", "📝 Smart Summary"])

        # --- TAB 1: SEARCH ---
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            query = st.text_input("Ask your video:", placeholder="e.g. 'Show me the part with the red car' or 'When do they talk about pricing?'")
            
            if query and tools["db"]:
                query_vec = tools["vision"].get_text_embedding(query)
                
                # --- VISUAL RESULTS ---
                if not st.session_state.get('is_audio', False):
                    st.markdown("##### 🖼️ Visual Matches")
                    results = tools["db"].search(query_vec, "visual_search", top_k=12)
                    
                    if results:
                        GRID_SIZE = 3 
                        for i in range(0, len(results), GRID_SIZE):
                            batch = results[i : i + GRID_SIZE]
                            cols = st.columns(GRID_SIZE)
                            for idx, hit in enumerate(batch):
                                timestamp = hit.payload['timestamp']
                                score = hit.score
                                time_str = format_time(timestamp)
                                
                                with cols[idx]:
                                    st.video(st.session_state['file_path'], start_time=int(timestamp))
                                    st.caption(f"**{time_str}**")
                    else:
                        st.info("No visual matches found.")
                    st.divider()

                # --- AUDIO RESULTS ---
                st.markdown("##### 🗣️ Audio Matches")
                found_audio = False
                
                # 1. Exact Match
                if 'transcript_segments' in st.session_state:
                    exact_matches = [s for s in st.session_state['transcript_segments'] if query.lower() in s['text'].lower()]
                    if exact_matches:
                        found_audio = True
                        st.success(f"Found {len(exact_matches)} exact spoken matches.")
                        for match in exact_matches[:5]:
                            time_str = format_time(match['start'])
                            with st.container():
                                c1, c2 = st.columns([3, 1])
                                with c1:
                                    # Highlight Logic
                                    clean_text = match['text']
                                    highlight_text = clean_text.replace(query, f"**{query}**").replace(query.lower(), f"**{query.lower()}**").replace(query.capitalize(), f"**{query.capitalize()}**")
                                    st.markdown(f"**🗣️ Said:** ... {highlight_text} ...")
                                    st.caption(f"Time: {time_str}")
                                with c2:
                                    st.video(st.session_state['file_path'], start_time=int(match['start']))
                                st.divider()

                # 2. Semantic Fallback
                if not found_audio:
                    st.caption("Searching for similar meanings...")
                    audio_results = tools["db"].search(query_vec, "audio_search", top_k=5)
                    if audio_results:
                        for hit in audio_results:
                            text_content = hit.payload['text']
                            timestamp = hit.payload['timestamp']
                            time_str = format_time(timestamp)
                            with st.container():
                                c1, c2 = st.columns([3, 1])
                                with c1:
                                    st.info(f"\"{text_content}\"")
                                    st.caption(f"Time: {time_str} | Contextual Match")
                                with c2:
                                    st.video(st.session_state['file_path'], start_time=int(timestamp))
                                st.divider()
                    else:
                        st.info("No audio matches found.")

        # --- TAB 2: SUMMARY ---
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(" Generate AI Summary"):
                if 'transcript_text' in st.session_state and tools["llm"]:
                    with st.spinner("Analyzing narrative structure..."):
                        context_text = st.session_state['transcript_text']
                        prompt = f"""
                        Transcript: <transcript>{context_text}</transcript>
                        Task: Create a beautiful, structured summary. Use Markdown headers and bullet points.
                        """
                        completion = tools["llm"].chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model="llama-3.3-70b-versatile"
                        )
                        st.markdown(completion.choices[0].message.content)
                else:
                    st.error("Transcript missing.")
        
        st.markdown('</div>', unsafe_allow_html=True) # End Results Card
    
    st.markdown('</div>', unsafe_allow_html=True) # End Main Animation Container