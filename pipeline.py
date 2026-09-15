"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments():
    """Parse command-line arguments."""
    pass  # TODO: implement


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    pass  # TODO: implement


def main():
    """Main pipeline function."""
    setup_logging(verbose=True)
    logger.debug("this is a debug message")
    logger.info("this is an info message")


if __name__ == "__main__":
    main()