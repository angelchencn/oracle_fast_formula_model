from trl import SFTConfig, SFTTrainer
import inspect

print("SFTConfig args:")
try:
    print(inspect.signature(SFTConfig.__init__))
except Exception as e:
    print(e)

print("\nSFTTrainer args:")
try:
    print(inspect.signature(SFTTrainer.__init__))
except Exception as e:
    print(e)
