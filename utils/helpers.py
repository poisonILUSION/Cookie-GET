"""Funções auxiliares para CookieGet"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

logger = logging.getLogger(__name__)


def setup_logging(log_file: Path, level=logging.INFO):
    """Configura o sistema de logging"""
    log_file.parent.mkdir(exist_ok=True)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Configura logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


def load_cookie_from_file(filepath: Path) -> Optional[str]:
    """Carrega um cookie salvo de um arquivo JSON"""
    try:
        if not filepath.exists():
            logger.warning(f"⚠️ Arquivo não encontrado: {filepath}")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cookie_value = data.get('cookie', {}).get('value')
            
            if cookie_value:
                logger.info(f"✅ Cookie carregado de: {filepath}")
                return cookie_value
            else:
                logger.warning("⚠️ Cookie não encontrado no arquivo")
                return None
    
    except json.JSONDecodeError:
        logger.error(f"❌ Erro ao decodificar JSON: {filepath}")
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao carregar cookie: {e}")
        return None


def load_profile_info_from_file(filepath: Path) -> Optional[Dict]:
    """Carrega informações do perfil de um arquivo JSON"""
    try:
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('profile_info')
    
    except Exception as e:
        logger.error(f"❌ Erro ao carregar informações do perfil: {e}")
        return None


def format_cookie_display(cookie_value: str, show_full=False) -> str:
    """Formata o cookie para exibição segura"""
    if not cookie_value:
        return "Nenhum cookie"
    
    if show_full:
        return cookie_value
    else:
        # Mostra apenas primeiros e últimos 10 caracteres
        if len(cookie_value) > 20:
            return f"{cookie_value[:10]}...{cookie_value[-10:]}"
        return cookie_value


def validate_roblox_url(url: str) -> bool:
    """Valida se é uma URL válida do Roblox"""
    if not isinstance(url, str):
        return False
    
    return url.startswith(("http://", "https://")) and "roblox.com" in url.lower()


def get_user_id_from_url(url: str) -> Optional[int]:
    """Extrai user ID de uma URL do Roblox"""
    try:
        parts = url.split('/')
        
        for i, part in enumerate(parts):
            if part == 'users' and i + 1 < len(parts):
                return int(parts[i + 1])
        
        return None
    except:
        return None


def print_success(message: str):
    """Imprime mensagem de sucesso"""
    print(f"\n✅ {message}\n")


def print_error(message: str):
    """Imprime mensagem de erro"""
    print(f"\n❌ {message}\n")


def print_info(message: str):
    """Imprime mensagem informativa"""
    print(f"\n💡 {message}\n")
