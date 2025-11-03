# Arch-Linux-Bash-Assistant (Gemini) 🧠💻

A lightweight command-line assistant powered by **Google Gemini**, optimized for **Arch Linux** users.  
It provides concise, bash-focused answers with **Gemini 2.5-Flash**.
I use **Nordic** colour palette , so if colours don´t work maybe itś that.

---
## 📦 Features

- ⚙️ **Command-line based** — ask anything directly from bash.  
- 🧠 **Context-aware answers** — includes your recent bash history for smarter replies.  
- ⚡ **Powered by Google Gemini 2.5 Flash API**.  
- 🧩 **Portable** — run from any directory after installation.  
- 💬 **Clean formatted responses** (bold text, colored commands, etc.).  

---
## --Installation--

### 1. Clone the Repository
```bash
git clone https://github.com/Mr-M-3/Arch-Linux-Bash-Assistant.git ~/IABash
cd ~/IABash
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install google-genai
```

### 3. Make the Script Executable
```bash
chmod +x Gemini.py
```
### 4. Add it as a Global Command
```bash
mkdir -p ~/bin
ln -s ~/IABash/Gemini.py ~/bin/gemini
```

### 5. Obtain your api key [Here](https://aistudio.google.com/app/api-keys) , and add it
```bash
export GOOGLE_API_KEY="your_api_key_here"
export PATH="$HOME/bin:$PATH"
```

### 6. Reload
```bash
source ~/.bashrc
```

### Usage
```bash
gemini hello,where is your config document
```
---
### Comments
This is a very simple Gemini model, so don’t expect it to be like any of today’s advanced models. 
It’s very useful for asking about Bash commands if you forget something — that’s mainly what I use it for.
Also, feel free to modify the prompt as you wish.
I recommend including your PC model for better answers.

---
### 📄Lice
MIT License © 2025 Mr-M-3
Feel free to modify and share this project.

### ❤️Contribute
Pull requests are welcome!
If you have ideas to improve formatting, error handling, or add color themes, feel free to open an issue.
