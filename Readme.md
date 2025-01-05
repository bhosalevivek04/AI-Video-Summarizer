# Video AI Summarizer 🎥

A powerful video analysis tool powered by Gemini AI that provides instant insights and summaries in multiple languages.

## Features ✨

- **Multi-language Support**: Get analysis in English, Hindi, and Marathi
- **Flexible Analysis Depths**: Choose between Quick, Standard, and Detailed analysis
- **Smart Templates**: Pre-built query templates for common analysis needs
- **History Tracking**: Keep track of all your previous analyses
- **Easy Export**: Download analysis results in text format
- **User-friendly Interface**: Clean and intuitive design

## Demo 🚀

[Live Demo](https://ai-video-summarize.streamlit.app/)

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/bhosalevivek04/AI-Video-Summarizer.git
   cd video-ai-summarizer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create `.streamlit/secrets.toml`
   - Add your Gemini API key:
     ```toml
     GOOGLE_API_KEY = "your-api-key"
     ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage 📝

1. Upload a video file (supported formats: MP4, MOV, AVI)
2. Select analysis depth and language
3. Choose a template or write your own query
4. Click "Analyse Video" and wait for results
5. Download or save the analysis

## Technologies Used 💻

- Streamlit
- Google Gemini AI
- Python
- DuckDuckGo API

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.


## Contact 📧

Vivek Bhosale - [bhosalevivek04@email.com](mailto:your@email.com)

Project Link: https://github.com/bhosalevivek04/AI-Video-Summarizer

## Acknowledgments 🙏

- Google Gemini AI for providing the powerful video analysis capabilities
- Streamlit for the amazing web framework
- All contributors and users of this project
