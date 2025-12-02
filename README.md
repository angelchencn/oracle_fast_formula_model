# Oracle Fast Formula Model

This project fine-tunes a DeepSeek Coder model (1.3B) to generate Oracle Fast Formula code from natural language instructions.

## Project Structure

- `prepare_data.py`: Generates synthetic training data based on templates.
- `train.py`: Fine-tunes the model using LoRA and 4-bit quantization (QLoRA).
- `inference.py`: Runs inference using the fine-tuned model (adapter).
- `requirements.txt`: Python dependencies.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Generate Data
First, generate the synthetic dataset for training. This will create `data/processed/train_data.jsonl`.
```bash
python prepare_data.py
```

### 2. Train Model
Run the training script to fine-tune the model. The model adapter will be saved to `output/`.
```bash
python train.py
```
*Note: This script is configured for a short demo run (50 steps).*

### 3. Inference
Test the trained model by providing an instruction.
```bash
python inference.py "Write a Fast Formula to calculate a bonus of 10% of salary if the grade is 'Manager'."
```
Or simply run it without arguments to use the default prompt:
```bash
python inference.py
```

## Model Details
- **Base Model**: `deepseek-ai/deepseek-coder-1.3b-instruct`
- **Technique**: LoRA (Low-Rank Adaptation) with 4-bit quantization (bitsandbytes).
- **Frameworks**: PyTorch, Transformers, PEFT, TRL.
