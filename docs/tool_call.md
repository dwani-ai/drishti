
./build/bin/llama-server -hf Qwen/Qwen3-32B-GGUF --host 0.0.0.0 --port 91000 --n-gpu-layers 100 --threads 4 --ctx-size 4096 --batch-size 256 --jinja -fa 


huggingface-cli download google/gemma-3-27b-it-qat-q4_0-gguf --local-dir hf_models/

 ./build/bin/llama-server   --model hf_models/gemma-3-27b-it-q4_0.gguf  --mmproj hf_models/mmproj-model-f16-27B.gguf  --host 0.0.0.0   --port 9000   --n-gpu-layers 100   --threads 4   --ctx-size 4096   --batch-size 256
 


<!-- 
./build/bin/llama-server -hf Qwen/Qwen3-32B-GGUF --host 0.0.0.0 --port 91000 --n-gpu-layers 100 --threads 4 --ctx-size 4096 --batch-size 256 --jinja -fa --reasoning-format deepseek


docker run --rm --gpus all \
  -v /path/to/models:/models \
  -p 8000:8000 \
  ghcr.io/ggml-org/llama.cpp:server \
  --model /models/Qwen3-8B-Q4_0.gguf \
  --host 0.0.0.0 \
  --port 8000 \
  --ctx-size 4096 \
  --threads 6 \
  --batch-size 64 \
  --ngl 99 \
  --chat-template qwen3

docker run --rm --gpus all \
  -p 8000:8000 \
  ghcr.io/ggml-org/llama.cpp:server \
  --model /models/Qwen3-8B-Q4_0.gguf \
  --host 0.0.0.0 \
  --port 8000 \
  --ctx-size 4096 \
  --threads 6 \
  --batch-size 64 \
  --ngl 99 \
  --chat-template qwen3


./build/bin/llama-server -hf ggml-org/Qwen2.5-VL-32B-Instruct-GGUF --host 0.0.0.0 --port 9000 --n-gpu-layers 100 --threads 4 --ctx-size 4096 --batch-size 256



./build/bin/llama-server -hf Qwen/Qwen3-8B-GGUF --host 0.0.0.0 --port 91000 --n-gpu-layers 100 --threads 4 --ctx-size 4096 --batch-size 256

-->
