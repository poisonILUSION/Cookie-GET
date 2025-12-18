# --- EXTRATOR DE COOKIES ROBLOX ---

import logging
import json
import time
import webbrowser
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from .browser import BrowserManager
from config.settings import ROBLOX_BASE_URL, ROBLOX_PROFILE_URL, DATA_DIR

logger = logging.getLogger(__name__)


class RobloxCookieExtractor:
    
    ROBLOSECURITY_COOKIE_NAME = ".ROBLOSECURITY"
    COOKIES_DATA_FILE = DATA_DIR / "saved_cookies.json"
    
    def __init__(self, timeout=30, browser_type='firefox'):
        self.browser = BrowserManager(timeout=timeout, browser_type=browser_type)
        self.profile_url = None
        self.username = None
        self.user_id = None
        self.browser_type = browser_type
    
    # --- INICIA O NAVEGADOR ---
    def start(self):
        self.browser.start()
    
    # --- SOLICITA SELEÇÃO DO NAVEGADOR ---
    def select_browser(self) -> str:
        print("\n" + "="*60)
        print("🌐 Selecione o Navegador")
        print("="*60)
        print("\n1. Google Chrome")
        print("2. Firefox")
        print("3. Opera GX")
        print("4. Microsoft Edge")
        
        while True:
            choice = input("\n➤ Escolha (1-4): ").strip()
            
            if choice == '1':
                self.browser_type = 'chrome'
                self.browser = BrowserManager(timeout=30, browser_type='chrome')
                logger.info("✅ Chrome selecionado")
                return 'chrome'
            elif choice == '2':
                self.browser_type = 'firefox'
                self.browser = BrowserManager(timeout=30, browser_type='firefox')
                logger.info("✅ Firefox selecionado")
                return 'firefox'
            elif choice == '3':
                self.browser_type = 'opera'
                self.browser = BrowserManager(timeout=30, browser_type='opera')
                logger.info("✅ Opera GX selecionado")
                return 'opera'
            elif choice == '4':
                self.browser_type = 'edge'
                self.browser = BrowserManager(timeout=30, browser_type='edge')
                logger.info("✅ Edge selecionado")
                return 'edge'
            else:
                print("❌ Opção inválida! Digite 1, 2, 3 ou 4")
    
    # --- SOLICITA INPUT DO USUÁRIO (URL ou NICK) ---
    def input_profile_info(self) -> str:
        print("\n" + "="*60)
        print("👤 Informações do Perfil")
        print("="*60)
        print("\n1. Colar link do perfil")
        print("2. Digitar nome de usuário")
        
        while True:
            choice = input("\n➤ Escolha (1-2): ").strip()
            
            if choice == '1':
                while True:
                    url = input("\n🔗 Cole o link do perfil Roblox: ").strip()
                    
                    if url.startswith(("http://", "https://")) and "roblox.com" in url.lower():
                        self.profile_url = url
                        self._extract_username_from_url(url)
                        logger.info(f"✅ URL aceita: {url}")
                        return url
                    else:
                        print("❌ URL inválida! Use: https://www.roblox.com/users/[ID]/profile")
            
            elif choice == '2':
                username = input("\n👤 Digite o nome de usuário Roblox: ").strip()
                if username:
                    self.username = username
                    # Constrói URL do perfil a partir do username
                    self.profile_url = f"https://www.roblox.com/users/profile?username={username}"
                    logger.info(f"✅ Username aceito: {username}")
                    return self.profile_url
                else:
                    print("❌ Nome de usuário não pode estar vazio")
            else:
                print("❌ Opção inválida! Digite 1 ou 2")
    
    def _extract_username_from_url(self, url: str):
        """Tenta extrair username da URL"""
        try:
            # Se conseguir pegar do padrão de ID, faz uma requisição para pegar o username
            user_id = self._extract_user_id_from_url()
            if user_id:
                try:
                    response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        self.username = data.get('name', 'Desconhecido')
                except:
                    self.username = "Desconhecido"
        except:
            self.username = "Desconhecido"
    
    # --- ABRE A URL DO PERFIL ---
    def navigate_to_profile(self):
        if not self.profile_url:
            raise ValueError("URL do perfil não foi definida")
        
        logger.info(f"🌐 Abrindo perfil: {self.profile_url}")
        self.browser.open_url(self.profile_url)
        
        print("\n⏳ Aguarde o navegador carregar a página (10 segundos)...")
        for i in range(10, 0, -1):
            print(f"   ⏱️  {i}s...", end='\r')
            time.sleep(1)
        print("   ✅ Pronto!                  ")
    
    # --- EXTRAI USER ID DA URL DO PERFIL ---
    def extract_profile_info(self) -> Dict:
        try:
            user_id = self._extract_user_id_from_url()
            
            logger.info(f"✅ Informações extraídas - User ID: {user_id}")
            
            return {
                "username": self.username or "Desconhecido",
                "user_id": user_id,
                "avatar_url": None,
                "profile_url": self.profile_url,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair informações do perfil: {e}")
            return {
                "username": self.username or "Desconhecido",
                "user_id": None,
                "avatar_url": None,
                "profile_url": self.profile_url,
                "timestamp": datetime.now().isoformat()
            }
    
    # --- EXTRAI USER_ID DA URL ---
    def _extract_user_id_from_url(self) -> Optional[int]:
        try:
            if not self.profile_url:
                return None
            
            url = self.profile_url
            parts = url.split('/')
            
            for i, part in enumerate(parts):
                if part == 'users' and i + 1 < len(parts):
                    user_id = int(parts[i + 1])
                    self.user_id = user_id
                    return user_id
            
            return None
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair user ID: {e}")
            return None
    
    # --- EXTRAI O COOKIE .ROBLOSECURITY ---
    def extract_roblosecurity_cookie(self) -> Optional[Dict]:
        try:
            logger.info(f"🍪 Procurando cookie .ROBLOSECURITY no {self.browser_type}...")
            
            cookie = self.browser.get_cookie(self.ROBLOSECURITY_COOKIE_NAME)
            
            if cookie:
                logger.info("✅ Cookie .ROBLOSECURITY encontrado!")
                return cookie
            else:
                logger.warning("⚠️ Cookie .ROBLOSECURITY não encontrado")
                logger.info("💡 Certifique-se de estar logado na conta do Roblox")
                return None
        
        except Exception as e:
            logger.error(f"❌ Erro ao extrair cookie: {e}")
            return None
    
    # --- EXTRAI APENAS O VALOR DO COOKIE ---
    def extract_cookie_value(self) -> Optional[str]:
        cookie = self.extract_roblosecurity_cookie()
        if cookie:
            return cookie.get('value')
        return None
    
    # --- SALVA COOKIE COM NOME DO USUÁRIO ---
    def save_cookie_with_username(self, username: str, cookie_value: str) -> bool:
        try:
            # Carrega cookies existentes
            cookies_data = self._load_saved_cookies()
            
            # Adiciona novo cookie
            cookies_data[username] = {
                "cookie": cookie_value,
                "saved_at": datetime.now().isoformat()
            }
            
            # Salva arquivo
            self.COOKIES_DATA_FILE.parent.mkdir(exist_ok=True)
            with open(self.COOKIES_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(cookies_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Cookie do usuário '{username}' salvo!")
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao salvar cookie: {e}")
            return False
    
    # --- CARREGA COOKIES SALVOS ---
    def _load_saved_cookies(self) -> Dict:
        try:
            if self.COOKIES_DATA_FILE.exists():
                with open(self.COOKIES_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Erro ao carregar cookies salvos: {e}")
        
        return {}
    
    # --- OBTÉM LISTA DE COOKIES SALVOS ---
    def get_saved_cookies(self) -> Dict[str, str]:
        cookies_data = self._load_saved_cookies()
        return {username: data.get('cookie', '') for username, data in cookies_data.items()}
    
    # --- ABRE URL COM COOKIE NO NAVEGADOR (INJEÇÃO AUTOMÁTICA) ---
    def login_with_cookie(self, cookie_value: str) -> bool:
        try:
            # Seleciona navegador
            self.select_browser()
            self.start()
            
            # Abre Roblox com injeção de cookie
            roblox_url = "https://www.roblox.com/"
            
            print("\n🔐 Injetando cookie automaticamente...")
            print("⏳ Aguarde (3-5 segundos)...")
            
            if self.browser.open_url_with_selenium(roblox_url, cookie_value):
                print_success("Login automático realizado com sucesso!")
                print_info("Você está logado no Roblox. O navegador permanecerá aberto.")
                logger.info("✅ Login com cookie concluído")
                return True
            else:
                print_error("Erro ao injetar cookie. Abrindo manualmente...")
                self.browser.open_url(roblox_url)
                
                print("\n⏳ Navegador aberto. Para logar manualmente:")
                print("1. Abra o Console (F12 ou Ctrl+Shift+I)")
                print("2. Vá para a aba 'Application' ou 'Storage'")
                print("3. Clique em 'Cookies' > 'https://www.roblox.com'")
                print("4. Procure por '.ROBLOSECURITY' e edite com o novo valor")
                print("5. Recarregue a página (F5)")
                
                input("\n➤ Pressione ENTER após completar...")
                logger.info("✅ Login manual concluído")
                return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao fazer login: {e}")
            print_error(f"Erro: {e}")
            return False
    
    # --- EXIBE COOKIES SALVOS ---
    def display_saved_cookies(self):
        cookies = self.get_saved_cookies()
        
        if not cookies:
            print("\n❌ Nenhum cookie salvo!")
            return
        
        print("\n" + "="*60)
        print("💾 COOKIES SALVOS")
        print("="*60)
        
        for idx, (username, cookie_value) in enumerate(cookies.items(), 1):
            print(f"\n{idx}. {username}")
            print(f"   Cookie: {cookie_value[:20]}...{cookie_value[-20:]}")
    
    # --- FECHA O NAVEGADOR ---
    def close(self):
        self.browser.close()
    
    # --- FECHA APENAS A ABA DO PERFIL ---
    def close_tab(self):
        return self.browser.close_current_tab()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
