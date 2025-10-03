#   By Fahad Alduraibi
#   2025
#   Version: 1.0
#   Logic analyzer (Logicuino)
#   using an Arduino (ATmega328P) board

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from collections import deque

# --- Configuration ---
SERIAL_PORT = "/dev/ttyACM0"   # Change to COMx on Windows if needed
BAUD_RATE = 1000000 # Must match Arduino setting
NUM_CHANNELS = 8
BUFFER_SIZE = 10000
ROW_SPACING = 1.5

# --- Serial setup ---
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)

# --- Buffers ---
time_buffer = deque(maxlen=BUFFER_SIZE)
signal_buffers = [deque(maxlen=BUFFER_SIZE) for _ in range(NUM_CHANNELS)]
sample_index = 0

# --- Plot setup ---
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.15)  # make space for button
lines = []
for ch in range(NUM_CHANNELS,0, -1):
    line, = ax.plot([], [], lw=1, label=f"CH{ch}")  # label as CH0 - CH7
    lines.append(line)

ax.set_ylim(-0.1, NUM_CHANNELS * ROW_SPACING)
ax.legend(loc="upper right")
ax.set_xlabel("Sample index")
ax.set_ylabel("Channels")

# --- Zoom & Pan state ---
time_scale = 1.0
x_offset = 0
is_panning = False
last_mouse_x = None
is_frozen = False  # <-- freeze state

# --- Freeze button ---
def toggle_freeze(event):
    global is_frozen
    is_frozen = not is_frozen
    if is_frozen:
        button.label.set_text("Resume")
    else:
        button.label.set_text("Freeze")
        
ax_button = plt.axes([0.8, 0.02, 0.15, 0.05])  # x, y, width, height
button = Button(ax_button, 'Freeze')
button.on_clicked(toggle_freeze)

# --- Keyboard zoom ---
def on_key(event):
    global time_scale
    if event.key == '+':
        time_scale = max(0.01, time_scale / 2)
    elif event.key == '-':
        time_scale = min(10, time_scale * 2)

# --- Mouse zoom & pan ---
def on_scroll(event):
    global time_scale
    if event.button == 'up':
        time_scale = max(0.01, time_scale / 1.5)
    elif event.button == 'down':
        time_scale = min(10, time_scale * 1.5)

def on_press(event):
    global is_panning, last_mouse_x
    if event.button == 1:
        is_panning = True
        last_mouse_x = event.xdata

def on_release(event):
    global is_panning
    if event.button == 1:
        is_panning = False

def on_motion(event):
    global x_offset, last_mouse_x
    if is_panning and event.xdata is not None and last_mouse_x is not None:
        dx = last_mouse_x - event.xdata
        x_offset += dx
        last_mouse_x = event.xdata

fig.canvas.mpl_connect("key_press_event", on_key)
fig.canvas.mpl_connect("scroll_event", on_scroll)
fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("motion_notify_event", on_motion)

# --- Update loop ---
def update(frame):
    global sample_index
    if not is_frozen:
        data = ser.read(500)
        for byte in data:
            time_buffer.append(sample_index)
            for ch in range(NUM_CHANNELS):
                bit = (byte >> ch) & 1
                signal_buffers[ch].append(bit + ch * ROW_SPACING)
            sample_index += 1

        if len(time_buffer) > 0:
            window = int(BUFFER_SIZE * time_scale)
            x_max = sample_index - x_offset
            x_min = max(0, x_max - window)
            ax.set_xlim(x_min, x_max)

            for ch in range(NUM_CHANNELS):
                lines[ch].set_data(time_buffer, signal_buffers[ch])

    return lines

ani = animation.FuncAnimation(fig, update, interval=30, blit=False)
plt.show()
