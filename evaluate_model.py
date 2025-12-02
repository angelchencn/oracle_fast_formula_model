import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Configuration
BASE_MODEL = "deepseek-ai/deepseek-coder-1.3b-instruct"
ADAPTER_PATH = "output"

# Test Cases covering all categories
TEST_CASES = [
    {
        "category": "Bonus (Payroll)",
        "instruction": "Write an Oracle Fast Formula to calculate an annual bonus based on employee grade and salary.",
        "expected_keywords": ["ALIAS", "DEFAULT FOR", "INPUTS ARE", "IF Grade =", "RETURN bonus_amount"]
    },
    {
        "category": "Absence (Absence)",
        "instruction": "Create a Fast Formula for vacation accrual that gives more days to employees with longer service.",
        "expected_keywords": ["DAYS_BETWEEN", "PER_ASG_REL_ORIGINAL_DATE_OF_HIRE", "IF years_service >=", "RETURN accrual"]
    },
    {
        "category": "Overtime (Payroll)",
        "instruction": "Write a formula to calculate overtime pay. Overtime is paid at 1.5x for hours over 40.",
        "expected_keywords": ["IF hours_worked >", "overtime_pay =", "regular_pay =", "RETURN total_pay"]
    },
    {
        "category": "Deduction (Payroll)",
        "instruction": "Write a formula to calculate a deduction that is a percentage of earnings, subject to a minimum and maximum.",
        "expected_keywords": ["deduction_amt =", "IF deduction_amt <", "IF deduction_amt >", "RETURN deduction_amt"]
    },
    {
        "category": "Earning Proration (Payroll)",
        "instruction": "Write a formula to prorate an earning based on FTE (Full Time Equivalent).",
        "expected_keywords": ["PER_ASG_FTE_VALUE", "actual_amount =", "target_amount * fte", "RETURN actual_amount"]
    },
    {
        "category": "Benefit Eligibility (Benefits)",
        "instruction": "Write a formula to determine eligibility for a benefit based on age and length of service.",
        "expected_keywords": ["MONTHS_BETWEEN", "PER_PER_DATE_OF_BIRTH", "eligible = 'Y'", "RETURN eligible"]
    },
    {
        "category": "Time Validation (Time)",
        "instruction": "Write a formula to validate that daily hours do not exceed a maximum limit.",
        "expected_keywords": ["valid = 'N'", "message =", "IF", "RETURN valid, message"]
    },
    {
        "category": "UDT Lookup (Advanced)",
        "instruction": "Write a formula that retrieves a value from a User Defined Table (UDT) based on a row and column.",
        "expected_keywords": ["GET_TABLE_VALUE", "table_name =", "row_value =", "RETURN return_value"]
    }
]

def evaluate():
    print("Loading model...")
    try:
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
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure training has completed and 'output' directory exists.")
        return

    print(f"\nRunning {len(TEST_CASES)} test cases...\n")
    print("-" * 80)

    for i, test in enumerate(TEST_CASES):
        print(f"Test Case {i+1}: {test['category']}")
        print(f"Instruction: {test['instruction']}")
        
        prompt = f"### Instruction:\n{test['instruction']}\n\n### Response:\n"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs, 
            max_new_tokens=512, 
            do_sample=True, 
            temperature=0.2,
            top_p=0.95
        )
        
        generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract just the response part (simple heuristic)
        if "### Response:" in generated_code:
            code_only = generated_code.split("### Response:")[1].strip()
        else:
            code_only = generated_code

        print("\nGenerated Code:")
        print(code_only[:500] + "..." if len(code_only) > 500 else code_only)
        
        # Verification
        missing_keywords = [kw for kw in test['expected_keywords'] if kw not in code_only]
        
        if not missing_keywords:
            print("\n✅ PASS")
        else:
            print(f"\n❌ FAIL - Missing keywords: {missing_keywords}")
            
        print("-" * 80)

if __name__ == "__main__":
    evaluate()
