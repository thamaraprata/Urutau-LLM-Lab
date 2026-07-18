"""
Testes básicos dos challenges.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from llm.challenges import ChallengeManager


def test_challenges_loaded():
    """Testa que os challenges foram carregados."""
    manager = ChallengeManager()
    challenges = manager.list_challenges()

    assert len(challenges) >= 5, "Deve ter pelo menos 5 challenges"
    print(f"✅ {len(challenges)} challenges carregados")


def test_required_fields():
    """Testa que cada challenge tem os campos obrigatórios."""
    manager = ChallengeManager()
    challenges = manager.list_challenges()

    required = ['id', 'name', 'owasp', 'difficulty', 'description']
    for challenge in challenges:
        for field in required:
            assert field in challenge, f"Challenge {challenge['id']} sem campo {field}"

    print("✅ Todos os challenges têm campos obrigatórios")


def test_get_challenge():
    """Testa buscar um challenge específico."""
    manager = ChallengeManager()
    challenge = manager.get_challenge('01')

    assert challenge is not None, "Challenge 01 deve existir"
    assert 'system_prompt' in challenge, "Challenge deve ter system_prompt"
    assert 'flag_pattern' in challenge, "Challenge deve ter flag_pattern"
    assert 'hint' in challenge, "Challenge deve ter hint"
    assert 'writeup' in challenge, "Challenge deve ter writeup"

    print("✅ Challenge 01 tem todos os campos necessários")


def test_owasp_categories():
    """Testa que os challenges cobrem categorias do OWASP LLM Top 10."""
    manager = ChallengeManager()
    challenges = manager.list_challenges()

    owasp_codes = set()
    for challenge in challenges:
        if 'LLM' in challenge['owasp']:
            # Extrai o código (ex: "LLM01" de "LLM01: Prompt Injection")
            code = challenge['owasp'].split(':')[0].strip()
            owasp_codes.add(code)

    assert len(owasp_codes) >= 3, f"Deve ter pelo menos 3 OWASP LLM codes, tem: {owasp_codes}"
    print(f"✅ Cobre {len(owasp_codes)} categorias OWASP LLM: {sorted(owasp_codes)}")


if __name__ == '__main__':
    print("🦉 Rodando testes do UrutauLLM-Lab...\n")
    test_challenges_loaded()
    test_required_fields()
    test_get_challenge()
    test_owasp_categories()
    print("\n✅ Todos os testes passaram!")
