# Insta Prospect IA Simple

Outil local gratuit qui permet de :
- Récupérer des followers d’un compte Instagram
- Filtrer automatiquement ceux qui ont une photo de profil avec visage
- Générer un message personnalisé avec IA (Ollama)
- Valider et envoyer les messages manuellement

**Attention** : Utilise uniquement un **compte secondaire**. Risque de ban Instagram élevé.

## Installation (5 minutes)

### 1. Installer Ollama
- Télécharge et installe Ollama → [https://ollama.com/download](https://ollama.com/download)
- Ouvre un terminal et tape :
  ```bash
  ollama pull llama3
### 2. Installer le projet
Clone le repo (ou télécharge le ZIP)
git clone https://github.com/kylianthes/insta-prospect-ia.git
- Dans le même terminal, tape :
  ```bash
  cd (ton-chemin-d'accès)\insta-prospect-ia

# Installe les dépendances
- Tape :
  ```bash
  pip install -r requirements.txt

### 3. Lancer l’application
- Toujours dans le m^me terminal, tape :
  ```bash
  streamlit run app.py
L’application s’ouvre dans ton navigateur automatiquement.
## Comment utiliser

Connexion : Mets ton compte Instagram secondaire dans le menu de gauche.
Récupération : Entre le username d’un compte (ex: neymarjr, un influenceur, une marque, etc.)
Clique sur "Récupérer des followers"
Pour chaque profil proposé :
Lis le message généré par l’IA
Modifie-le si tu veux
Clique "Envoyer" ou "Skip"


Recommandation forte : Ne dépasse pas 15-20 messages par jour pour éviter le ban.
Limitations

Pas complètement automatique (validation humaine obligatoire)
Dépend de la stabilité d’Instagram et d’Ollama
Récupération de followers limitée (Instagram bloque vite)
