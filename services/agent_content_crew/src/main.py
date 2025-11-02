from .cli.brief_collector import collect_brief
from .models.content_models import MarketingBrief
from .models.validation_models import ValidationReport
from .crew import ContentCrew, ValidationCrew

from .config.settings import settings
from .config.logger import logger

VALIDATION_THRESHOLD = 50

def run():
    """
    Run the full validation and content creation pipeline
    """

    try:
        brief_data = collect_brief()
        brief = MarketingBrief(**brief_data)
    except Exception as e:
        logger.error(f"Error during brief collection or validation: {e}")
        return

    # inputs for validation crew
    validation_inputs = {
        **brief.dict(),
        'validator_model_provider': settings.VALIDATOR_LLM_PROVIDER,
        'validator_model_name': settings.VALIDATOR_LLM_MODEL,
    }

    logger.info(f"--- Starting Validation Crew for: {brief.product_name} ---")
    validation_crew = ValidationCrew().create_crew()
    validation_result = validation_crew.kickoff(inputs=validation_inputs)

    if not isinstance(validation_result, ValidationReport):
        logger.error("Validation failed to return the expected report structure.")
        logger.error(f"Received: {validation_result}")
        return

    logger.info(f"--- Validation Complete ---")
    logger.info(f"  Market Demand: {validation_result.market_demand}")
    logger.info(f"  Competitor Density: {validation_result.competitor_density}")
    logger.info(f"  Monetization Potential: {validation_result.monetization_potential}")
    logger.info(f"  RECOMMENDATION: {validation_result.recommendation}")
    logger.info(f"  FINAL SCORE: {validation_result.viability_score} / 100")

    if validation_result.viability_score < VALIDATION_THRESHOLD:
        logger.warning(
            f"Idea scored {validation_result.viability_score}, which is below the threshold of {VALIDATION_THRESHOLD}.")
        logger.warning("Aborting content generation. The idea is not viable.")
        return

    logger.info(f"Validation passed! Proceeding to content generation.")
    
    bucket_name = settings.MINIO_BUCKET_NAME
    
    if not bucket_name:
        raise ValueError("MINIO_BUCKET_NAME environment variable not set or .env file not loaded.")
    
    content_crew_inputs = {
        **brief.dict(),
        'validation_report': validation_result.dict(),
        'bucket_name': bucket_name,

        # Add the LLM configs for each agent
        'researcher_model_provider': settings.RESEARCHER_MODEL_PROVIDER,
        'researcher_model_name': settings.RESEARCHER_MODEL_ID,
        
        'copywriter_model_provider': settings.COPYWRITER_MODEL_PROVIDER,
        'copywriter_model_name': settings.COPYWRITER_MODEL_ID,
        
        'editor_model_provider': settings.EDITOR_MODEL_PROVIDER,
        'editor_model_name': settings.EDITOR_MODEL_ID,
    }

    logger.info("\n--- Starting Content Crew for: {product_idea} ---")
    logger.info(f"--- Using MinIO Bucket: {bucket_name} ---")
    logger.info("--- Agent LLM Config ---")
    logger.info(f"  Researcher: {settings.RESEARCHER_MODEL_PROVIDER} / {settings.RESEARCHER_MODEL_ID}")
    logger.info(f"  Copywriter: {settings.COPYWRITER_MODEL_PROVIDER} / {settings.COPYWRITER_MODEL_ID}")
    logger.info(f"  Editor:     {settings.EDITOR_MODEL_PROVIDER} / {settings.EDITOR_MODEL_ID}")
    logger.info("------------------------")
    
    # Create an instance of the crew and kick it off
    content_crew = ContentCrew().create_crew()
    result = content_crew.kickoff(inputs=content_crew_inputs)
    
    logger.info("\n--- Content Crew Finished ---")
    logger.SHOW_FINAL_RESULT = True
    logger.info(f"Final Result:\n{result}")
    logger.info("--- Check your MinIO bucket for the output ---")
    
    
if __name__ == "__main__":
    logger.info("Logger initialized. Starting brief collection...")
    run()
