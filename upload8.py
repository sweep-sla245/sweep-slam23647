import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION GITHUB ---
# Place ton APK dans le même dossier que ton script sur GitHub
APK_PATH = "Digiminer.apk"
USER_IDS = ["2306001", "2306002", "2306003", "2306004", "2306005", "2306006", "2306007", "2306008", "2306009", "23060010", "23060011", "23060012", "23060013", "23060014", "23060015", "23060016", "23060017", "23060018", "23060019", "23060020", "23060021", "23060022", "23060023", "23060024", "23060025", "23060026", "23060027", "23060028", "23060029", "23060030", "23060031", "23060032", "23060033", "23060034", "23060035", "23060036", "23060037", "23060038", "23060039", "23060040", "23060041", "23060042", "23060043", "23060044", "23060045", "23060046", "23060047", "23060048", "23060049", "23060050", "23060051", "23060052", "23060053", "23060054", "23060055", "23060056", "23060057", "23060058", "23060059", "23060060","23060061","23060062","23060063","23060064",]

def upload_apk_final(uid):
    print(f"\n--- [ID {uid}] Démarrage ---")
    
    if not os.path.exists(APK_PATH):
        print(f"❌ Erreur : Fichier {APK_PATH} introuvable dans le dépôt.")
        return

    # --- CONFIGURATION SANS GRAPHIQUE (HEADLESS) ---
    co = ChromiumOptions()
    co.set_argument('--headless')  # Pas d'interface graphique
    co.set_argument('--no-sandbox') # Nécessaire pour les serveurs Linux
    co.set_argument('--disable-gpu')
    
    page = ChromiumPage(co)
    try:
        page.get(f'https://www.uptoplay.net/filemanager.php?username={uid}')
        time.sleep(10) # Temps d'attente augmenté pour Cloudflare sur serveur
        
        cookies = {c['name']: c['value'] for c in page.cookies()}
        ua = page.user_agent
        page.quit()

        print(f"[{uid}] Envoi réel du fichier...")
        url = "https://www.uptoplay.net/filemanager.php"
        params = {'service': 'apkonserver01', 'username': uid}
        data = {'api': 'upload', 'dir': ''}

        with open(APK_PATH, 'rb') as f:
            files = {'file': (os.path.basename(APK_PATH), f, 'application/vnd.android.package-archive')}
            headers = {'User-Agent': ua}
            
            response = requests.post(
                url, 
                params=params, 
                cookies=cookies, 
                data=data, 
                files=files, 
                headers=headers
            )

        if response.status_code == 200:
            if "filemanager.php" in response.text or "Digiminer.apk" in response.text:
                print(f"✅ [ID {uid}] Téléchargement REUSSI !")
            else:
                print(f"⚠️ [ID {uid}] Réponse inattendue (Cloudflare a peut-être bloqué le POST).")
        else:
            print(f"❌ [ID {uid}] Erreur serveur : {response.status_code}")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        if 'page' in locals(): page.quit()

# Lancement
for uid in USER_IDS:
    upload_apk_final(uid)
    time.sleep(5)
