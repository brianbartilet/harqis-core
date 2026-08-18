import os
import sys
import threading
import traceback
from pathlib import Path
from datetime import datetime
import faulthandler
import psutil


def main() -> None:
    """
    Entry-point wrapper for the desktop activity logger.

    This exists so that:
    - Import-time errors in core.utilities.capture.actions are captured.
    - Any unhandled exceptions inside run_capture are logged to actions_crash.log.
    - Fatal crashes (segfaults, etc.) dump a faulthandler trace to actions_crash.log.
    """

    # Read log_dir from CLI, default to current working directory
    if len(sys.argv) > 1:
        log_dir = sys.argv[1]
    else:
        log_dir = "."

    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)

    crash_file = log_dir_path / "actions_crash.log"
    bootstrap_file = log_dir_path / "actions_bootstrap.log"

    # Basic bootstrap log so we can see lifecycle events
    def _boot(msg: str) -> None:
        ts = datetime.now().isoformat()
        try:
            with bootstrap_file.open("a", encoding="utf-8") as f:
                f.write(f"{ts} - {msg}\n")
        except Exception:
            # If we can't log bootstrap info, just ignore
            pass

    _boot("actions_entry.main started")
    _boot(f"  pid = {os.getpid()}")
    _boot(f"  sys.argv = {sys.argv!r}")

    try:
        max_memory_mb = max(128, int(os.environ.get("CAPTURE_MAX_MEMORY_MB", "768")))
    except ValueError:
        max_memory_mb = 768
    watchdog_stop = threading.Event()

    def _memory_watchdog() -> None:
        process = psutil.Process()
        while not watchdog_stop.wait(1.0):
            try:
                memory = process.memory_info()
                private_bytes = getattr(memory, "private", memory.rss)
                private_mb = private_bytes / (1024 * 1024)
                if private_mb >= max_memory_mb:
                    _boot(
                        "MEMORY_WATCHDOG_EXIT "
                        f"pid={os.getpid()} private_memory_mb={private_mb:.1f} "
                        f"limit_mb={max_memory_mb}"
                    )
                    os._exit(70)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return

    threading.Thread(
        target=_memory_watchdog,
        name="capture-memory-watchdog",
        daemon=True,
    ).start()
    _boot(f"memory watchdog enabled limit_mb={max_memory_mb}")

    # Try to open crash file early and enable faulthandler on it
    fh = None
    try:
        fh = crash_file.open("a", encoding="utf-8")
        fh.write(f"=== faulthandler session start {datetime.now().isoformat()} ===\n")
        fh.flush()
        faulthandler.enable(fh)
        _boot("faulthandler enabled")
    except Exception:
        # If this fails, we still continue; just no faulthandler
        _boot("WARNING: failed to enable faulthandler")

    try:
        # Import inside try so ANY import error is captured here
        _boot("importing run_capture...")
        from core.utilities.capture.actions import run_capture

        _boot("imported run_capture OK")

        # Now run the main loop
        _boot("calling run_capture()")
        run_capture(
            rotation="hourly",
            log_clipboard_text=True,
            log_clipboard_images=True,
            log_open_apps=True,
            mask_secrets_enabled=True,
            log_dir=log_dir,
        )
        _boot("run_capture() returned normally")

    except KeyboardInterrupt:
        _boot("KeyboardInterrupt caught in actions_entry")
        print("\nStopped by user.")

    except Exception:
        # Log crash to file (Python-level exceptions)
        _boot("EXCEPTION in actions_entry, writing to actions_crash.log")
        try:
            if fh is None:
                # If we failed earlier, open crash file now
                with crash_file.open("a", encoding="utf-8") as f:
                    f.write(f"=== Crash at {datetime.now().isoformat()} ===\n")
                    traceback.print_exc(file=f)
                    f.write("\n")
            else:
                fh.write(f"=== Crash at {datetime.now().isoformat()} ===\n")
                traceback.print_exc(file=fh)
                fh.write("\n")
                fh.flush()
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

    finally:
        watchdog_stop.set()
        _boot("actions_entry.main exiting")
        # Clean up faulthandler file
        try:
            if fh is not None:
                fh.flush()
                fh.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
