# --- EXTRATOR DE COOKIES ROBLOX ---

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import LOG_FILE, COOKIES_FILE
from core.cookie_extractor import RobloxCookieExtractor
from utils.helpers import setup_logging, print_success, print_error, print_info

logger = setup_logging(LOG_FILE, logging.INFO)


def main():
    try:
        print("\n" + "="*60)
        print("🍪 CookieGet - Extrator de Cookies Roblox")
        print("="*60)
        
        # --- CRIA E INICIA O EXTRATOR ---
        extrator = RobloxCookieExtractor(timeout=30)
        
        print("\n🌐 Conectando ao Firefox...")
        extrator.start()
        
        # --- SOLICITA URL DO PERFIL ---
        profile_url = extrator.input_profile_url()
        
        # --- ABRE A URL DO PERFIL ---
        print(f"\n🔗 Acessando perfil...")
        extrator.navigate_to_profile()
        
        # --- EXTRAI INFORMAÇÕES DO PERFIL ---
        print(f"\n📊 Extraindo informações do perfil...")
        profile_info = extrator.extract_profile_info()
        
        print(f"   👤 Usuário: {profile_info['username']}")
        if profile_info['user_id']:
            print(f"   🆔 ID: {profile_info['user_id']}")
        
        # --- EXTRAI O COOKIE .ROBLOSECURITY ---
        print(f"\n🍪 Extraindo cookie .ROBLOSECURITY...")
        cookie = extrator.extract_roblosecurity_cookie()
        
        if cookie:
            print(f"   ✅ Cookie extraído com sucesso!")
            
            # --- SALVA O COOKIE EM ARQUIVO ---
            print(f"\n💾 Salvando cookie em arquivo...")
            if extrator.save_cookie_to_file(str(COOKIES_FILE)):
                print_success(f"Cookie salvo em: {COOKIES_FILE}")
                
                cookie_value = cookie.get('value', '')
                print("\n" + "="*60)
                print("🔑 Valor do Cookie:")
                print("="*60)
                print(f"\n{cookie_value}\n")
                print("="*60)
                
                print_info("Este cookie pode ser usado no Discord Bot para monitorar a conta!")
        else:
            print_error("Não foi possível extrair o cookie. Certifique-se de estar logado!")
        
        # --- FECHA APENAS A ABA DO PERFIL ---
        print("\n📑 Fechando aba do perfil...")
        extrator.close_tab()
        print("✅ Aba fechada! Firefox ainda está aberto para você usar.")
        
    except KeyboardInterrupt:
        print_error("Processo cancelado pelo usuário")
        logger.info("Processo cancelado pelo usuário")
    except Exception as e:
        print_error(f"Erro durante execução: {e}")
        logger.error(f"Erro: {e}", exc_info=True)
    finally:
        pass


if __name__ == "__main__":
    main()
