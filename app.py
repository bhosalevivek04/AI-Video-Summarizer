import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini 
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file,get_file
import google.generativeai as genai
import time
from pathlib import Path

import tempfile

from dotenv import load_dotenv
load_dotenv()

import os
import random
from datetime import datetime

API_KEY=os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai .configure(api_key=API_KEY)

st.set_page_config(
    page_title="Video AI Summarizer | Analyze Videos with AI",
    page_icon="🎥",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/bhosalevivek04/AI-Video-Summarizer',
        'Report a bug': 'https://github.com/bhosalevivek04/AI-Video-Summarizer/issues',
        'About': """
        ## Video AI Summarizer
        Analyze videos using advanced AI technology powered by Gemini.
        
        - ✨ Multi-language support (English, Hindi, Marathi)
        - 🎯 Multiple analysis depths
        - 📊 Detailed insights and summaries
        """
    }
)

# Add meta tags and description
st.markdown("""
    <!-- SEO Meta Tags -->
    <meta name="description" content="AI-powered video analysis tool that provides summaries and insights in multiple languages. Upload your video and get instant analysis.">
    <meta name="keywords" content="video analysis, AI summarizer, video insights, Gemini AI, video summary, Hindi analysis, Marathi analysis">
    <meta name="author" content="Your Name">
    
    <!-- Open Graph / Social Media Meta Tags -->
    <meta property="og:title" content="Video AI Summarizer | Analyze Videos with AI">
    <meta property="og:description" content="Get instant AI-powered video analysis in English, Hindi, and Marathi">
    <meta property="og:image" content="your-preview-image-url">
    <meta property="og:url" content="your-app-url">
    
    <!-- Schema.org markup for Google -->
    <script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "WebApplication",
        "name": "Video AI Summarizer",
        "description": "AI-powered video analysis tool with multi-language support",
        "applicationCategory": "Multimedia Analysis Tool",
        "operatingSystem": "Web Browser",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }
    }
    </script>
""", unsafe_allow_html=True)

# Add custom styling
st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        color: #1E88E5;
        font-size: 42px;
        font-weight: bold;
        padding-bottom: 20px;
        text-align: center;
    }
    
    /* Subtitle styling */
    .sub-title {
        color: #424242;
        font-size: 24px;
        padding-bottom: 30px;
        text-align: center;
    }
    
    /* Card-like container for video */
    .video-container {
        padding: 20px;
        margin: 20px 0;
    }
    
    /* Improve text area appearance */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    
    /* Style the analyze button */
    .stButton button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        padding: 10px 25px;
        border: none;
    }
    
    /* Style the sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
        padding: 20px;
    }
    
    /* Style expanders */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    /* Style download button */
    .stDownloadButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        border: none;
    }
    
    /* Add divider styling */
    hr {
        margin: 30px 0;
        border: none;
        border-top: 1px solid #eee;
    }
    
    /* Style status messages */
    .stSuccess, .stInfo {
        border-radius: 10px;
    }
    
    /* Add loading animation */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .loading {
        animation: pulse 1.5s infinite;
    }
    
    /* Add padding to main content to prevent overlap with footer */
    .main {
        margin-bottom: 100px;
    }
    
    /* Add padding to footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4a4a4a;  /* Darker gray background */
        padding: 10px;
        text-align: center;
        border-top: 1px solid #666;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# Update main title with keywords
st.markdown("""
    <h1 class='main-title'>Video AI Summarizer & Analysis Tool 🎥</h1>
    <p class='sub-title'>Instant Video Analysis in English, Hindi & Marathi | Powered by Gemini AI</p>
""", unsafe_allow_html=True)

# Update the footer styling with gray colors
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4a4a4a;  /* Darker gray background */
        padding: 10px;
        text-align: center;
        border-top: 1px solid #666;
        z-index: 999;
    }
    
    /* Add padding to main content to prevent overlap with footer */
    .main {
        margin-bottom: 100px;
    }
    </style>
    
    <div class="main">
        <!-- Your main content is here -->
    </div>
    
    <div class="footer">
        <p style='color: #e0e0e0; font-size: 0.8em; margin: 0;'>  <!-- Light gray text -->
            Video Analysis | AI Summary | Multi-language Support | Instant Insights
            <br>
            Powered by Advanced AI Technology
        </p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Settings")
    analysis_depth = st.select_slider(
        "Analysis Depth",
        options=["Quick", "Standard", "Detailed"],
        value="Standard"
    )
    language = st.selectbox(
        "Response Language",
        ["English", "Hindi", "Marathi"]
    )

@st.cache_resource
def initialize_agent():    
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True
    )

## Initialize the agent
multimodal_Agent=initialize_agent()

# File uploader
video_file=st.file_uploader(
    "Upload a video file",type=['mp4','mov','avi'],help="Upload a video for AI analysis"
)

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

if 'processing' not in st.session_state:
    st.session_state.processing = False

if video_file:
    # Dynamically set the suffix based on the uploaded file
    suffix = Path(video_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    # Style the video display section
    st.markdown("<div class='video-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Add custom CSS to control video size
        st.markdown("""
            <style>
                .stVideo {
                    width: 100%;
                    max-width: 400px;
                    height: auto;
                }
                video {
                    max-height: 300px;
                }
            </style>
        """, unsafe_allow_html=True)
        st.video(video_path)
    st.markdown("</div>", unsafe_allow_html=True)

    # Add template queries before the user input
    templates = {
        "General Summary": "Provide a general summary of this video",
        "Technical Analysis": "Analyze the technical aspects of this video",
        "Content Review": "Review the main content and message of this video",
        "Audience Analysis": "Who is the target audience for this video?"
    }

    template_choice = st.selectbox(
        "📋 Query Templates",
        ["Custom"] + list(templates.keys())
    )

    # Style the query input
    st.markdown("### 🤔 What would you like to know about this video?")
    user_query = st.text_area(
        label="Video Query",
        label_visibility="collapsed",
        placeholder="Ask anything about video content. The AI agent will analyze and gather additional information",
        help="Provide specific questions or insights you want from the video.",
        value=templates[template_choice] if template_choice != "Custom" else "",
        key="query_input"
    )

    if st.button("🔍 Analyse Video", disabled=st.session_state.processing):
        if not user_query:
            st.warning("Please enter a question or select a template to analyze the video.")
            st.stop()
        
        st.session_state.processing = True
        try:
            # Add at the start of video processing
            if video_file.size > 200 * 1024 * 1024:  # 200MB limit
                st.error("Video file is too large. Please upload a file smaller than 200MB.")
                st.stop()

            # Add supported formats check
            SUPPORTED_FORMATS = ['mp4', 'mov', 'avi']
            file_extension = video_file.name.split('.')[-1].lower()
            if file_extension not in SUPPORTED_FORMATS:
                st.error(f"Unsupported file format. Please upload one of: {', '.join(SUPPORTED_FORMATS)}")
                st.stop()

            # Create a placeholder for the spinner
            spinner_placeholder = st.empty()
            stop_button = st.button("Stop Analysis", key="stop_analysis")
            
            with spinner_placeholder:
                with st.status("Analyzing video...", expanded=True) as status:
                    st.write("Uploading video...")
                    processed_video = upload_file(video_path)
                    
                    st.write("Processing video...")
                    progress_bar = st.progress(0)
                    while processed_video.state.name == "PROCESSING":
                        progress_bar.progress(random.random())  # Show progress animation
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)
                    progress_bar.progress(100)
                    
                    st.write("Generating insights...")
                    # Create language-specific instructions
                    language_instructions = {
                        "English": "Please provide the analysis in English with standard English formatting.",
                        "Hindi": "कृपया विश्लेषण हिंदी में प्रदान करें, उचित हिंदी भाषा के प्रारूप और शैली का उपयोग करें।",
                        "Marathi": "कृपया विश्लेषण मराठीमध्ये प्रदान करा, योग्य मराठी भाषेचे स्वरूप आणि शैली वापरा."
                    }

                    def get_analysis_points(depth):
                        if depth == "Quick":
                            return "- Main content summary"
                        elif depth == "Standard":
                            return """- Main content summary
                                    - Key themes and messages
                                    - Visual and audio elements analysis"""
                        else:  # Detailed
                            return """- Main content summary
                                    - Detailed scene-by-scene analysis
                                    - Technical aspects (camera work, editing, sound)
                                    - Contextual analysis and implications
                                    - Related background information
                                    - Subtle details and nuances"""

                    analysis_prompt = (
                        f"""
                        Analyze the uploaded video for content and context.
                        Analysis Depth: {analysis_depth}
                        {
                            "Quick: Provide a brief overview and key points only." if analysis_depth == "Quick"
                            else "Standard: Provide a balanced analysis with moderate detail."
                            if analysis_depth == "Standard"
                            else "Detailed: Provide an in-depth analysis with comprehensive details, including subtle elements, technical aspects, and thorough context."
                        }
                        
                        {language_instructions[language]}
                        
                        Query: {user_query}
                        
                        Please structure your response in {language} and include:
                        {get_analysis_points(analysis_depth)}

                        Important: The entire response MUST be in {language}. All headings, descriptions, and analysis should be in {language}.
                        """
                    )

                    # Add retry mechanism
                    max_retries = 3
                    retry_count = 0

                    while retry_count < max_retries:
                        try:
                            response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])
                            break
                        except Exception as e:
                            retry_count += 1
                            if retry_count == max_retries:
                                st.error(f"Failed after {max_retries} attempts: {str(e)}")
                            else:
                                st.warning(f"Attempt {retry_count} failed, retrying...")
                                time.sleep(2)

            # Clear the spinner after processing is complete
            spinner_placeholder.empty()
            
            st.subheader("Analysis Result")
            st.markdown(response.content)

            if response:
                st.session_state.analysis_history.append({
                    'video_name': video_file.name,
                    'query': user_query,
                    'response': response.content,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # Fix download functionality
                try:
                    # Convert response content to string if it's not already
                    download_content = str(response.content)
                    
                    # Create a formatted text with metadata
                    download_text = f"""Video Analysis Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Video: {video_file.name}
Query: {user_query}
Language: {language}
Analysis Depth: {analysis_depth}

Analysis Results:
{download_content}
"""
                    
                    st.download_button(
                        label="📥 Download Analysis as TXT",
                        data=download_text,
                        file_name=f"video_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_button"
                    )
                except Exception as e:
                    st.error(f"Error preparing download: {str(e)}")

        except Exception as error:
            st.error(f"An error occurred during analysis: {error}")
        finally:
            # Clean up temporary files
            Path(video_path).unlink(missing_ok=True)
            spinner_placeholder.empty()  # Ensure spinner is removed even if there's an error
            st.session_state.processing = False  # Reset processing state

else:
    st.info("Upload a video file to begin analysis.")

    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

with st.expander("ℹ️ How to use this app"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            ### 📝 Steps to Use
            1. **Upload Video** 📤
               - Click 'Browse files' to upload your video
               - Maximum size: 200MB
            
            2. **Ask Question** ❓
               - Type your question about the video
               - Be specific for better results
            
            3. **Analyze** 🔍
               - Click 'Analyse Video' button
               - Wait for AI processing
        """)
    with col2:
        st.markdown("""
            ### 💡 Tips & Info
            - **Supported formats**: MP4, MOV, AVI
            - **Best results**:
              - Keep videos under 5 minutes
              - Use clear, well-lit content
              - Ask specific questions
            - **Analysis depth**:
              - Quick: Basic overview
              - Standard: Balanced analysis
              - Detailed: In-depth insights
        """)

# Add history viewer
with st.expander("📜 Previous Analyses"):
    if not st.session_state.analysis_history:
        st.info("No previous analyses yet. Your analysis history will appear here.")
    else:
        for idx, analysis in enumerate(st.session_state.analysis_history):
            with st.container():
                st.markdown(f"### 📊 Analysis #{idx + 1}")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🎥 Video**: {analysis['video_name']}")
                    st.markdown(f"**❓ Query**: {analysis['query']}")
                with col2:
                    st.markdown(f"**🕒 Time**: {analysis['timestamp']}")
                st.markdown("**💡 Insights**:")
                st.markdown(analysis['response'])
                st.divider()

# After showing results
with st.expander("📝 Provide Feedback"):
    col1, col2 = st.columns([2,1])
    with col1:
        feedback = st.radio(
            "Was this analysis helpful?",
            ["Very Helpful 😊", "Somewhat Helpful 🤔", "Not Helpful ☹️"]
        )
    with col2:
        st.markdown("### Share your thoughts")
        feedback_text = st.text_area(
            label="Feedback Text",
            label_visibility="collapsed",
            placeholder="Your feedback helps us improve!"
        )
    
    if st.button("Submit Feedback", key="feedback_button"):
        st.success("Thank you for your feedback! 🙏")

# Add keyboard shortcuts
st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            document.querySelector('button:contains("Analyse")').click();
        }
    });
    </script>
""", unsafe_allow_html=True)