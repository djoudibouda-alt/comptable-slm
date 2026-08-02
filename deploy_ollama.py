"""
Script de déploiement local pour Comptable-SLM via Ollama
"""
import os
import shutil
import subprocess
import sys


GGUF_SOURCE = "comptable-slm.Q4_K_M.gguf"
GGUF_DEST = "comptable-slm-unsloth.Q4_K_M.gguf"
MODEL_NAME = "comptable-slm"
MODELFILE = "Modelfile"


def check_ollama_installed():
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        print(f"Ollama détecté : {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("Ollama non trouvé !")
        print("Installez-le depuis : https://ollama.com/download")
        return False


def check_gguf_exists():
    if os.path.exists(GGUF_SOURCE):
        print(f"Modèle GGUF trouvé : {GGUF_SOURCE}")
        return True
    elif os.path.exists(GGUF_DEST):
        print(f"Modèle GGUF trouvé : {GGUF_DEST}")
        return True
    else:
        print(f"Fichier GGUF non trouvé !")
        print(f"Cherché : {GGUF_SOURCE} ou {GGUF_DEST}")
        return False


def create_model():
    print(f"\nCréation du modèle Ollama '{MODEL_NAME}'...")
    
    cmd = ["ollama", "create", MODEL_NAME, "-f", MODELFILE]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Modèle '{MODEL_NAME}' créé avec succès !")
        return True
    else:
        print(f"Erreur : {result.stderr}")
        return False


def test_model():
    print(f"\nTest du modèle '{MODEL_NAME}'...")
    
    test_prompt = "Quelle est la différence entre SARL et EURL en Algérie ?"
    cmd = ["ollama", "run", MODEL_NAME, test_prompt]
    
    print(f"\nQuestion : {test_prompt}")
    print("Réponse :")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    
    return result.returncode == 0


def main():
    print("=" * 60)
    print("DÉPLOIEMENT COMPTABLE-SLM")
    print("=" * 60)
    
    if not check_ollama_installed():
        sys.exit(1)
    
    if not check_gguf_exists():
        print("\nVeuillez d'abord exécuter le notebook Colab pour générer le fichier GGUF.")
        sys.exit(1)
    
    if not create_model():
        sys.exit(1)
    
    test_model()
    
    print("\n" + "=" * 60)
    print("DÉPLOIEMENT TERMINÉ !")
    print("=" * 60)
    print(f"\nPour utiliser le modèle :")
    print(f"  ollama run {MODEL_NAME}")
    print(f"\nPour poser une question :")
    print(f'  ollama run {MODEL_NAME} "Quel est le taux d\'IBS en Algérie ?"')
    print(f"\nPour lister les modèles :")
    print(f"  ollama list")


if __name__ == "__main__":
    main()
