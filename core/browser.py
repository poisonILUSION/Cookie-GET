# --- GERENCIADOR DE NAVEGADORES ---

import logging
import subprocess
import time
import sqlite3
from pathlib import Path
import os
import json
import webbrowser

logger = logging.getLogger(__name__)


class BrowserManager:
    
    BROWSER_TYPES = {
        'firefox': 'firefox.exe',
        'chrome': 'chrome.exe',
        'edge': 'msedge.exe',
        'opera': 'opera.exe'
    }
    
    def __init__(self, timeout=30, browser_type='firefox'):
        self.timeout = timeout
        self.browser_type = browser_type.lower()
        self.firefox_profile_path = None
        self.profile_path = None
    
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
    
    # --- ABRE NAVEGADOR SE NÃO ESTIVER RODANDO ---
    def start(self):
        try:
            if self.browser_type == 'firefox':
                self._start_firefox()
            elif self.browser_type == 'chrome':
                self._start_chrome()
            elif self.browser_type == 'edge':
                self._start_edge()
            elif self.browser_type == 'opera':
                self._start_opera()
            else:
                logger.error(f"❌ Navegador não suportado: {self.browser_type}")
                raise ValueError(f"Navegador não suportado: {self.browser_type}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar navegador: {e}")
            raise
    
    def _start_firefox(self):
        if not self._is_browser_running('firefox.exe'):
            logger.info("🌐 Abrindo Firefox...")
            subprocess.Popen(["firefox"])
            time.sleep(5)
            logger.info("✅ Firefox aberto com sucesso")
        else:
            logger.info("✅ Firefox já está em execução")
        
        if not self.firefox_profile_path:
            self._get_firefox_profile_path()
    
    def _start_chrome(self):
        if not self._is_browser_running('chrome.exe'):
            logger.info("🌐 Abrindo Google Chrome...")
            subprocess.Popen(["chrome"])
            time.sleep(5)
            logger.info("✅ Chrome aberto com sucesso")
        else:
            logger.info("✅ Chrome já está em execução")
    
    def _start_edge(self):
        if not self._is_browser_running('msedge.exe'):
            logger.info("🌐 Abrindo Microsoft Edge...")
            subprocess.Popen(["msedge"])
            time.sleep(5)
            logger.info("✅ Edge aberto com sucesso")
        else:
            logger.info("✅ Edge já está em execução")
    
    def _start_opera(self):
        if not self._is_browser_running('opera.exe'):
            logger.info("🌐 Abrindo Opera GX...")
            subprocess.Popen(["opera"])
            time.sleep(5)
            logger.info("✅ Opera GX aberto com sucesso")
        else:
            logger.info("✅ Opera GX já está em execução")
    
    # --- VERIFICA SE UM NAVEGADOR ESTÁ RODANDO ---
    def _is_browser_running(self, browser_name):
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            return browser_name.lower() in result.stdout.lower()
        except:
            return False
    
    # --- EXTRAI COOKIES DO BANCO DE DADOS DO FIREFOX ---
    def get_cookies(self):
        if self.browser_type != 'firefox':
            logger.warning("⚠️ Extração de cookies atualmente suportada apenas em Firefox")
            return []
        
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
    
    # --- ABRE URL NO NAVEGADOR ---
    def open_url(self, url):
        try:
            webbrowser.open(url)
            logger.info(f"🔗 Abrindo URL: {url}")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao abrir URL: {e}")
            return False
    
    # --- FECHA O NAVEGADOR COMPLETAMENTE ---
    def close(self):
        try:
            browser_exe = self.BROWSER_TYPES.get(self.browser_type, 'firefox.exe')
            subprocess.run(["taskkill", "/IM", browser_exe, "/F"], capture_output=True)
            logger.info(f"✅ {self.browser_type.capitalize()} fechado")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao fechar navegador: {e}")
    
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
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
