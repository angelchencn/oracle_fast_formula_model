import json
import random
import os

# Output directories
OUTPUT_DIR = "oracle_fast_formula_model/data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "train_data.jsonl")

# Templates for Fast Formula generation
TEMPLATES = [
    {
        "type": "Bonus Calculation",
        "instruction": "Write an Oracle Fast Formula to calculate an annual bonus based on employee grade and salary.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Payroll */

ALIAS {salary_dbi} AS Salary
ALIAS {grade_dbi} AS Grade

DEFAULT FOR Salary IS 0
DEFAULT FOR Grade IS 'Entry'

INPUTS ARE {inputs}

/* Calculation Logic */
IF Grade = '{grade_high}' THEN
(
    bonus_amount = Salary * {high_pct}
)
ELSE
(
    bonus_amount = Salary * {low_pct}
)

RETURN bonus_amount
"""
    },
    {
        "type": "Absence Accrual",
        "instruction": "Create a Fast Formula for vacation accrual that gives more days to employees with longer service.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Global Absence Accrual */

DEFAULT FOR PER_ASG_REL_ORIGINAL_DATE_OF_HIRE IS '1900/01/01 00:00:00' (date)
INPUTS ARE {inputs}

/* Calculate Years of Service */
years_service = DAYS_BETWEEN({effective_date}, PER_ASG_REL_ORIGINAL_DATE_OF_HIRE) / 365

accrual = 0

IF years_service >= {tier_2_years} THEN
    accrual = {tier_2_amt}
ELSE IF years_service >= {tier_1_years} THEN
    accrual = {tier_1_amt}
ELSE
    accrual = {base_amt}

RETURN accrual
"""
    },
    {
        "type": "Overtime Calculation",
        "instruction": "Write a formula to calculate overtime pay. Overtime is paid at 1.5x for hours over 40.",
        "code_template": """
/* Formula Name: {formula_name} */
/* Type: Payroll */

INPUTS ARE {inputs}

overtime_pay = 0
regular_pay = 0

IF hours_worked > {std_hours} THEN
(
    overtime_hours = hours_worked - {std_hours}
    overtime_pay = overtime_hours * hourly_rate * {ot_rate}
    regular_pay = {std_hours} * hourly_rate
)
ELSE
(
    regular_pay = hours_worked * hourly_rate
)

total_pay = regular_pay + overtime_pay

RETURN total_pay, overtime_pay
"""
    }
]

def generate_sample(template):
    # Randomize values
    data = {}
    
    if template["type"] == "Bonus Calculation":
        data["formula_name"] = f"BONUS_CALC_{random.randint(100, 999)}"
        data["salary_dbi"] = random.choice(["CMP_ASSIGNMENT_SALARY_AMOUNT", "PAY_SALARY_ELEMENT_ENTRY_VALUE"])
        data["grade_dbi"] = "PER_ASG_GRADE_NAME"
        data["inputs"] = "bonus_date (date)"
        data["grade_high"] = random.choice(["Director", "Senior", "Manager"])
        data["high_pct"] = random.choice(["0.20", "0.15", "0.25"])
        data["low_pct"] = random.choice(["0.05", "0.10", "0.08"])
        
    elif template["type"] == "Absence Accrual":
        data["formula_name"] = f"VACATION_ACCRUAL_{random.randint(100, 999)}"
        data["effective_date"] = "IV_END_DATE"
        data["inputs"] = "IV_END_DATE (date), IV_START_DATE (date)"
        data["tier_2_years"] = str(random.randint(5, 10))
        data["tier_1_years"] = str(random.randint(1, 4))
        data["tier_2_amt"] = str(random.randint(20, 25))
        data["tier_1_amt"] = str(random.randint(15, 19))
        data["base_amt"] = str(random.randint(10, 14))
        
    elif template["type"] == "Overtime Calculation":
        data["formula_name"] = f"OT_PAY_{random.randint(100, 999)}"
        data["inputs"] = "hours_worked, hourly_rate"
        data["std_hours"] = str(random.choice([35, 40, 44]))
        data["ot_rate"] = str(random.choice([1.5, 2.0]))

    # Fill template
    code = template["code_template"].format(**data)
    
    return {
        "instruction": template["instruction"],
        "input": "",
        "output": code.strip()
    }

def main():
    print(f"Generating synthetic data to {OUTPUT_FILE}...")
    samples = []
    
    # Generate 100 samples
    for _ in range(100):
        tmpl = random.choice(TEMPLATES)
        samples.append(generate_sample(tmpl))
        
    with open(OUTPUT_FILE, 'w') as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")
            
    print(f"Generated {len(samples)} samples.")

if __name__ == "__main__":
    main()
