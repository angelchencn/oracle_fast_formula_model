from trl import SFTConfig
import inspect

print("SFTConfig fields:")
try:
    # SFTConfig is a dataclass-like object (TrainingArguments)
    # It might use __dataclass_fields__ or similar
    if hasattr(SFTConfig, '__dataclass_fields__'):
        print(list(SFTConfig.__dataclass_fields__.keys()))
    else:
        # Fallback to init params
        sig = inspect.signature(SFTConfig.__init__)
        print(list(sig.parameters.keys()))
except Exception as e:
    print(f"Error: {e}")
    print(dir(SFTConfig))
