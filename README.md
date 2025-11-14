#  AI Image Generator with Bytez + Flask

A powerful Flask-based AI image generation application using the **Bytez** API.  
Generate stunning images from text prompts with multiple artistic styles, automatic downloads, and gallery view.

---

##  Features
- 🖼 Generate images from any text prompt
- 🎨 Multiple style presets (Realistic, Anime, Cinematic, Fantasy, Portrait, Landscape, Artistic)
- 💾 Automatic image saving to `/outputs`
- 🖥 Built-in Gallery viewer
- 🔐 Secure API key handling using `.env`

---

## 1. Clone the repository
```bash
git clone https://github.com/Musafir02/text2image.git
cd text2image
```

## 2. Create a virtual environment
**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```
**Mac / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
``` 

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Copy .env.example to .env
Mac / Linux
```bash
cp .env.example .env
```
Windows PowerShell
```bash
copy .env.example .env
```

## 5. Get your Bytez API key

Create an account and generate a key:
https://bytez.com

Use the **mumix-xl-v20-sdxl** model key.

Then open .env file and insert key:

BYTEZ_API_KEY=your_api_key_here

Run the Application
```bash
python app.py
```

## 6. Open the application in your browser
```bash
http://localhost:5000
```

## Contributing

Pull requests are welcome.
Suggestions & improvements appreciated!

## Author

Developed by Ibrahim Shaikh
If you like the project, ⭐ star the repo!
