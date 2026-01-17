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

Here is the **clean, properly formatted GitHub README section** in **Markdown**, ready to paste directly into your `README.md` 👇

---

## 🖥️ How to Run the Project Locally

Follow the steps below to set up and run the **Smart Cultural Storyteller** on your local machine.

---

### 1️⃣ Prerequisites

Ensure the following are installed on your system:

* Python **3.9 or higher**
* `pip` (Python package manager)
* Git

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/SMART_STORYTELLER.git
cd SMART_STORYTELLER
```

---

### 3️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
NANO_BANANA_API_KEY=your_nano_banana_api_key
```

⚠️ **Never commit the `.env` file to a public repository.**

---

### 6️⃣ Run the Application

Start the Streamlit web application:

```bash
streamlit run app.py
```

Once running, open your browser and navigate to:

```
http://localhost:8501
```

---

### 7️⃣ Using the Application

* Select a storytelling mode (Cultural, Ancestral, Emotion-Based, Interactive)
* Choose the number of words for the story
* Select the number of images to generate
* Generate the story, images, and narrated output

Generated files will be stored in:

* `assets/images/`
* `assets/audio/`
* `assets/videos/`

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
