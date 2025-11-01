from .cli.brief_collector import collect_brief
from .models.content_models import MarketingBrief
from .crew import ContentCrew

from .config.settings import settings
from .config.logger import logger

def run(product_idea: str):
    """
    Run the content creation crew by first collecting a comprehensive
    marketing brief
    """

    try:
        brief_data = collect_brief()

        # 3. Validate the data with Pydantic
        brief = MarketingBrief(**brief_data)
    except Exception as e:
        logger.error(f"Error during brief collection or validation: {e}")
        return
    
    bucket_name = settings.MINIO_BUCKET_NAME
    
    if not bucket_name:
        raise ValueError("MINIO_BUCKET_NAME environment variable not set or .env file not loaded.")
    
    crew_inputs = {

        **brief.dict(),

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
    crew_instance = ContentCrew()
    result = crew_instance.create_crew().kickoff(inputs=crew_inputs)
    
    logger.info("\n--- Content Crew Finished ---")
    logger.SHOW_FINAL_RESULT = True
    logger.info(f"Final Result:\n{result}")
    logger.info("--- Check your MinIO bucket for the output ---")
    
    
if __name__ == "__main__":
    logger.info("Logger initialized. Starting brief collection...")
    run()
