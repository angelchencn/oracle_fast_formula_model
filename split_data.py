import json
import os

input_file = "oracle_fast_formula_model/data/processed/train_data.jsonl"
output_dir = "oracle_fast_formula_model/data/processed"

bonus_file = os.path.join(output_dir, "bonus_data.jsonl")
absence_file = os.path.join(output_dir, "absence_data.jsonl")
overtime_file = os.path.join(output_dir, "overtime_data.jsonl")

bonus_data = []
absence_data = []
overtime_data = []

print(f"Reading from {input_file}...")

with open(input_file, 'r') as f:
    for line in f:
        entry = json.loads(line)
        instruction = entry.get("instruction", "").lower()
        output = entry.get("output", "")
        
        if "bonus" in instruction or "BONUS_CALC" in output:
            bonus_data.append(entry)
        elif "vacation accrual" in instruction or "VACATION_ACCRUAL" in output:
            absence_data.append(entry)
        elif "overtime" in instruction or "OT_PAY" in output:
            overtime_data.append(entry)
        else:
            print(f"Warning: Could not categorize entry: {instruction[:50]}...")

def write_jsonl(filename, data):
    with open(filename, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    print(f"Wrote {len(data)} entries to {filename}")

write_jsonl(bonus_file, bonus_data)
write_jsonl(absence_file, absence_data)
write_jsonl(overtime_file, overtime_data)
