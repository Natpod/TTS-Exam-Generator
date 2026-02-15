---

# TTS-Exam-Generator 🎧 English Listening Exam Generator

Python script to generate Cambridge style listening exams in english
This project generates a **single merged MP3 listening exam file** from a structured CSV/Excel input file.

It supports:

* ✅ Dialogue and Monologue formats
* ✅ Random male/female voice simulation
* ✅ Accent variation (US, UK, AU, etc.)
* ✅ Speaker 1 / Speaker 2 alternating logic
* ✅ Automatic merging into one final MP3 file

---

# 📦 Requirements

## 1️⃣ Python Version

Python **3.9+** recommended.

Check your version:

```bash
python --version
```

---

## 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Python Dependencies

Create a `requirements.txt` file:

```
gTTS
pydub
pandas
openpyxl
tk
```

Then install:

```bash
pip install -r requirements.txt
```

---

# 🔊 4️⃣ Install FFmpeg (REQUIRED)

⚠️ `pydub` needs FFmpeg to export MP3 files.

---

## Windows

1. Download from:
   [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

2. Extract folder

3. Add `/bin` folder to **System PATH**

4. Restart terminal

Test installation:

```bash
ffmpeg -version
```

---

## Mac

```bash
brew install ffmpeg
```

---

## Linux (Ubuntu)

```bash
sudo apt update
sudo apt install ffmpeg
```

---

# 📄 Input File Structure

The script accepts **CSV or Excel (.xlsx)** with this structure:

| QuestionNumber | Type      | Excerpt                     | Question |
| -------------- | --------- | --------------------------- | -------- |
| 1              | Dialogue  | Speaker text - Speaker text | Why...?  |
| 2              | Monologue | Speech text                 | What...? |

### Important:

* Dialogue speakers MUST be separated by `" - "`
* Exactly 2 speakers per dialogue
* No extra hyphens inside sentences

Example:

```
1,Dialogue,"I heard you're moving - Yes, I found a job closer to home.","Why is the speaker moving?"
```

---

# ▶️ Running the Script (CLI Version)

Example:

```bash
python tts-exam-generator.py input.csv output.mp3
```

Arguments:

* `input.csv` → your exam file
* `output.mp3` → final merged audio

# 👥 Speaker Logic

For Dialogues:

* Even question number → Speaker 1 = Accent A, Speaker 2 = Accent B
* Odd question number → Speaker 1 = Accent B, Speaker 2 = Accent A

Gender is randomly simulated via pitch shifting.

Monologues:

* Default female voice
* Default US accent

---

# 🛠 Project Structure Example

```
project/
│
├── generate_exam.py
├── app.py
├── requirements.txt
├── input.csv
├── README.md
└── output.mp3
```

---

# 🧪 Troubleshooting

### ❌ "ffmpeg not found"

Solution:

* Make sure FFmpeg is installed
* Ensure `/bin` folder is in PATH
* Restart terminal

---

### ❌ Audio exports but no sound

Check:

* Speakers connected
* File size > 0 KB
* FFmpeg working correctly

---

### ❌ gTTS connection error

* Check internet connection
* gTTS requires online access

---

# 🚀 Production Notes

For better voice quality and real male/female voices:

Consider upgrading to:

* Google Cloud TTS
* Microsoft Edge TTS
* ElevenLabs API

---

# ✅ Final Output

The script generates:

```
final_exam.mp3
```

Containing:

* Intro
* All excerpts
* Natural pauses
* All merged into ONE file

---

Here is a clean, production-ready **Docker version** of your Listening Exam Generator.

You can copy this directly into your project.

---

# 🐳 Docker Setup – English Listening Exam Generator

This container will:

* Install Python
* Install FFmpeg
* Install all Python dependencies
* Run your script inside an isolated environment

---

# 📁 Project Structure

```
listening-exam/
│
├── generate_exam.py
├── app.py                  (optional GUI)
├── requirements.txt
├── Dockerfile
├── input.csv
└── README.md
```

---

# 📦 requirements.txt

```
gTTS
pydub
pandas
openpyxl
```

(You do NOT need to install ffmpeg here — Docker will handle it.)

---

# 🐳 Dockerfile

Create a file named `Dockerfile` (no extension):

```dockerfile
# Use official Python image
FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "tts-exam-generator.py"]
```

---

# 🚀 Build Docker Image

Open terminal inside your project folder:

```bash
docker build -t listening-exam .
```

---

# ▶️ Run the Script (CLI Version)

If your script expects:

```bash
python generate_exam.py input.csv output.mp3
```

Run Docker like this:

```bash
docker run --rm -v ${PWD}:/app listening-exam input.csv output.mp3
```

### Windows PowerShell:

```powershell
docker run --rm -v ${PWD}:/app listening-exam input.csv output.mp3
```

### Windows CMD:

```cmd
docker run --rm -v %cd%:/app listening-exam input.csv output.mp3
```

---


This mounts your local folder into the container so:

* Docker can read `input.csv`
* Docker writes `output.mp3` back to your computer

---


# 🌐 Internet Requirement

`gTTS` requires internet access.

Docker must have internet connectivity.

---


# 🧪 Test Docker Installation

Check:

```bash
docker --version
```

If not installed:

Download from:

👉 [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

---
