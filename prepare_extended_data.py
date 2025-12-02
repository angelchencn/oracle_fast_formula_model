import json
import random
import os

# Output directories
OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Templates for Fast Formula generation
TEMPLATES = [
    # --- Payroll Core ---
    {
        "type": "Deduction Calculation",
        "category": "Payroll",
        "filename": "deduction_data.jsonl",
        "instruction": "Write a formula to calculate a deduction that is a percentage of earnings, subject to a minimum and maximum.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Payroll */

INPUTS ARE {inputs}

deduction_amt = 0
earnings_amt = {earnings_dbi}

/* Calculate Percentage */
deduction_amt = earnings_amt * {pct}

/* Apply Min/Max */
IF deduction_amt < {min_amt} THEN
    deduction_amt = {min_amt}

IF deduction_amt > {max_amt} THEN
    deduction_amt = {max_amt}

RETURN deduction_amt
"""
    },
    {
        "type": "Earning Proration",
        "category": "Payroll",
        "filename": "earning_data.jsonl",
        "instruction": "Write a formula to prorate an earning based on FTE (Full Time Equivalent).",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Payroll */

DEFAULT FOR PER_ASG_FTE_VALUE IS 1

INPUTS ARE {inputs}

target_amount = {base_amount}
fte = PER_ASG_FTE_VALUE

/* Prorate based on FTE */
actual_amount = target_amount * fte

RETURN actual_amount
"""
    },
    
    # --- Benefits ---
    {
        "type": "Benefit Eligibility",
        "category": "Benefits",
        "filename": "benefit_eligibility_data.jsonl",
        "instruction": "Write a formula to determine eligibility for a benefit based on age and length of service.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Participant Eligibility */

DEFAULT FOR PER_ASG_REL_ORIGINAL_DATE_OF_HIRE IS '1900/01/01 00:00:00' (date)
DEFAULT FOR PER_PER_DATE_OF_BIRTH IS '1900/01/01 00:00:00' (date)

INPUTS ARE {inputs}

eligible = 'N'

/* Calculate Age and Service */
age = MONTHS_BETWEEN({effective_date}, PER_PER_DATE_OF_BIRTH) / 12
service_years = MONTHS_BETWEEN({effective_date}, PER_ASG_REL_ORIGINAL_DATE_OF_HIRE) / 12

IF age >= {min_age} AND service_years >= {min_service} THEN
    eligible = 'Y'

RETURN eligible
"""
    },
    
    # --- Time and Labor ---
    {
        "type": "Time Validation",
        "category": "Time",
        "filename": "time_validation_data.jsonl",
        "instruction": "Write a formula to validate that daily hours do not exceed a maximum limit.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Time Entry Rules */

INPUTS ARE {inputs}

valid = 'Y'
message = ' '

IF {hours_input} > {max_hours} THEN
(
    valid = 'N'
    message = 'Daily hours cannot exceed {max_hours}.'
)

RETURN valid, message
"""
    },
    
    # --- Advanced Syntax ---
    {
        "type": "User Defined Table",
        "category": "Advanced",
        "filename": "advanced_syntax_data.jsonl",
        "instruction": "Write a formula that retrieves a value from a User Defined Table (UDT) based on a row and column.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Payroll */

INPUTS ARE {inputs}

table_name = '{udt_name}'
row_value = {row_input}
col_name = '{col_name}'

/* Get value from UDT */
return_value = GET_TABLE_VALUE(table_name, col_name, row_value)

RETURN return_value
"""
    }
]

def generate_sample(template):
    data = {}
    
    if template["type"] == "Deduction Calculation":
        data["formula_name"] = f"DED_{random.randint(1000, 9999)}"
        data["inputs"] = "amount (number)"
        data["earnings_dbi"] = random.choice(["GROSS_EARNINGS_ASG_RUN", "REGULAR_PAY_ASG_RUN"])
        data["pct"] = str(random.choice([0.01, 0.02, 0.05, 0.10]))
        data["min_amt"] = str(random.randint(10, 50))
        data["max_amt"] = str(random.randint(200, 1000))
        
    elif template["type"] == "Earning Proration":
        data["formula_name"] = f"EARN_{random.randint(1000, 9999)}"
        data["inputs"] = "date_earned (date)"
        data["base_amount"] = str(random.choice([1000, 2000, 5000]))
        
    elif template["type"] == "Benefit Eligibility":
        data["formula_name"] = f"BEN_ELIG_{random.randint(1000, 9999)}"
        data["inputs"] = "IV_EFFECTIVE_DATE (date)"
        data["effective_date"] = "IV_EFFECTIVE_DATE"
        data["min_age"] = str(random.randint(18, 25))
        data["min_service"] = str(random.randint(1, 5))
        
    elif template["type"] == "Time Validation":
        data["formula_name"] = f"TIME_VAL_{random.randint(1000, 9999)}"
        data["inputs"] = "measure (number)"
        data["hours_input"] = "measure"
        data["max_hours"] = str(random.choice([8, 10, 12, 16]))
        
    elif template["type"] == "User Defined Table":
        data["formula_name"] = f"GET_RATE_{random.randint(1000, 9999)}"
        data["inputs"] = "grade_code (text)"
        data["udt_name"] = random.choice(["MY_RATES", "BONUS_PCT", "SHIFT_DIFF"])
        data["row_input"] = "grade_code"
        data["col_name"] = random.choice(["RATE", "VALUE", "AMOUNT"])

    code = template["code_template"].format(**data)
    
    return {
        "instruction": template["instruction"],
        "input": "",
        "output": code.strip(),
        "filename": template["filename"]
    }

def main():
    print("Generating extended synthetic data...")
    
    # Group samples by filename
    file_samples = {}
    
    for _ in range(200): # Generate 200 samples total
        tmpl = random.choice(TEMPLATES)
        sample = generate_sample(tmpl)
        filename = sample.pop("filename") # Remove filename from json output
        
        if filename not in file_samples:
            file_samples[filename] = []
        file_samples[filename].append(sample)
        
    # Write to files
    for filename, samples in file_samples.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w') as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")
        print(f"Generated {len(samples)} samples in {filename}")

if __name__ == "__main__":
    main()
