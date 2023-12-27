import json
import sys
def validate_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            testnet_data = data.get('testnet', {})
            
            key_1 = testnet_data.get('1', [])
            key_2 = testnet_data.get('2', [])

            if isinstance(key_1, list) and isinstance(key_2, list):
                if len(key_1) >= 1 and len(key_2) >= 1:
                    print("Validation successful")
                    return True
                else:
                    print("Validation failed: Keys '1' and '2' under 'testnet' must have at least one item.")
                    return False
            else:
                print("Validation failed: Keys '1' and '2' under 'testnet' must be arrays.")
                return False

    except FileNotFoundError:
        print(f"Validation failed: File not found at {file_path}")
        return False

# Replace 'sdkSeedProviders.json' with the actual file path
file_path = 'sdkSeedProviders.json'
result = validate_json(file_path)
if not result:
    sys.exit(1)
