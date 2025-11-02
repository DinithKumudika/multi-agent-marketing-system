from .cli.cli import CLI
from .config.logger import logger

def run():
    """
    Initializes and runs the main Content Pipeline.
    """
    try:
        CLI.run()
    except Exception as e:
            logger.error(f"A critical unhandled error occurred: {e}", exc_info=True)
    finally:
        logger.info("Application shutting down.")

if __name__ == "__main__":
    logger.info("Logger initialized. Starting Content Pipeline...")
    run()
