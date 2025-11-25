import sys
import traceback
from pathlib import Path
from datetime import datetime


def main():
    # Read log_dir from CLI
    if len(sys.argv) > 1:
        log_dir = sys.argv[1]
    else:
        log_dir = "."

    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)

    crash_file = log_dir_path / "actions_crash.log"

    try:
        # Import inside try so import errors are captured
        from core.utilities.capture.actions import run_capture

        run_capture(
            rotation="hourly",
            log_clipboard_text=True,
            log_clipboard_images=True,
            log_open_apps=True,
            mask_secrets_enabled=True,
            log_dir=log_dir,
        )

    except KeyboardInterrupt:
        print("\nStopped by user.")

    except Exception:
        # Log crash to file
        try:
            with crash_file.open("a", encoding="utf-8") as f:
                f.write(f"=== Crash at {datetime.now().isoformat()} ===\n")
                traceback.print_exc(file=f)
                f.write("\n")
        except Exception:
            print("Failed to write actions_crash.log")

        # Print traceback to console (if visible)
        print("UNHANDLED EXCEPTION IN actions_entry:")
        traceback.print_exc()

        # Keep console open if interactive
        try:
            input("Press Enter to close this window...")
        except EOFError:
            pass


if __name__ == "__main__":
    main()
