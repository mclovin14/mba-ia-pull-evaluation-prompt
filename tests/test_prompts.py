"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import os
from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @pytest.fixture(scope="class")
    def prompt_data(self):
        """
        Carrega os dados do prompt dinamicamente baseado na variável de ambiente PROMPT_FILE.
        Se a variável não for fornecida, assume bug_to_user_story_v2.yml como padrão.
        """
        prompt_filename = os.getenv("PROMPT_FILE", "bug_to_user_story_v2.yml")
        path = Path(__file__).parent.parent / "prompts" / prompt_filename
        
        if not path.exists():
            pytest.fail(f"Arquivo de prompt não encontrado: {path}")
            
        data = load_prompts(str(path))
        # O yaml tem um root key (bug_to_user_story_v1 ou similar)
        root_key = list(data.keys())[0]
        return data[root_key]

    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "O campo 'system_prompt' não foi encontrado no arquivo YAML"
        assert prompt_data["system_prompt"] is not None, "O campo 'system_prompt' não pode ser nulo"
        assert prompt_data["system_prompt"].strip() != "", "O campo 'system_prompt' não pode estar vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        role_keywords = ["você é", "atue como", "aja como", "você é um", "product manager", "especialista", "sua missão é"]
        has_role = any(keyword in system_prompt for keyword in role_keywords)
        assert has_role is True, "O prompt não define claramente uma persona (Role Prompting não encontrado)"

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        format_keywords = ["formato", "markdown", "user story:", "título:", "critérios de aceite", "**", "como um"]
        # Precisamos garantir que pelo menos algumas dessas estruturas chave estão no texto
        matches = [kw for kw in format_keywords if kw in system_prompt]
        assert len(matches) >= 2, f"O prompt não parece forçar um formato claro. Keywords encontradas: {matches}"

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        example_keywords = ["exemplo", "entrada:", "saída:", "entrada", "saída", "example"]
        has_examples = any(keyword in system_prompt for keyword in example_keywords)
        assert has_examples is True, "Não foram encontrados exemplos de entrada/saída no prompt (Few-shot faltando)"

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")
        
        # Procurando especificamente por "[TODO]" ou variações exatas isoladas
        # Não podemos buscar "TODO" em upper porque pegaria palavras como "meTODOlogias" ou "TODOS"
        assert "[TODO]" not in system_prompt, "Existem anotações '[TODO]' pendentes no system_prompt"
        assert "[TODO]" not in user_prompt, "Existem anotações '[TODO]' pendentes no user_prompt"

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list), "O campo 'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, f"É necessário listar pelo menos 2 técnicas aplicadas, mas foram encontradas apenas {len(techniques)}: {techniques}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])