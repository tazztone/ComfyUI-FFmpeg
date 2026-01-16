import sys
import os

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    print("Attempting to import AnalyzeStreamsV3...")
    from nodes.streamAnalysis_v3 import AnalyzeStreamsV3

    print("Successfully imported AnalyzeStreamsV3")
    print(f"Display Name: {AnalyzeStreamsV3.define_schema().display_name}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
