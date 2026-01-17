---

# 🌍 Smart Cultural Storyteller

Smart Cultural Storyteller is a **multimodal AI-based web application** that generates culturally rich stories along with AI-generated images and narrated audio. The system allows users to customize storytelling modes, story length, and number of images, delivering an immersive digital storytelling experience.

---

## 🚀 Features

* 📖 AI-generated cultural and emotional stories
* 🎭 Multiple storytelling modes:

  * Cultural Storytelling
  * Ancestral Storytelling
  * Emotion-Based Storytelling
  * Interactive Storytelling
* 🖼 Scene-wise AI image generation
* 🔊 Text-to-Speech narration
* 🎥 Multimedia storytelling output
* ⚙ User control over word count and image count

---

## 🧠 System Overview

The application follows a modular workflow:

1. User selects storytelling parameters via the web interface
2. Story is generated using a Large Language Model (LLM)
3. Story is split into scenes
4. Images are generated for each scene
5. Story text is converted into audio narration
6. Final multimedia output is displayed to the user

---

## 🛠️ Technologies Used

* **Streamlit** – Web application framework
* **Python** – Backend logic
* **Groq API** – Story generation using LLMs
* **Nano Banana API** – AI-based image generation
* **Text-to-Speech (TTS)** – Audio narration

---

## 📂 Project Structure

```
├── app.py                # Main Streamlit application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── assets/               # Images or static resources (if any)
└── Backend/              # Contains file used for story, image generation and TTS
└──.env                   # Contains API keys of Groq and Gemini(Nano Banana)
```

---

## ▶️ How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/your-username/smart-cultural-storyteller.git
```

2. Navigate to the project directory:

```bash
cd smart-cultural-storyteller
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

---

## 🔑 API Configuration

Before running the application, add your API keys:

```python
GROQ_API_KEY = "your_groq_api_key"
NANO_BANANA_API_KEY = "your_nano_banana_api_key"
```

⚠️ **Do not expose API keys in public repositories.**

---

## 📊 Results

* Successfully generates AI-based cultural stories
* Produces relevant scene-wise images
* Converts stories into narrated audio
* Delivers a complete multimedia storytelling experience

---

## ⚠️ Limitations

* Image quality depends on prompt design
* Longer stories increase generation time
* Cultural accuracy is model-dependent

---

## 🔮 Future Improvements

* Multilingual storytelling support
* Improved image realism
* Faster generation pipeline
* Mobile application deployment

---

## 🤖 AI Usage Disclosure

This project uses AI models for story generation, image generation, and text-to-speech conversion. AI tools were also used to assist with code structuring and documentation under human supervision. The Author takes no responsibility of the output the Web-App produces, it depends on the prompts given by the User only.

---

## 📜 License

This project is intended for **academic and educational purposes**.

---

✅ **Professional**
✅ **Academic + GitHub ready**
