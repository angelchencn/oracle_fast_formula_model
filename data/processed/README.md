# Oracle Fast Formula Synthetic Dataset

This directory contains synthetic training data for the Oracle Fast Formula model. Each file is in JSONL format, containing instruction-input-output pairs.

## Data Files

### Core Payroll
*   **`bonus_data.jsonl`**: Formulas for calculating annual bonuses based on employee grade and salary.
*   **`overtime_data.jsonl`**: Formulas for calculating overtime pay (e.g., 1.5x rate for hours > standard).
*   **`deduction_data.jsonl`**: Formulas for calculating deductions as a percentage of earnings, with minimum and maximum limits.
*   **`earning_data.jsonl`**: Formulas for prorating earnings based on FTE (Full Time Equivalent).

### Absence Management
*   **`absence_data.jsonl`**: Formulas for vacation accrual rules based on years of service.

### Benefits
*   **`benefit_eligibility_data.jsonl`**: Formulas for determining benefit eligibility based on age and length of service.

### Time and Labor
*   **`time_validation_data.jsonl`**: Validation formulas to ensure daily hours do not exceed specific limits.

### Advanced Syntax
*   **`advanced_syntax_data.jsonl`**: Examples of using User Defined Tables (UDT) via `GET_TABLE_VALUE`.

## Format
Each line in the JSONL files is a JSON object with the following fields:
*   `instruction`: The natural language request describing what the formula should do.
*   `input`: (Optional) Additional context or inputs.
*   `output`: The corresponding Oracle Fast Formula code.
