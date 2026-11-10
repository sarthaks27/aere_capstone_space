'''
Toggle based on Keyboard
Turn on GPIO0..GPIO3 using WASD keyboard
Prof. Nelson
'''
import sys
import termios
import tty
import select
from gpiozero import LED

# ---- Configuration ----
RELAY_PINS = list(range(24))   # GPIO0–GPIO23
ACTIVE_LOW = False             # change to True if relay board is active LOW

# Create relay objects
relays = [LED(pin, active_high=not ACTIVE_LOW) for pin in RELAY_PINS]

# thruster number - GPIO pin
Z3 = 0; Z1 = 1; Y1 = 2; X1 = 3; X6 = 4; Z2 = 5
Y2 = 6; X2 = 7; Y3 = 8; Z4 = 9; Y4 = 10; X4 = 11
X3 = 12; Z7 = 13; Y7 = 14; X7 = 15; Y6 = 16; Z5 = 17
Y5 = 18; X5 = 19; Z6 = 20; Z8 = 21; Y8 = 22; X8 = 23
# Map keyboard keys to relay indices

key_map = {
    'w': [X5, X6, X7, X8], # forward
    'a': [Y1, Y3, Y5, Y7], # left
    's': [X1, X2, X3, X4], # back
    'd': [Y2, Y4, Y6, Y8], # right
    '2': [Z3, Z4, Z7, Z8], # up
    'x': [Z1, Z2, Z5, Z6], # down
    '1': [Z1, Z2, X7, X8], # pitch up
    'z': [X3, X4, X5, X6], # pitch down
    'q': [Y1, Y4, Y5, Y8], # roll left
    'e': [Y2, Y3, Y6, Y7], # roll right
    't': [Y2, Y4, Y5, Y7], # yaw left
    'y': [Y1, Y3, Y6, Y8], # yaw right
}

# Track state of each relay
relay_state = [False] * len(relays)

# ---- Make sure all relays are turned OFF ----
# ---- Terminal setup ----
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

print("Startuip reset: all relays OFF")
print("WASD toggle demo controlling GPIO0–GPIO3")
print("Press Ctrl+C to exit")

try:
    while True:
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1).lower()

            if key in key_map:
                idx = key_map[key]

                # Toggle state
                relay_state[idx] = not relay_state[idx]

                if relay_state[idx]:
                    relays[idx].on()
                    print(f"Relay {idx} ON")
                else:
                    relays[idx].off()
                    print(f"Relay {idx} OFF")

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    # Safety: turn everything off
    for r in relays:
        r.off()
