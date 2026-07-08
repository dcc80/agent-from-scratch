import pytest
from agent import executer_calculatrice, executer_compter_caracteres, executer_outil

# Tests déterministes : on teste la logique de nos outils, pas le comportement du LLM
def test_calculatrice_addition():
    assert executer_calculatrice("addition", 2, 3) == 5

def test_calculatrice_multiplication():
    assert executer_calculatrice("multiplication", 47, 12) == 564

def test_calculatrice_division():
    assert executer_calculatrice("division", 10, 2) == 5.0

def test_compter_caracteres():
    assert executer_compter_caracteres("multiplication") == 14

def test_compter_caracteres_vide():
    assert executer_compter_caracteres("") == 0

def test_executer_outil_generique():
    # Vérifie que le registre d'outils route bien vers la bonne fonction
    resultat = executer_outil("calculatrice", {"operation": "addition", "a": 1, "b": 1})
    assert resultat == 2