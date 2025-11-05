#!/usr/bin/env python3
"""
Network-Pinpointer Main Entry Point

Semantic Network Diagnostic Tool using LJPW Framework
"""

import sys
import os

# Add network_pinpointer to path
sys.path.insert(0, os.path.dirname(__file__))

from network_pinpointer.cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
