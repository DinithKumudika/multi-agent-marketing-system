import questionary

from ..cli.brief_collector import collect_brief
from ..config.logger import logger
from ..config.settings import settings
from ..models.content_models import MarketingBrief
from ..models.validation_models import ValidationReport
from ..crew import ValidationCrew, ContentCrew
from ..utils.crew_runner import run_crew


class CLI:
    """
    Manages the full marketing brief, validation, and content generation pipeline
    for the ContentCrew service through CLI
    """

    def __init__(self):
        self.settings = settings
        self.logger = logger

    @staticmethod
    def _print(message: str = "", **kwargs):
        kwargs.setdefault('flush', True)
        print(message, **kwargs)

    def _run(self):
        """
        Runs the main application loop.
        """
        while True:
            brief = self._collect_and_validate_brief()
            if brief is None:  # User cancelled
                break

            validation_result = self._run_validation(brief)
            if validation_result is None:  # Validation failed
                continue

            proceed = self._confirm_with_user(validation_result)
            if not proceed:  # User rejected or wants to restart
                continue

            content_result = self._run_content_generation(brief, validation_result)
            if content_result:
                self._log_final_result(content_result)

            if not self._ask_to_run_again():
                break

    def _collect_and_validate_brief(self) -> MarketingBrief | None:
        """
        Collects brief from user and validates it with Pydantic.
        Returns a valid MarketingBrief object or None if user cancels.
        """
        try:
            brief_data = collect_brief()
            return MarketingBrief(**brief_data)
        except KeyboardInterrupt:
            self.logger.info("\nUser cancelled brief collection. Exiting.")
            return None
        except Exception as e:
            self.logger.error(f"Error during brief collection or validation: {e}")
            return None

    def _run_validation(self, brief: MarketingBrief) -> ValidationReport | None:
        """
        Runs the ValidationCrew.
        Returns a ValidationReport or None if it fails.
        """
        validation_inputs = {
            **brief.dict(),
            'validator_model_provider': self.settings.VALIDATOR_LLM_PROVIDER,
            'validator_model_name': self.settings.VALIDATOR_LLM_MODEL,
        }

        validation_crew = ValidationCrew().create_crew()
        result = run_crew(
            validation_crew,
            validation_inputs,
            f"🚀 Running Market Validation for '{brief.product_name}'...",
            "Validation Complete!",
            "Validation Failed"
        )

        if result is None or not isinstance(result, ValidationReport):
            self.logger.error("Validation failed to return a valid report. Please try again.")
            return None

        return result

    def _confirm_with_user(self, report: ValidationReport) -> bool:
        """
        Shows the validation report and asks the user for confirmation to proceed.
        Returns True to proceed, False to restart.
        """
        self.logger.info(f"--- Validation Report for: {report.product_name} ---")
        self.logger.info(f"  Market Demand: {report.market_demand}")
        self.logger.info(f"  Competitor Density: {report.competitor_density}")
        self.logger.info(f"  Monetization Potential: {report.monetization_potential}")
        self.logger.info(f"  RECOMMENDATION: {report.recommendation}")
        self.logger.info(f"  FINAL SCORE: {report.viability_score} / 100")
        self.logger.info("--------------------------------------------------")

        try:
            if report.viability_score < self.settings.VALIDATION_THRESHOLD:
                self.logger.warning(
                    f"Idea scored {report.viability_score}, which is below the threshold of {self.settings.VALIDATION_THRESHOLD}.")
                proceed = questionary.confirm(
                    "Score is low. Do you want to proceed to content generation anyway?"
                ).unsafe_ask()
            else:
                self.logger.info("Validation passed!")
                proceed = questionary.confirm(
                    "Do you want to approve this brief and proceed to content generation?"
                ).unsafe_ask()

            if not proceed:
                self.logger.warning("User rejected. Restarting collection...")
                print("\n" + "=" * 50 + "\n")
                return False

            return True

        except KeyboardInterrupt:
            self.logger.info("\nUser aborted. Exiting.")
            return False

    def _run_content_generation(self, brief: MarketingBrief, report: ValidationReport):
        """
        Runs the ContentCrew.
        """
        content_inputs = {
            **brief.dict(),
            'validation_report': report.dict(),
            'bucket_name': self.settings.MINIO_BUCKET_NAME,
            'researcher_model_provider': self.settings.RESEARCHER_LLM_PROVIDER,
            'researcher_model_name': self.settings.RESEARCHER_LLM_MODEL,
            'copywriter_model_provider': self.settings.COPYWRITER_LLM_PROVIDER,
            'copywriter_model_name': self.settings.COPYWRITER_LLM_MODEL,
            'editor_model_provider': self.settings.EDITOR_LLM_PROVIDER,
            'editor_model_name': self.settings.EDITOR_LLM_MODEL,
        }

        content_crew = ContentCrew().create_crew()
        return run_crew(
            content_crew,
            content_inputs,
            "✍️ Running Content Generation (This may take a few minutes)...",
            "Content Generation Complete!",
            "Content Generation Failed"
        )

    def _log_final_result(self, content_result):
        self.logger.info("\n--- Content Crew Finished ---")
        self.logger.SHOW_FINAL_RESULT = True
        self.logger.info(f"Final Result:\n{content_result}")
        self.logger.info("--- Check your MinIO bucket for the output ---")

    def _ask_to_run_again(self) -> bool:
        """
        Asks the user if they want to run a new brief.
        Returns True to continue, False to exit.
        """
        try:
            run_again = questionary.confirm("Do you want to run a new idea brief?").unsafe_ask()
            if not run_again:
                self.logger.info("Goodbye!")
                return False
            else:
                print("\n" + "=" * 50 + "\n")
                return True
        except KeyboardInterrupt:
            self.logger.info("\nExiting. Goodbye!")
            return False

    @classmethod
    def run(cls):
        try:
            cli = cls()
            cli._run()
        except Exception as e:
            cls._print(str(e))