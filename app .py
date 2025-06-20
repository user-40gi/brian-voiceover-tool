import gradio as gr
from TTS.api import TTS

# Load XTTS model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

MAX_WORDS = 3000

def generate_voice(text):
    words = len(text.strip().split())

    if words == 0:
        return "❌ Script is empty.", None
    elif words > MAX_WORDS:
        return f"❌ Word limit exceeded! You used {words} words, max is {MAX_WORDS}.", None

    output_path = "output.mp3"
    tts.tts_to_file(
        text=text,
        speaker_wav="brian_sample.wav",  # Make sure this file exists in same folder
        language="en",
        file_path=output_path
    )
    return f"✅ Voice generated successfully! Word count: {words}", output_path

def count_words(text):
    return f"📝 Word count: {len(text.strip().split())} / {MAX_WORDS}"

with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ Brian-Style AI Voiceover Tool")
    gr.Markdown("Paste your script below (max 3000 words) and generate high-quality Brian-style voiceover.")

    with gr.Row():
        text_input = gr.Textbox(label="Paste your script", lines=15, placeholder="Enter your script here...")
        word_counter = gr.Label(value="📝 Word count: 0 / 3000")

    text_input.change(fn=count_words, inputs=text_input, outputs=word_counter)

    generate_btn = gr.Button("🚀 Generate Voice")
    status_output = gr.Textbox(label="Status")
    audio_output = gr.Audio(label="🎧 Preview Voice", type="filepath")
    download_output = gr.File(label="⬇️ Download MP3")

    def run_all(text):
        status, path = generate_voice(text)
        if path:
            return status, path, path
        else:
            return status, None, None

    generate_btn.click(fn=run_all, inputs=text_input, outputs=[status_output, audio_output, download_output])

demo.launch()
