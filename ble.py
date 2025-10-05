import subprocess

def is_device_connected(device_identifier):
    """
    Returns True if a device with the given name or MAC address is connected.
    device_identifier: str (e.g., "ESP32 Keyboard" or "EC:E3:34:B3:14:9E")
    """
    result = subprocess.run(
        ["bluetoothctl", "devices", "Connected"],
        capture_output=True, text=True
    )
    for line in result.stdout.strip().splitlines():
        if device_identifier in line:
            return True
    return False

# Example usage:
if __name__ == "__main__":
    # Replace with your device name or MAC address
    print(is_device_connected("ESP32 Keyboard"))  # True if connected
    print(is_device_connected("EC:E3:34:B3:14:9E"))  # True if connected