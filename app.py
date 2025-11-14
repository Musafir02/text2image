from flask import Flask, render_template, request, jsonify, send_from_directory
from bytez import Bytez
import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("BYTEZ_API_KEY")


QUALITY_PREFIXES = {
    "realistic": "masterpiece, best quality, ultra detailed, 8k uhd, professional photography, DSLR, sharp focus, perfect lighting, photorealistic, ",
    "artistic": "masterpiece, best quality, highly detailed, professional artwork, trending on artstation, award winning, vibrant colors, intricate details, ",
    "anime": "masterpiece, best quality, highly detailed, anime style, official art, vivid colors, perfect anatomy, beautiful lighting, ",
    "cinematic": "masterpiece, best quality, cinematic lighting, dramatic, epic composition, movie still, professional color grading, ",
    "fantasy": "masterpiece, best quality, fantasy art, highly detailed, magical atmosphere, epic, stunning visuals, professional illustration, ",
    "portrait": "masterpiece, best quality, professional portrait, sharp focus, studio lighting, detailed face, perfect skin, high resolution, ",
    "landscape": "masterpiece, best quality, breathtaking landscape, professional photography, golden hour lighting, vivid colors, ultra sharp, "
}

QUALITY_SUFFIX = ", detailed, high resolution, professional, pristine quality"

NEGATIVE_PROMPT = "low quality, blurry, bad anatomy, poorly drawn, ugly, deformed, distorted, watermark, text, worst quality, low resolution, grainy, artifacts, jpeg artifacts, duplicate, cropped, mutation, extra limbs"


def enhance_prompt(user_prompt: str, style: str = "realistic") -> str:
    """Enhance user prompt with quality keywords."""
    prefix = QUALITY_PREFIXES.get(style.lower(), QUALITY_PREFIXES["realistic"])
    return f"{prefix}{user_prompt}{QUALITY_SUFFIX}"


def download_image(url: str, folder: str = "outputs") -> str:
    """Download image from URL and save it to `folder`. Returns local file path."""
    os.makedirs(folder, exist_ok=True)
    
    parsed = urlparse(url)
    name = os.path.basename(parsed.path) or f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = os.path.join(folder, name)
    
    resp = requests.get(url)
    resp.raise_for_status()
    
    with open(file_path, "wb") as f:
        f.write(resp.content)
    
    return file_path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/styles')
def get_styles():
    """Return available style options."""
    return jsonify({'styles': list(QUALITY_PREFIXES.keys())})


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        style = data.get('style', 'realistic')
        use_enhancement = data.get('use_enhancement', True)
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Enhance prompt if requested
        final_prompt = enhance_prompt(prompt, style) if use_enhancement else prompt
        
        sdk = Bytez(API_KEY)
        model = sdk.model("John6666/mumix-xl-v20-sdxl")
        
        print(f"Generating with style: {style}")
        print(f"Original prompt: {prompt}")
        print(f"Enhanced prompt: {final_prompt}")
        
        response = model.run(final_prompt)
        
        image_url = None
        error = None
        
        if hasattr(response, "output"):
            image_url = response.output
            error = getattr(response, "error", None)
        elif isinstance(response, dict):
            image_url = response.get("output")
            error = response.get("error")
        
        if error:
            return jsonify({'error': error}), 500
        
        if image_url:
            saved_path = download_image(image_url)
            filename = os.path.basename(saved_path)
            return jsonify({
                'success': True, 
                'image': filename,
                'enhanced_prompt': final_prompt if use_enhancement else None,
                'original_prompt': prompt,
                'style': style
            })
        
        return jsonify({'error': 'No image generated'}), 500
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/outputs/<filename>')
def serve_image(filename):
    return send_from_directory('outputs', filename)


@app.route('/gallery')
def gallery():
    images = []
    if os.path.exists('outputs'):
        images = [f for f in os.listdir('outputs') if f.endswith(('.png', '.jpg', '.jpeg'))]
        # Sort by modification time, newest first
        images.sort(key=lambda x: os.path.getmtime(os.path.join('outputs', x)), reverse=True)
    return jsonify({'images': images})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)