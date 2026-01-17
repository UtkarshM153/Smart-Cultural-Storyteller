# app.py - FULLY FIXED VERSION
import streamlit as st
import base64
import os
import uuid
from dotenv import load_dotenv
from backend.story_generator import (
    generate_emotion_story,
    generate_ancestral_story,
    generate_mythology_dialogue,
    generate_cultural_story
)
from backend.images_generator import generate_images_from_story
from backend.scene_generator import create_slideshow_video

load_dotenv()

st.set_page_config(
    page_title="Smart Cultural Storyteller", 
    page_icon="📜", 
    layout="wide"
)

# Background setup
def set_background(image_path="assets/images/background.jpg"):
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('data:image/jpg;base64,{encoded}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

set_background()

# Enhanced CSS
st.markdown("""
    <style>
    .story-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 15px;
        line-height: 1.8;
        margin: 20px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: white;
        font-size: 1.1em;
    }
    .stVideo {
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📖 Smart Cultural Storyteller")
menu = st.sidebar.radio(
    "Select a Mode",
    ["Home", "Emotion-Based Storytelling", "Ancestral Story", 
     "Interactive Story", "Cultural Story"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Settings")

story_length = st.sidebar.selectbox(
    "Story Length",
    ["short", "medium", "long", "custom"],
    index=1,
    format_func=lambda x: {
        "short": "Short (100 words)", 
        "medium": "Medium (200 words)", 
        "long": "Long (300 words)", 
        "custom": "Custom"
    }[x]
)

custom_words = None
custom_paragraphs = None

if story_length == "custom":
    custom_words = st.sidebar.number_input("Words", 50, 500, 200, 50)
    custom_paragraphs = st.sidebar.number_input("Paragraphs", 2, 10, 4)

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Media Generation")

generate_images_enabled = st.sidebar.checkbox("Generate Images", True)
if generate_images_enabled:
    num_images = st.sidebar.slider("Number of Images", 4, 10, 6)

generate_video_enabled = st.sidebar.checkbox("Generate Video", True)
if generate_video_enabled:
    add_video_effects = st.sidebar.checkbox("Add Video Effects", True)

st.sidebar.markdown("---")
st.sidebar.info("⏱️ Generation takes 2-3 minutes")

def vertical_center():
    st.markdown("<div style='height: 8vh;'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 3, 1])
    return col

def add_images_and_video(story, user_prompt=""):
    """Generate and display images and video"""
    
    if not generate_images_enabled and not generate_video_enabled:
        return
    
    st.markdown("---")
    
    images_b64 = []
    valid_images = []
    
    # Generate Images
    if generate_images_enabled:
        try:
            with st.spinner(f"🎨 Generating {num_images} images (this may take 2-3 minutes)..."):
                # Pass user prompt for better context matching
                images_b64 = generate_images_from_story(
                    story_text=story, 
                    num_images=num_images, 
                    user_prompt=user_prompt
                )
            
            valid_images = [img for img in images_b64 if img is not None]
            
            if valid_images:
                st.success(f"✨ Successfully generated {len(valid_images)} images!")
                
                st.markdown("### 🖼️ Generated Images")
                st.markdown("---")
                
                # Display in responsive grid
                cols_per_row = 3
                num_rows = (len(valid_images) + cols_per_row - 1) // cols_per_row
                
                for row in range(num_rows):
                    cols = st.columns(cols_per_row)
                    for col_idx in range(cols_per_row):
                        img_idx = row * cols_per_row + col_idx
                        if img_idx < len(valid_images):
                            with cols[col_idx]:
                                st.image(
                                    f"data:image/png;base64,{valid_images[img_idx]}", 
                                    use_container_width=True,
                                    caption=f"Scene {img_idx + 1}"
                                )
                
                st.markdown("---")
            else:
                st.error("❌ Failed to generate images")
                return
                
        except Exception as e:
            st.error(f"❌ Image Generation Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return
    
    # Generate Video
    if generate_video_enabled and valid_images:
        st.markdown("### 🎬 Creating Your Story Video...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🎬 Processing images...")
            progress_bar.progress(20)
            
            story_id = str(uuid.uuid4())[:8]
            
            status_text.text("🎥 Creating video with effects...")
            progress_bar.progress(50)
            
            video_path = create_slideshow_video(
                images_b64=valid_images,  # Use only valid images
                sid=story_id, 
                story=story,
                effects=add_video_effects
            )
            
            progress_bar.progress(90)
            status_text.text("🎵 Adding audio narration...")
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            if video_path and os.path.exists(video_path):
                st.success("✨ Video created successfully!")
                
                st.markdown("### 🎥 Your Story Video")
                st.markdown("---")
                
                try:
                    # Display video player
                    st.video(video_path)
                    
                    # Show video info
                    size_mb = os.path.getsize(video_path) / (1024 * 1024)
                    words = len(story.split())
                    duration = words / 3.0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Duration", f"{duration:.0f}s")
                    with col2:
                        st.metric("File Size", f"{size_mb:.2f} MB")
                    with col3:
                        st.metric("Images", len(valid_images))
                    
                    st.markdown("---")
                    
                    # Download button
                    with open(video_path, 'rb') as video_file:
                        st.download_button(
                            label="📥 Download Video",
                            data=video_file,
                            file_name=f"story_{story_id}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                    
                    st.success("🎉 Complete! Your story video is ready.")
                    st.info("💡 Tip: Click play to watch with audio narration.")
                        
                except Exception as e:
                    st.error(f"❌ Error displaying video: {str(e)}")
            else:
                st.warning("⚠️ Video generation failed. Please try again.")
                
        except Exception as e:
            st.error(f"❌ Video Generation Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# HOME PAGE
if menu == "Home":
    with vertical_center():
        st.markdown("""
            <div style="background:rgba(0,0,0,0.75); backdrop-filter: blur(10px); 
                        padding:50px; border-radius:20px; color:white; text-align:center;">
                <h1 style="font-size: 3em; margin-bottom: 20px;">📜 Smart Cultural Storyteller</h1>
                <h3 style="font-size: 1.5em; color: #FFD700; margin-bottom: 30px;">
                    AI-Powered Cultural Narratives
                </h3>
                <p style="font-size: 1.2em; line-height: 2;">
                    🎭 Emotion-based tales • 🌳 Ancestral legacy<br>
                    💬 Talk with wise friends • 📜 True history<br><br>
                    <em style="color: #FFD700; font-size: 1.1em;">
                        ✨ With AI-generated images & video narration! ✨
                    </em>
                </p>
            </div>
            """, unsafe_allow_html=True)

# EMOTION-BASED STORYTELLING
elif menu == "Emotion-Based Storytelling":
    with vertical_center():
        st.markdown("""
            <h2 style='color:white; text-align:center; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.7);'>
                🎭 Emotion-Based Storytelling
            </h2>
        """, unsafe_allow_html=True)
    
    emotions = ["Devotion", "Joy", "Love", "Courage", "Sadness", "Wonder", "Wisdom"]
    
    col1, col2 = st.columns(2)
    with col1:
        emotion = st.selectbox("Choose an Emotion", emotions)
    with col2:
        idea = st.text_area(
            "Your Story Idea (be specific!)", 
            height=100, 
            placeholder="E.g., 'A mother's love for her son' or 'King's devotion to Lord Jagannath'"
        )
    
    if st.button("✨ Generate Story ✨", use_container_width=True):
        if idea.strip():
            with st.spinner("📝 Creating your story..."):
                story = generate_emotion_story(
                    emotion, idea, story_length, 
                    custom_words, custom_paragraphs
                )
                st.success(f"📖 Your {emotion} Story")
                st.markdown(f"<div class='story-container'>{story}</div>", 
                          unsafe_allow_html=True)
                
                # Generate media with user prompt context
                add_images_and_video(story, user_prompt=idea)
        else:
            st.error("⚠️ Please enter your story idea!")

# ANCESTRAL STORY
elif menu == "Ancestral Story":
    with vertical_center():
        st.markdown("""
            <h2 style='color:white; text-align:center; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.7);'>
                🌳 Ancestral Story
            </h2>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        your_name = st.text_input("Your Name *", placeholder="Enter your name")
        father = st.text_input("Father's Name *", placeholder="Father's name")
        mother = st.text_input("Mother's Name *", placeholder="Mother's name")
    
    with col2:
        grandpa = st.text_input("Grandfather's Name", placeholder="Optional")
        grandma = st.text_input("Grandmother's Name", placeholder="Optional")
        siblings = st.text_input("Siblings", placeholder="Optional: names of siblings")
    
    idea = st.text_area("Additional Details", height=100, 
                       placeholder="Any specific events or themes you'd like included")
    
    if st.button("🌿 Generate Legacy 🌿", use_container_width=True):
        if your_name and father and mother:
            with st.spinner("📝 Creating your ancestral story..."):
                story = generate_ancestral_story(
                    your_name, father, mother, grandpa, grandma, 
                    siblings, idea, story_length, custom_words, custom_paragraphs
                )
                st.success("📖 Your Family Legacy")
                st.markdown(f"<div class='story-container'>{story}</div>", 
                          unsafe_allow_html=True)
                
                # Generate media
                add_images_and_video(story, user_prompt=f"{your_name}'s family story")
        else:
            st.error("⚠️ Please fill in all required fields (marked with *)")

# INTERACTIVE FRIENDLY CONVERSATION
elif menu == "Interactive Story":
    with vertical_center():
        st.markdown("""
            <h2 style='color:white; text-align:center; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.7);'>
                💬 Talk with a Wise Friend
            </h2>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background:rgba(255,255,255,0.1); padding:20px; border-radius:10px; margin-bottom:20px;'>
            <p style='color:white; text-align:center; font-size:1.1em;'>
                💭 Share your problems, worries, or life questions<br>
                🕉️ Get wisdom and guidance from Krishna or Ram<br>
                💝 Like talking to a caring, wise friend
            </p>
        </div>
    """, unsafe_allow_html=True)

    if "dialogue" not in st.session_state:
        st.session_state.dialogue = {
            "started": False, 
            "history": [], 
            "context": "", 
            "question": "", 
            "correct_answer": "", 
            "scenario": None
        }

    if st.button("💬 Start Conversation 💬", use_container_width=True):
        st.session_state.dialogue = {
            "started": True, 
            "history": [], 
            "context": "", 
            "question": "", 
            "correct_answer": "", 
            "scenario": None
        }
        with st.spinner("💭 Your wise friend is ready to listen..."):
            response = generate_mythology_dialogue()
            if "error" in response:
                st.warning(f"Starting with default greeting...")
            
            # Always proceed even with error
            if "segment" in response:
                st.session_state.dialogue["history"].append(response["segment"])
                st.session_state.dialogue.update(response)
                st.rerun()

    if st.session_state.dialogue["started"]:
        scenario = st.session_state.dialogue.get("scenario")
        if scenario:
            st.info(f"🙏 You are speaking with **{scenario['wise']}** - A wise friend who understands life's challenges")

        # Display conversation history
        if st.session_state.dialogue["history"]:
            dialogue_text = "<br><br>".join(st.session_state.dialogue["history"])
            st.markdown(f"<div class='story-container'>{dialogue_text}</div>", 
                       unsafe_allow_html=True)

        # Input for user's response
        if st.session_state.dialogue.get("question"):
            st.markdown("---")
            answer = st.text_area(
                "You speak:", 
                height=100,
                placeholder="Share your thoughts, problems, or answer the question above...",
                key="user_answer"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("💬 Continue Conversation", use_container_width=True):
                    if answer and answer.strip():
                        # Add user's response to history
                        st.session_state.dialogue["history"].append(f"<strong>You speak:</strong> {answer}")
                        
                        with st.spinner("🤔 Your friend is thinking..."):
                            response = generate_mythology_dialogue(
                                st.session_state.dialogue["context"],
                                answer,
                                st.session_state.dialogue["correct_answer"],
                                st.session_state.dialogue["scenario"]
                            )
                            
                            if "segment" in response:
                                st.session_state.dialogue["history"].append(response["segment"])
                                st.session_state.dialogue.update(response)
                                st.rerun()
                            else:
                                st.error("⚠️ Let's try that again...")
                    else:
                        st.warning("⚠️ Please share your thoughts before continuing.")
            
            with col2:
                if st.button("🔄 New Topic", use_container_width=True):
                    del st.session_state.dialogue
                    st.rerun()
        else:
            st.success("✅ Conversation Complete!")
            st.info("💡 Your wise friend has shared their wisdom with you.")
            if st.button("🔄 Start New Conversation", use_container_width=True):
                del st.session_state.dialogue
                st.rerun()

# CULTURAL/HISTORICAL STORY
elif menu == "Cultural Story":
    with vertical_center():
        st.markdown("""
            <h2 style='color:white; text-align:center; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.7);'>
                📜 True Cultural History
            </h2>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        topic = st.text_input(
            "Topic/Subject", 
            placeholder="E.g., Lord Jagannath,Taj Mahal..."
        )
    
    with col2:
        extra = st.text_area(
            "Focus/Details", 
            height=100, 
            placeholder="E.g., 'Focus on devotion rituals' or 'His contribution to India'"
        )
    
    if st.button("📜 Generate True Story 📜", use_container_width=True):
        if topic:
            with st.spinner("📝 Retrieving historical facts..."):
                story = generate_cultural_story(
                    topic, extra, story_length, 
                    custom_words, custom_paragraphs
                )
                st.success("📖 True Cultural History")
                st.markdown(f"<div class='story-container'>{story}</div>", 
                          unsafe_allow_html=True)
                
                # Generate media with full context
                full_context = f"{topic} {extra}" if extra else topic
                add_images_and_video(story, user_prompt=full_context)
        else:
            st.error("⚠️ Please enter a topic!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:rgba(255,255,255,0.7);'>
        <p>🇮🇳 Preserving and Celebrating Indian Heritage 🇮🇳</p>
    </div>
""", unsafe_allow_html=True)