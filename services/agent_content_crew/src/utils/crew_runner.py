from halo import Halo
from ..config.logger import logger

def run_crew(crew, inputs, start_text, success_text, failure_text):
    """
        Runs a crew.kickoff() method.
        Handles success, failure, and exceptions.
    """
    spinner = Halo(text=start_text, spinner='dots')
    try:
        spinner.start()
        result = crew.kickoff(inputs=inputs)
        spinner.succeed(success_text)
        return result
    except Exception as e:
        spinner.fail(f"{failure_text}: {e}")
        logger.error(f"Error running crew: {e}", exc_info=True)
        return None