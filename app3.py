import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Smart Text Summarizer",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Smart Text Summarizer")
st.write("Summarize long articles, essays, or documents instantly using the blazing-fast Groq API.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # API key input
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        value=os.environ.get("GROQ_API_KEY", ""),
        help="Get your free key from https://console.groq.com"
    )
    
    # Model selection (using current robust models)
    model_choice = st.selectbox(
        "Choose Model",
        ["openai/gpt-oss-20b", "openai/gpt-oss-120b"],
        index=0,
        help="gpt-oss-20b is ultra-fast; gpt-oss-120b excels at deep reasoning."
    )
    
    # Summary style selection
    summary_style = st.selectbox(
        "Summary Style",
        ["Bullet Points", "Short Paragraph", "Key Takeaways & Action Items"]
    )
    
    st.markdown("---")
    st.markdown("Powered by [Groq LPU](https://groq.com/) & [Streamlit](https://streamlit.io/)")

# Main content area
text_to_summarize = st.text_area(
    "Paste your text here:",
    height=250,
    placeholder="Paste a long news article, research report, or lecture notes here..."
)

if st.button("🚀 Generate Summary", type="primary"):
    if not api_key_input:
        st.error("Please enter your Groq API key in the sidebar or set it as an environment variable (`GROQ_API_KEY`).")
    elif not text_to_summarize.strip():
        st.warning("Please paste some text to summarize.")
    else:
        try:
            # Initialize Groq Client
            client = Groq(api_key=api_key_input)
            
            # Formulate prompt based on user selection
            if summary_style == "Bullet Points":
                prompt = f"Summarize the following text into clear, concise bullet points:\n\n{text_to_summarize}"
            elif summary_style == "Short Paragraph":
                prompt = f"Provide a concise short paragraph summary of the following text:\n\n{text_to_summarize}"
            else:
                prompt = f"Analyze the following text and extract key takeaways and core action items:\n\n{text_to_summarize}"
            
            with st.spinner("Summarizing at lightning speed..."):
                stream = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a precise, efficient assistant that summarizes text accurately without losing core details."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    stream=True,
                )
                
                # Display output container with streaming text effect
                st.subheader("Summary Result")
                response_container = st.empty()
                full_response = ""
                
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_response += content
                        response_container.markdown(full_response + "▌")
                        
                # Final render without streaming cursor
                response_container.markdown(full_response)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")