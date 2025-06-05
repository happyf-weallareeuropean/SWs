import time
from collections import defaultdict

from pynput import keyboard, mouse

# Duration in seconds to monitor actions
DURATION = 60

pressed_keys = set()
counts = defaultdict(int)

dragging = False
last_pos = None
movement = 0
DRAG_THRESHOLD = 10  # pixels


def on_press(key):
    if key in (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
        pressed_keys.add('cmd')
    else:
        pressed_keys.add(str(key))
    # Detect cmd+tab
    if 'cmd' in pressed_keys and str(key) == 'Key.tab':
        counts['cmd_tab'] += 1
    # Detect cmd+space
    if 'cmd' in pressed_keys and str(key) == 'Key.space':
        counts['cmd_space'] += 1
    # Exit early on ESC
    if key == keyboard.Key.esc:
        return False


def on_release(key):
    if key in (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
        pressed_keys.discard('cmd')
    else:
        pressed_keys.discard(str(key))


def on_move(x, y):
    global movement, last_pos
    if dragging and last_pos is not None:
        dx = x - last_pos[0]
        dy = y - last_pos[1]
        movement += (dx * dx + dy * dy) ** 0.5
        last_pos = (x, y)


def on_click(x, y, button, pressed):
    global dragging, last_pos, movement
    if button == mouse.Button.left:
        if pressed:
            dragging = True
            last_pos = (x, y)
            movement = 0
        else:
            if dragging and movement > DRAG_THRESHOLD:
                counts['drag'] += 1
            dragging = False
            last_pos = None


if __name__ == '__main__':
    msg = (
        f"Monitoring actions for {DURATION} seconds. "
        "Press ESC to quit early."
    )
    print(msg)
    start = time.time()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as kl, \
            mouse.Listener(on_move=on_move, on_click=on_click) as ml:
        while kl.running and time.time() - start < DURATION:
            time.sleep(0.1)
        kl.stop()
        ml.stop()

    print("\nSummary of actions:")
    for k, v in counts.items():
        print(f"{k}: {v}")

    # Simple suggestions
    if counts['cmd_tab'] > 5:
        print(
            "You frequently switch apps with CMD+Tab. "
            "Consider a launcher like Raycast for custom shortcuts."
        )
    if counts['cmd_space'] > 5:
        print(
            "You used Spotlight often. "
            "Raycast can replace or extend it with more actions."
        )
    if counts['drag'] > 5:
        print(
            "Many mouse drag operations detected. "
            "A window manager with hotkeys could speed this up."
        )
