dristhi  - Assitant for Visually Challenged

- Problem :
  - Hey dwani, what do you see ?


- Solution
  - Voice to Text (ASR)
  - Text to Command - Camera open (Tool Call)
  - Image Capture to Description ( Vision LM)
  - Description to Voice (TTS)

- Integration
  - Webcam + Mic
  - Rpi + Pi Camera + Mic
  - Reachy Mini
  - Alexa/Echo / Google Home

---

- Server 

./build/bin/llama-server -hf Qwen/Qwen3-32B-GGUF --host 0.0.0.0 --port 91000 --n-gpu-layers 100 --threads 4 --ctx-size 4096 --batch-size 256 --jinja -fa 

docker pull ghcr.io/ggml-org/llama.cpp:server-cuda-b5763

- Server 

```bash
./build/bin/llama-server -hf Qwen/Qwen3-32B-GGUF --host 0.0.0.0 --port 9100 --n-gpu-layers 100 --threads 4 --ctx-size 4096 --batch-size 256 --jinja -fa 

huggingface-cli download google/gemma-3-27b-it-qat-q4_0-gguf --local-dir hf_models/

 ./build/bin/llama-server   --model hf_models/gemma-3-27b-it-q4_0.gguf  --mmproj hf_models/mmproj-model-f16-27B.gguf  --host 0.0.0.0   --port 9000   --n-gpu-layers 100   --threads 4   --ctx-size 4096   --batch-size 256
 

- Client
  - pip install openai pytz requests opencv-python
  - python src/frame_desctibe.py
sudo apt-get update && sudo apt-get install -y portaudio19-dev build-essential python3-dev

```

- Client
  - pip install openai pytz requests opencv-python
  - python src/frame_desctibe.py


<!-- 
  - pip install openai-whisper pyaudio numpy
  - python src/voice_dwani.py

  - pip install transformers

-->
