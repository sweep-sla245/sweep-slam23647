import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions


# ============================================================
# CONFIGURATION
# ============================================================

# Dossier dans lequel se trouve ce script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# APK situé dans le même dossier que le script
APK_PATH = os.path.join(BASE_DIR, "Digiminer.apk")

# Chrome Portable
CHROME_PATH = os.path.join(
    BASE_DIR,
    "GoogleChromePortable",
    "App",
    "Chrome-bin",
    "chrome.exe"
)

USER_IDS = [
    "2306001",
    "2306002",
    "2306003",
    "2306004",
    "2306005",
    "2306006",
    "2306007",
    "2306008",
    "2306009",
    "23060010",
    "23060011",
    "23060012",
    "23060013",
    "23060014",
    "23060015",
    "23060016",
    "23060017",
    "23060018",
    "23060019",
    "23060020",
    "23060021",
    "23060022",
    "23060023",
    "23060024",
    "23060025",
    "23060026",
    "23060027",
    "23060028",
    "23060029",
    "23060030",
    "23060031",
    "23060032",
    "23060033",
    "23060034",
    "23060035",
    "23060036",
    "23060037",
    "23060038",
    "23060039",
    "23060040",
    "23060041",
    "23060042",
    "23060043",
    "23060044",
    "23060045",
    "23060056",
    "23060047",
    "23060048",
    "23060049",
    "23060050",
    "23060051",
    "23060052",
    "23060053",
    "23060054",
    "23060055",
    "23060056",
    "23060057",
    "23060058",
    "23060059",
    "23060060",
    "23060061",
    "23060062",
    "23060063",
    "23060064",
]


def upload_apk_final(uid):

    print(f"\n--- [ID {uid}] Démarrage ---")

    # Vérification de l'APK
    if not os.path.isfile(APK_PATH):
        print(f"❌ APK introuvable : {APK_PATH}")
        return

    # Vérification de Chrome Portable
    if not os.path.isfile(CHROME_PATH):
        print(f"❌ Chrome Portable introuvable : {CHROME_PATH}")
        return

    print(f"[{uid}] Chrome Portable détecté.")

    page = None

    try:
        # ====================================================
        # CONFIGURATION CHROME PORTABLE - SANS INTERFACE
        # ====================================================

        co = ChromiumOptions()

        co.set_browser_path(CHROME_PATH)

        co.set_argument("--headless")
        co.set_argument("--no-sandbox")
        co.set_argument("--disable-gpu")
        co.set_argument("--disable-dev-shm-usage")

        # ====================================================
        # OUVERTURE DE LA PAGE
        # ====================================================

        page = ChromiumPage(co)

        page.get(
            f"https://www.myandroid.org/filemanager.php?username={uid}"
        )

        time.sleep(10)

        # ====================================================
        # RÉCUPÉRATION DES COOKIES
        # ====================================================

        cookies = {
            c["name"]: c["value"]
            for c in page.cookies()
        }

        ua = page.user_agent

        print(f"[{uid}] Cookies récupérés.")

        page.quit()
        page = None

        # ====================================================
        # ENVOI DU FICHIER
        # ====================================================

        print(f"[{uid}] Envoi du fichier...")

        url = "https://www.myandroid.org/filemanager.php"

        params = {
            "service": "apkonserver01",
            "username": uid
        }

        data = {
            "api": "upload",
            "dir": ""
        }

        with open(APK_PATH, "rb") as f:

            files = {
                "file": (
                    os.path.basename(APK_PATH),
                    f,
                    "application/vnd.android.package-archive"
                )
            }

            headers = {
                "User-Agent": ua
            }

            response = requests.post(
                url,
                params=params,
                cookies=cookies,
                data=data,
                files=files,
                headers=headers,
                timeout=120
            )

        # ====================================================
        # RÉSULTAT
        # ====================================================

        if response.status_code == 200:

            if (
                "filemanager.php" in response.text
                or "Digiminer.apk" in response.text
            ):
                print(f"✅ [ID {uid}] Upload réussi !")
            else:
                print(
                    f"⚠️ [ID {uid}] "
                    "Réponse inattendue."
                )

        else:

            print(
                f"❌ [ID {uid}] "
                f"Erreur serveur : {response.status_code}"
            )

    except Exception as e:

        print(f"❌ [ID {uid}] Erreur critique : {e}")

    finally:

        if page is not None:

            try:
                page.quit()
            except:
                pass


# ============================================================
# LANCEMENT
# ============================================================

print("==============================================")
print("       APK AUTO UPLOAD - WINDOWS")
print("==============================================")
print(f"APK    : {APK_PATH}")
print(f"Chrome : {CHROME_PATH}")
print(f"IDs    : {len(USER_IDS)}")
print("==============================================")

for uid in USER_IDS:

    upload_apk_final(uid)

    time.sleep(5)

print("\n==============================================")
print("Tous les traitements sont terminés.")
print("==============================================")