from trl import SFTConfig

print("Testing SFTConfig instantiation...")

try:
    config = SFTConfig(output_dir="tmp", max_seq_length=512)
    print("Success with max_seq_length")
except TypeError as e:
    print(f"Failed with max_seq_length: {e}")

try:
    config = SFTConfig(output_dir="tmp", max_length=512)
    print("Success with max_length")
except TypeError as e:
    print(f"Failed with max_length: {e}")

try:
    config = SFTConfig(output_dir="tmp", dataset_text_field="text")
    print("Success with dataset_text_field")
except TypeError as e:
    print(f"Failed with dataset_text_field: {e}")
