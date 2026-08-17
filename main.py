def main():
    """
    Main entry point.
    """
    try:
        base_dir = Path(__file__).resolve().parent.parent
        config_file = base_dir / "settings.ini"

        config = load_config(config_file)

        log_file = config["GENERAL"]["log_file"]
        setup_logger(log_file)

    except Exception as exc:
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