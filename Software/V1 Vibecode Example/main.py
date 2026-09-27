import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.hid import HIDModes

# Initialize displayio before creating the keyboard
displayio.release_displays()

# --- OLED Display Setup (Assuming 4-pin I2C) ---
i2c = busio.I2C(scl=board.IO36, sda=board.IO35)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# 128x32 is the standard resolution for a 0.91" OLED
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Create a basic text group to show on the screen
splash = displayio.Group()
text_area = label.Label(terminalio.FONT, text="KMK Wireless", color=0xFFFF00, x=10, y=15)
splash.append(text_area)
display.root_group = splash

# --- Keyboard Setup ---
keyboard = KMKKeyboard()

# --- Matrix Setup ---
keyboard.row_pins = (board.IO4, board.IO6, board.IO12, board.IO7, board.IO13, board.IO8)
keyboard.col_pins = (board.IO16, board.IO15, board.IO17, board.IO18, board.IO21, board.IO34, board.IO38, board.IO44, board.IO37, board.IO43, board.IO33, board.IO1, board.IO3, board.IO2, board.IO5)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Encoder Setup ---
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
# Replace IO11 and IO12 with your actual ESP32-S3 EC11 pins
encoder_handler.pins = ((board.IO10, board.IO9, None, False),)
encoder_handler.map = (
    ((KC.VOLD, KC.VOLU),), 
)

# --- Keymap Setup ---
keyboard.keymap = [
    [
        # Row 0
        KC.ESC, KC.N1, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.DEL,
        # Row 1
        KC.GRV,  KC.Q,  KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC, KC.UP,
        # Row 2
        KC.TAB,  KC.A,  KC.W,  KC.E,  KC.R,  KC.T,  KC.Y,  KC.U,  KC.I,  KC.O,  KC.P, KC.LBRC, KC.RBRC, KC.BSLS, KC.PSCR,
        # Row 3
        KC.CAPS, KC.Z,  KC.S,  KC.D,  KC.F,  KC.G,  KC.H,  KC.J,  KC.K,  KC.L, KC.SCLN, KC.QUOT, KC.NO, KC.ENT, KC.LEFT,
        # Row 4
        KC.LSFT, KC.LGUI,  KC.X,  KC.C,  KC.V,  KC.B,  KC.N,  KC.M,  KC.COMM, KC.DOT, KC.RGUI, KC.SLSH, KC.NO, KC.RSFT, KC.DOWN,
        # Row 5
        KC.LCTRL, KC.LALT, KC.NO, KC.NO, KC.NO, KC.SPC, KC.NO, KC.NO, KC.NO, KC.RALT, KC.NO, KC.NO, KC.NO, KC.RCTRL, KC.RIGHT
    ]
]

if __name__ == '__main__':
    # Launch the keyboard in Bluetooth mode with a custom broadcast name
    keyboard.go(hid_type=HIDModes.BLE, ble_name='Keyboard')