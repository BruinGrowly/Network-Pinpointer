import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from network_pinpointer.semantic_storage import SemanticStorage

print("Testing SemanticStorage...")
storage = SemanticStorage()

targets = storage.get_all_targets()
print(f"Targets: {targets}")

for target in targets:
    profile = storage.get_profile(target)
    print(f"Profile for {target}: {profile.keys() if profile else 'None'}")
    if profile:
        print(f"  Mass: {profile.get('semantic_mass')}")

