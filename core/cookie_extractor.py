# --- EXTRATOR DE COOKIES ROBLOX ---

import logging
import json
import time
import webbrowser
from datetime import datetime
from typing import Optional, Dict, List
from .browser import BrowserManager
from config.settings import ROBLOX_BASE_URL, ROBLOX_PROFILE_URL

logger = logging.getLogger(__name__)


class RobloxCookieExtractor:
    
    ROBLOSECURITY_COOKIE_NAME = ".ROBLOSECURITY"
    
    def __init__(self, timeout=30):
        self.browser = BrowserManager(timeout=timeout)
        self.profile_url = None
        self.username = None
        self.user_id = None
    
    # --- INICIA O NAVEGADOR ---
    def start(self):
        self.browser.start()
    
    # --- SOLICITA URL DO PERFIL DO ROBLOX ---
    def input_profile_url(self) -> str:
        print("\n" + "="*60)
        print("🍪 CookieGet - Extrator de Cookies Roblox")
        print("="*60)
        print("\n📖 Instruções:")
        print("1. Cole a URL do seu perfil Roblox (ex: https://www.roblox.com/users/123456/profile)")
        print("2. Faça login se necessário (o navegador abrirá automaticamente)")
        print("3. Aguarde a extração do cookie\n")
        
        while True:
            url = input("🔗 Digite a URL do seu perfil Roblox: ").strip()
            
            if url.startswith(("http://", "https://")):
                if "roblox.com" in url.lower():
                    self.profile_url = url
                    logger.info(f"✅ URL aceita: {url}")
                    return url
                else:
                    print("❌ URL deve ser do Roblox (roblox.com)")
            else:
                print("❌ URL deve começar com http:// ou https://")
    
    # --- ABRE A URL DO PERFIL NO FIREFOX ---
    def navigate_to_profile(self):
        if not self.profile_url:
            raise ValueError("URL do perfil não foi definida")
        
        logger.info(f"🌐 Abrindo perfil no Firefox: {self.profile_url}")
        
        webbrowser.open(self.profile_url)
        
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
                "username": "Desconhecido",
                "user_id": user_id,
                "avatar_url": None,
                "profile_url": self.profile_url,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair informações do perfil: {e}")
            return {
                "username": "Desconhecido",
                "user_id": None,
                "avatar_url": None,
                "profile_url": self.profile_url,
                "timestamp": datetime.now().isoformat()
            }
    
    
    # --- EXTRAI USER_ID DA URL ---
    def _extract_user_id_from_url(self) -> Optional[int]:
        try:
            url = self.profile_url
            parts = url.split('/')
            
            for i, part in enumerate(parts):
                if part == 'users' and i + 1 < len(parts):
                    user_id = int(parts[i + 1])
                    return user_id
            
            return None
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair user ID: {e}")
            return None
    
    # --- EXTRAI O COOKIE .ROBLOSECURITY DO FIREFOX ---
    def extract_roblosecurity_cookie(self) -> Optional[Dict]:
        try:
            logger.info("🍪 Procurando cookie .ROBLOSECURITY no Firefox...")
            
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
    
    # --- EXTRAI TODOS OS COOKIES ---
    def extract_all_cookies(self) -> List[Dict]:
        return self.browser.get_cookies()
    
    # --- SALVA O COOKIE EM ARQUIVO JSON ---
    def save_cookie_to_file(self, filepath: str, include_profile_info=True) -> bool:
        try:
            cookie = self.extract_roblosecurity_cookie()
            
            if not cookie:
                logger.error("❌ Não foi possível extrair o cookie para salvar")
                return False
            
            profile_info = self.extract_profile_info()
            
            data = {
                "cookie": cookie,
                "profile_info": profile_info if include_profile_info else None,
                "extracted_at": datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Cookie salvo em: {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao salvar cookie: {e}")
            return False
    
    # --- FECHA O FIREFOX COMPLETAMENTE ---
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
