"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    client = Client()
    prompt = client.pull_prompt("leonanluppi/bug_to_user_story_v1")

    # Inicializa variáveis para o prompt
    system_prompt = ""
    user_prompt = ""
    
    # Extrai os textos do ChatPromptTemplate do LangChain
    if hasattr(prompt, "messages"):
        for msg in prompt.messages:
            msg_type = msg.__class__.__name__
            if msg_type == "SystemMessagePromptTemplate":
                system_prompt = msg.prompt.template
            elif msg_type == "HumanMessagePromptTemplate":
                user_prompt = msg.prompt.template

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "created_at": "2025-01-15",
            "tags": ["bug-analysis", "user-story", "product-management"]
        }
    }

    if not save_yaml(prompt_data, "prompts/bug_to_user_story_v1.yml"):
        raise RuntimeError("Falha ao salvar o arquivo YAML do prompt")



def main():
    """Função principal"""
    print_section_header("Pull de prompts do LangSmith Hub")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    pull_prompts_from_langsmith()
    print("✓ Prompt salvo em prompts/bug_to_user_story_v1.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
