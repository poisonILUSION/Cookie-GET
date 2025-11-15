"""Configurações gerais do CookieGet"""

import os
from pathlib import Path

# Diretórios
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# URLs
ROBLOX_BASE_URL = "https://www.roblox.com"
ROBLOX_PROFILE_URL = "{base}/my/profile"

# Firefox/Selenium
HEADLESS = False  # Mostrar navegador
TIMEOUT = 30  # Segundos para timeout
IMPLICIT_WAIT = 10  # Espera implícita

# Logging
LOG_FILE = LOGS_DIR / "cookie_get.log"
LOG_LEVEL = "INFO"

# Cookies
COOKIE_FILENAME = "roblox_cookies.json"
COOKIES_FILE = DATA_DIR / COOKIE_FILENAME
