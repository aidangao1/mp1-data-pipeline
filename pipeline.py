import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)




def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data processing pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument(
        "--config", "-c", required=True, help="Path to the YAML configuration file"
    )
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}"
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # NEW: remember how many rows arrived, before validation drops any
    rows_loaded = len(data)

    # NEW: validation step, in its own try/except
    validation = config["validation"]
    try:
        data = validate_dataframe(
            data,
            required_columns=validation["required_columns"],
            numeric_columns=validation["numeric_columns"],
        )
    except ValueError:
        sys.exit(1)

    logger.info(f"Validation complete: {rows_loaded} -> {len(data)} rows")

    # MOVED: now after validation, so the report measures processing only
    data_before = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(data_before, data)
    logger.info(
        f"Processing complete: {report['rows_before']} → {report['rows_after']} rows"
    )

    # CHANGED: save_data() replaces data.to_csv()
    save_data(data, args.output)
    logger.info(f"Saved cleaned data to {args.output}")

    # MOVED: report prints at the very end
    print(report)


if __name__ == "__main__":
    main()