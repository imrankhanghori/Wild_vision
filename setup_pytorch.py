"""
PyTorch Compatibility Setup
Run this script if you encounter PyTorch 2.6 model loading issues
"""

import torch
import sys

def setup_pytorch_compatibility():
    """Configure PyTorch for Ultralytics YOLO compatibility."""
    
    print(f"PyTorch version: {torch.__version__}")
    
    # For PyTorch 2.6+, add safe globals for Ultralytics
    if hasattr(torch.serialization, 'add_safe_globals'):
        print("✅ Detected PyTorch 2.6+, configuring safe globals...")
        
        try:
            from ultralytics.nn.tasks import DetectionModel
            from ultralytics.nn.modules import Conv, Bottleneck, C2f, SPPF
            
            # Add all Ultralytics classes as safe globals
            torch.serialization.add_safe_globals([
                DetectionModel,
                Conv,
                Bottleneck,
                C2f,
                SPPF
            ])
            
            print("✅ PyTorch configured for Ultralytics compatibility")
            return True
            
        except ImportError as e:
            print(f"⚠️ Warning: Could not import Ultralytics modules: {e}")
            return False
    else:
        print("✅ PyTorch < 2.6, no configuration needed")
        return True


if __name__ == "__main__":
    setup_pytorch_compatibility()
