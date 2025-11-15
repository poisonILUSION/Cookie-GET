# --- GERENCIADOR DO FIREFOX ---

import logging
import subprocess
import time
import sqlite3
from pathlib import Path
import os
import json

logger = logging.getLogger(__name__)


class BrowserManager:
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.firefox_profile_path = None
    
    # --- ENCONTRA O PERFIL DO FIREFOX NO WINDOWS ---
    def _get_firefox_profile_path(self):
        if os.name == 'nt':
            appdata = os.getenv('APPDATA')
            if appdata:
                firefox_profile_dir = Path(appdata) / 'Mozilla' / 'Firefox' / 'Profiles'
                if firefox_profile_dir.exists():
                    profiles_order = ['default-release', 'default']
                    
                    for profile_name in profiles_order:
                        profile_path = firefox_profile_dir / f"{profile_name}"
                        if (profile_path / 'cookies.sqlite').exists():
                            self.firefox_profile_path = str(profile_path)
                            logger.info(f"✅ Perfil Firefox encontrado: {profile_path}")
                            return str(profile_path)
                    
                    for profile in firefox_profile_dir.glob('*.default*'):
                        if (profile / 'cookies.sqlite').exists():
                            self.firefox_profile_path = str(profile)
                            logger.info(f"✅ Perfil Firefox encontrado: {profile}")
                            return str(profile)
        
        return None
    
    # --- ABRE FIREFOX SE NÃO ESTIVER RODANDO ---
    def start(self):
        try:
            if not self._is_firefox_running():
                logger.info("🌐 Abrindo Firefox...")
                subprocess.Popen(["firefox"])
                time.sleep(5)
                logger.info("✅ Firefox aberto com sucesso")
            else:
                logger.info("✅ Firefox já está em execução")
            
            if not self.firefox_profile_path:
                self._get_firefox_profile_path()
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar Firefox: {e}")
            raise
    
    # --- VERIFICA SE FIREFOX ESTÁ RODANDO ---
    def _is_firefox_running(self):
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            return "firefox.exe" in result.stdout.lower()
        except:
            return False
    
    # --- EXTRAI COOKIES DO BANCO DE DADOS DO FIREFOX ---
    def get_cookies(self):
        if not self.firefox_profile_path:
            self._get_firefox_profile_path()
        
        if not self.firefox_profile_path:
            logger.error("❌ Não foi possível encontrar o perfil do Firefox")
            return []
        
        try:
            cookies_db = Path(self.firefox_profile_path) / 'cookies.sqlite'
            
            if not cookies_db.exists():
                logger.warning(f"⚠️ Arquivo de cookies não encontrado: {cookies_db}")
                return []
            
            import tempfile
            import shutil
            
            # --- CRIA CÓPIA TEMPORÁRIA PARA EVITAR LOCK DO ARQUIVO ---
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite')
            temp_db.close()
            shutil.copy(cookies_db, temp_db.name)
            
            try:
                conn = sqlite3.connect(temp_db.name)
                cursor = conn.cursor()
                
                # --- CONSULTA COOKIES DO ROBLOX NO BANCO ---
                cursor.execute('''
                    SELECT name, value, host, path, expiry, isSecure, isHttpOnly
                    FROM moz_cookies
                    WHERE host LIKE '%roblox.com%'
                ''')
                
                cookies = []
                for row in cursor.fetchall():
                    cookies.append({
                        'name': row[0],
                        'value': row[1],
                        'domain': row[2],
                        'path': row[3],
                        'expiry': row[4],
                        'secure': bool(row[5]),
                        'httpOnly': bool(row[6])
                    })
                
                conn.close()
                logger.info(f"✅ {len(cookies)} cookie(s) extraído(s) do Firefox")
                return cookies
            
            finally:
                try:
                    os.unlink(temp_db.name)
                except:
                    pass
        
        except Exception as e:
            logger.error(f"❌ Erro ao extrair cookies: {e}")
            return []
    
    # --- OBTÉM UM COOKIE ESPECÍFICO ---
    def get_cookie(self, name):
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie['name'] == name:
                logger.info(f"🍪 Cookie encontrado: {name}")
                return cookie
        
        logger.warning(f"⚠️ Cookie não encontrado: {name}")
        return None
    
    # --- FECHA O FIREFOX COMPLETAMENTE ---
    def close(self):
        try:
            subprocess.run(["taskkill", "/IM", "firefox.exe", "/F"], capture_output=True)
            logger.info("✅ Firefox fechado")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao fechar Firefox: {e}")
    
    # --- FECHA APENAS A ABA ATUAL COM CTRL+W ---
    def close_current_tab(self):
        try:
            import pyautogui
            
            logger.info("📑 Fechando aba atual...")
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(1)
            logger.info("✅ Aba fechada com sucesso")
            return True
        except ImportError:
            logger.warning("⚠️ pyautogui não instalado. Use: pip install pyautogui")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Erro ao fechar aba: {e}")
            return False
    
    def get_url(self, url):
        try:
            subprocess.run(
                ["powershell", "-Command", 
                 f"(New-Object -COM 'Shell.Application').Open('{url}')"],
                capture_output=True
            )
            logger.info(f"🔗 Abrindo URL: {url}")
            time.sleep(2)
        except Exception as e:
            logger.error(f"❌ Erro ao abrir URL: {e}")
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
