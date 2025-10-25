import argparse
from agent_content_crew.src.crew import ContentCrew

def run(product_idea: str):
    """
    Run the content creation crew with a specific product idea.
    
    Args:
        product_idea (str): The product idea to pass to the crew.
    """
    
    product_input = {
        'product_idea': product_idea
    }

    print("\n--- Starting Content Crew for: {product_idea} ---")
    
    # Create an instance of the crew and kick it off
    crew_instance = ContentCrew()
    result = crew_instance.create_crew().kickoff(inputs=product_input)
    
    print("\n--- Content Crew Finished ---")
    print("\nFinal Result:")
    print(result)
    print("\n--- Check 'final_content.md' for the output ---")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Content Creation Crew with a specific product idea."
    )
    
    parser.add_argument(
        "product_idea",
        type=str,
        help="The product idea you want the crew to work on (e.g., 'An AI-powered hiking app')."
    )
    args = parser.parse_args()
    
    run(args.product_idea)
