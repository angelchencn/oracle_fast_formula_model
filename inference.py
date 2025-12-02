import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Configuration
BASE_MODEL = "deepseek-ai/deepseek-coder-1.3b-instruct"
ADAPTER_PATH = "output"

def generate_code(instruction):
    print("Loading model...")
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Load adapter
    model = PeftModel.from_pretrained(model, ADAPTER_PATH)
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    
    # Prepare prompt
    prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    print("Generating...")
    outputs = model.generate(
        **inputs, 
        max_new_tokens=512, 
        do_sample=True, 
        temperature=0.2,
        top_p=0.95
    )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "Write a Fast Formula to calculate a bonus of 10% of salary if the grade is 'Manager'."
        
    print(generate_code(prompt))
