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



既然您已经有了 Bonus (奖金), Absence (缺勤), 和 Overtime (加班) 的数据，这已经覆盖了薪资计算和考勤的基础部分。

为了让模型更强大，建议从以下几个方向扩展：

1. 核心薪资 (Payroll Core) - 最重要
这是 Fast Formula 最常用的领域。

Deductions (扣减): 比如社保、公积金、税务计算、法院扣款等。
Earnings (收入项): 比如基本工资、津贴 (住房、交通)、根据 FTE (全职当量) 分摊的计算。
Gross-to-Net (税前到税后): 复杂的税务处理逻辑。
2. 福利 (Benefits)
Eligibility Profiles (资格规则): 判断员工是否有资格享受某项福利（例如：入职满6个月才有牙科保险）。
Rate Calculations (费率计算): 根据年龄、职级、地区计算保险费率。
3. 时间与劳动力 (Time and Labor)
Time Entry Validation (工时校验): 比如“连续工作不能超过6天”、“加班必须有审批”。
Time Calculation (工时计算): 将打卡时间转换为薪资工时（例如：晚班津贴、节假日3倍工资）。
4. 验证与逻辑 (Validation & Logic)
Person Selection (人员选择): 在报表或批处理中筛选特定人群。
Input Validation (输入校验): 在界面上输入值时进行校验（例如：输入的金额不能超过薪资的 50%）。
5. 高级语法 (Advanced Syntax)
User Defined Tables (UDT): 演示如何从用户自定义表中取值（非常常用）。
Arrays (数组): 处理循环逻辑，比如逐日计算考勤。
Database Items (DBI): 使用更多的数据库项来获取员工信息（职位、部门、历史薪资）。
