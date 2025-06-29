import requests
import json

def test_ai_route():
    """Test de la route /ai/ask sans token"""
    
    # URL de votre API
    url = "http://localhost:5000/ai/ask"
    
    # Données de test
    data = {
        "question": "Bonjour, comment allez-vous?"
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Test de la route: {url}")
        print(f"Données envoyées: {json.dumps(data, indent=2)}")
        
        # Faire la requête POST
        response = requests.post(url, json=data, headers=headers)
        
        print(f"\nStatut de la réponse: {response.status_code}")
        print(f"Headers de la réponse: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"Réponse: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Erreur: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Erreur: Impossible de se connecter au serveur. Assurez-vous que Flask est en cours d'exécution sur le port 5000.")
    except Exception as e:
        print(f"Erreur inattendue: {e}")

if __name__ == "__main__":
    test_ai_route() 