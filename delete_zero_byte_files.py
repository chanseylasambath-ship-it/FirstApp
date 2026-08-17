# Zero_byte_cleanup.py

import configparser
import logging
from pathlib import Path


LOGGER = logging.getLogger(__name__)


def setup_logger(log_file):
    """
    Configure logging to record ONLY errors and critical failures.
    """
    log_path = Path(log_file)

    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RuntimeError(
            f"Unable to create log directory: {log_path.parent}"
        ) from exc

    # Remove existing handlers so logging can be configured reliably.
    LOGGER.handlers.clear()

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
    )

    LOGGER.setLevel(logging.ERROR)
    LOGGER.addHandler(handler)
    LOGGER.propagate = False


def delete_zero_byte_files(folder_path):
    """
    Delete zero-byte files from the given folder.

    Returns:
        int: Number of files successfully deleted.
    """
    folder = Path(folder_path)

    if not folder.exists():
        LOGGER.error("Process folder does not exist: %s", folder)
        return 0

    if not folder.is_dir():
        LOGGER.error("Process path is not a directory: %s", folder)
        return 0

    deleted_count = 0

    try:
        entries = folder.iterdir()
    except OSError as exc:
        LOGGER.error(
            "Unable to access process folder %s: %s",
            folder,
            exc
        )
        return 0

    for file_path in entries:
        try:
            if file_path.is_file() and file_path.stat().st_size == 0:
                file_path.unlink()
                deleted_count += 1

        except OSError as exc:
            LOGGER.error(
                "Failed to delete %s: %s",
                file_path,
                exc
            )
        except Exception as exc:
            LOGGER.error(
                "Unexpected error processing %s: %s",
                file_path,
                exc
            )

    return deleted_count


def load_config(config_file="settings.ini"):
    """
    Load and validate the configuration file.
    """
    config = configparser.ConfigParser()
    config_path = Path(config_file)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    config.read(config_path)

    if "GENERAL" not in config:
        raise ValueError(
            "Missing [GENERAL] section in configuration file."
        )

    if "log_file" not in config["GENERAL"]:
        raise ValueError(
            "Missing 'log_file' in [GENERAL] section."
        )

    return config


def main():
    """
    Main entry point.
    """
    try:
        config = load_config("settings.ini")

        log_file = config["GENERAL"]["log_file"]
        setup_logger(log_file)

    except Exception as exc:
        # Logging may not be configured yet, so print the error.
        print(f"Startup error: {exc}")
        return

    for section in config.sections():
        if section.upper() == "GENERAL":
            continue

        try:
            if "process_folder" not in config[section]:
                LOGGER.error(
                    "Missing 'process_folder' in section [%s]",
                    section
                )
                continue

            process_folder = config[section]["process_folder"]

            delete_zero_byte_files(process_folder)

        except Exception as exc:
            LOGGER.error(
                "Error processing section [%s]: %s",
                section,
                exc
            )


if __name__ == "__main__":
    main()