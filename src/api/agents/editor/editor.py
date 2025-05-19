from promptflow.core import Prompty, AzureOpenAIModelConfiguration
import json
import os
import argparse
from dotenv import load_dotenv 
from pathlib import Path
folder = Path(__file__).parent.absolute().as_posix()


load_dotenv()

def edit(article, feedback):
    
    # Load prompty with AzureOpenAIModelConfiguration override
    configuration = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_NAME')}.cognitiveservices.azure.com/"
    )
    override_model = {
        "configuration": configuration,
        "parameters": {"max_tokens": 512}
    }
    # create path to prompty file
    path_to_prompty = folder + "/editor.prompty"

    prompty_obj = Prompty.load(path_to_prompty, model=override_model)
    result = prompty_obj(article=article, feedback=feedback,)
    
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the editor on sample text.")
    parser.add_argument("--article", default="Example article")
    parser.add_argument("--feedback", default="Example feedback")
    args = parser.parse_args()

    result = edit(args.article, args.feedback)
    print(json.loads(result))
