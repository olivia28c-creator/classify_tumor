import argparse
import logging
from pathlib import Path

from classify_tumor.logging_config import setup_logging
from classify_tumor.service import run_prediction

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        prog="classify_tumor",
        description="Classify tumor images using a pre-trained model.",
        epilog="Thanks for using %(prog)s. For more information, visit https://www.kaggle.com/datasets/murtozalikhon/skin-cancer-classification"
    )

    parser.add_argument("image_path", help="Path to the image to be classified")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    setup_logging(args.debug)

    try:
        result = run_prediction(Path(args.image_path))
    except Exception as e:
        logger.error(str(e))
        raise SystemExit(1)

    # Output
    logger.info(
        "Prediction succesfully completed\n\tLABEL = %s\n\tCONFIDENCE = %.2f",
        result["label"],
        result["confidence"])

if __name__ == "__main__":
    main()