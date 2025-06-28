import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU : {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU found'}")