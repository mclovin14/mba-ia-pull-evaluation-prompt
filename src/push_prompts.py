"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        print(f"Iniciando push do prompt '{prompt_name}'...")
        
        # Cria o template do prompt com LangChain
        messages = [
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"])
        ]
        
        prompt_template = ChatPromptTemplate.from_messages(messages)
        
        client = Client()
        
        prompt_name_clean = prompt_name.split("/")[-1] if "/" in prompt_name else prompt_name
        
        client.push_prompt(
            prompt_name_clean,
            object=prompt_template,
            is_public=True,
            description=prompt_data.get("description", "")
        )
        print(f"✓ Push do prompt '{prompt_name}' concluído com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []
    
    required_fields = ['description', 'system_prompt', 'user_prompt', 'version']
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")
            
    system_prompt = prompt_data.get('system_prompt', '')
    if not system_prompt or not system_prompt.strip():
        errors.append("O campo 'system_prompt' está vazio")
        
    user_prompt = prompt_data.get('user_prompt', '')
    if not user_prompt or not user_prompt.strip():
        errors.append("O campo 'user_prompt' está vazio")
        
    techniques = prompt_data.get('techniques_applied', [])
    if not techniques:
        errors.append("Nenhuma técnica (techniques_applied) foi listada no prompt")
        
    return len(errors) == 0, errors


def main():
    """Função principal"""
    print_section_header("Push de Prompts para o LangSmith")
    
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1
        
    prompt_file = "prompts/bug_to_user_story_v2.yml"
    
    print(f"Carregando {prompt_file}...")
    yaml_data = load_yaml(prompt_file)
    
    if not yaml_data:
        print(f"❌ Não foi possível carregar {prompt_file}")
        return 1
        
    prompt_key = list(yaml_data.keys())[0]
    prompt_data = yaml_data[prompt_key]
    
    print("Validando estrutura do prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    
    if not is_valid:
        print("❌ Validação falhou. Erros encontrados:")
        for err in errors:
            print(f"  - {err}")
        print("\nCorrija os erros antes de enviar ao LangSmith.")
        return 1
        
    print("✓ Validação concluída com sucesso.")
    
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    
    if not username:
        print("❌ A variável USERNAME_LANGSMITH_HUB não está configurada no .env.")
        return 1

    prompt_name_to_push = f"{username}/bug_to_user_story_v2"
    
    print(f"Enviando como: {prompt_name_to_push}")
    success = push_prompt_to_langsmith(prompt_name_to_push, prompt_data)
    
    if success:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
