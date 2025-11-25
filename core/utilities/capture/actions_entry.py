import sys
import traceback
from pathlib import Path
from datetime import datetime


def main() -> None:
    """
    Entry-point wrapper for the desktop activity logger.

    This exists so that:
    - Import-time errors in core.utilities.capture.actions are captured.
    - Any unhandled exceptions inside run_capture are logged to actions_crash.log.
    """

    # Read log_dir from CLI, default to current working directory
    if len(sys.argv) > 1:
        log_dir = sys.argv[1]
    else:
        log_dir = "."

    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)

    crash_file = log_dir_path / "actions_crash.log"

    # Tiny boot log so we can see that the entry actually ran
    try:
        with (log_dir_path / "actions_bootstrap.log").open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - actions_entry.main started\n")
            f.write(f"  sys.argv = {sys.argv!r}\n")
    except Exception:
        # If we can't write this, just ignore
        pass

    try:
        # Import inside try so ANY import error is captured here
        from core.utilities.capture.actions import run_capture

        # Extra marker so we know we got past import
        try:
            with (log_dir_path / "actions_bootstrap.log").open("a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} - imported run_capture OK\n")
        except Exception:
            pass

        # Now run the main loop
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
