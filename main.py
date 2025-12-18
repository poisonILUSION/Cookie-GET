# --- EXTRATOR DE COOKIES ROBLOX - GROOBIE ---

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import LOG_FILE
from core.cookie_extractor import RobloxCookieExtractor
from utils.helpers import (
    setup_logging, print_success, print_error, print_info,
    display_ascii_banner, clear_screen, copy_to_clipboard,
    paste_from_clipboard
)

logger = setup_logging(LOG_FILE, logging.INFO)


def menu_principal():
    """Menu principal do GROOBIE"""
    while True:
        clear_screen()
        display_ascii_banner()
        
        print("="*60)
        print("📋 MENU PRINCIPAL")
        print("="*60)
        print("\n1. Pegar cookie da conta")
        print("2. Logar com cookie da conta")
        print("3. Cookies salvos")
        print("4. Sair")
        
        choice = input("\n➤ Escolha uma opção (1-4): ").strip()
        
        if choice == '1':
            menu_pegar_cookie()
        elif choice == '2':
            menu_logar_cookie()
        elif choice == '3':
            menu_cookies_salvos()
        elif choice == '4':
            print("\n👋 Até logo!")
            logger.info("Aplicação encerrada")
            break
        else:
            print("❌ Opção inválida!")
            input("➤ Pressione ENTER para continuar...")


def menu_pegar_cookie():
    """Menu para pegar cookie de uma conta"""
    try:
        clear_screen()
        display_ascii_banner()
        
        # Seleciona navegador
        print("\n" + "="*60)
        print("🌐 SELECIONE O NAVEGADOR")
        print("="*60)
        print("\n1. Google Chrome")
        print("2. Firefox")
        print("3. Opera GX")
        print("4. Microsoft Edge")
        
        browser_choice = input("\n➤ Escolha (1-4): ").strip()
        
        browser_map = {'1': 'chrome', '2': 'firefox', '3': 'opera', '4': 'edge'}
        if browser_choice not in browser_map:
            print("❌ Navegador inválido!")
            input("➤ Pressione ENTER para voltar...")
            return
        
        browser_type = browser_map[browser_choice]
        
        # Cria extrator
        extrator = RobloxCookieExtractor(timeout=30, browser_type=browser_type)
        
        # Inicia navegador
        print(f"\n🌐 Iniciando {browser_type.capitalize()}...")
        extrator.start()
        
        # Solicita informações do perfil
        profile_url = extrator.input_profile_info()
        
        # Abre o perfil
        print(f"\n🔗 Acessando perfil...")
        extrator.navigate_to_profile()
        
        # Extrai informações
        print(f"\n📊 Extraindo informações...")
        profile_info = extrator.extract_profile_info()
        
        print(f"\n   👤 Usuário: {profile_info['username']}")
        if profile_info['user_id']:
            print(f"   🆔 ID: {profile_info['user_id']}")
        
        # Extrai cookie
        print(f"\n🍪 Extraindo cookie...")
        cookie = extrator.extract_roblosecurity_cookie()
        
        if cookie:
            print(f"   ✅ Cookie extraído com sucesso!")
            
            cookie_value = cookie.get('value', '')
            
            print("\n" + "="*60)
            print("🔑 VALOR DO COOKIE")
            print("="*60)
            print(f"\n{cookie_value[:50]}...")
            print(f"\n(Total: {len(cookie_value)} caracteres)")
            
            # Pergunta se quer copiar
            copy_choice = input("\n➤ Deseja copiar o cookie? (S/N): ").strip().lower()
            if copy_choice == 's':
                if copy_to_clipboard(cookie_value):
                    print_success("Cookie copiado para clipboard!")
                else:
                    print_error("Erro ao copiar para clipboard!")
            
            # Pergunta se quer salvar
            save_choice = input("➤ Deseja salvar o cookie? (S/N): ").strip().lower()
            if save_choice == 's':
                username = input("➤ Digite o nome de usuário para salvar: ").strip()
                if username:
                    if extrator.save_cookie_with_username(username, cookie_value):
                        print_success(f"Cookie do usuário '{username}' salvo!")
                    else:
                        print_error("Erro ao salvar cookie!")
        else:
            print_error("Não foi possível extrair o cookie!")
            print_info("Certifique-se de estar logado na conta do Roblox")
        
        input("\n➤ Pressione ENTER para voltar ao menu...")
        
    except KeyboardInterrupt:
        print_error("Processo cancelado pelo usuário")
        logger.info("Pegar cookie - Processo cancelado")
    except Exception as e:
        print_error(f"Erro durante execução: {e}")
        logger.error(f"Erro em menu_pegar_cookie: {e}", exc_info=True)


def menu_logar_cookie():
    """Menu para logar com cookie"""
    try:
        while True:
            clear_screen()
            display_ascii_banner()
            
            print("="*60)
            print("🔑 LOGAR COM COOKIE")
            print("="*60)
            print("\n1. Logar com cookie salvo")
            print("2. Logar com outro cookie")
            print("3. Voltar")
            
            choice = input("\n➤ Escolha (1-3): ").strip()
            
            if choice == '1':
                logar_com_cookie_salvo()
            elif choice == '2':
                logar_com_outro_cookie()
            elif choice == '3':
                break
            else:
                print("❌ Opção inválida!")
                input("➤ Pressione ENTER para continuar...")
    
    except KeyboardInterrupt:
        print_error("Processo cancelado")
    except Exception as e:
        print_error(f"Erro: {e}")
        logger.error(f"Erro em menu_logar_cookie: {e}", exc_info=True)


def logar_com_cookie_salvo():
    """Loga com um cookie previamente salvo"""
    try:
        clear_screen()
        display_ascii_banner()
        
        extrator = RobloxCookieExtractor(timeout=30)
        cookies = extrator.get_saved_cookies()
        
        if not cookies:
            print_error("Nenhum cookie salvo!")
            input("➤ Pressione ENTER para voltar...")
            return
        
        print("="*60)
        print("💾 COOKIES SALVOS")
        print("="*60)
        
        cookie_list = list(cookies.items())
        for idx, (username, _) in enumerate(cookie_list, 1):
            print(f"\n{idx}. {username}")
        
        print(f"\n{len(cookie_list) + 1}. Voltar")
        
        choice = input("\n➤ Escolha um cookie (1-" + str(len(cookie_list) + 1) + "): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if choice_idx == len(cookie_list):
                return
            
            if 0 <= choice_idx < len(cookie_list):
                username, cookie_value = cookie_list[choice_idx]
                print(f"\n🔐 Abrindo navegador para logar como {username}...")
                extrator.login_with_cookie(cookie_value)
            else:
                print("❌ Escolha inválida!")
        except ValueError:
            print("❌ Digite um número válido!")
        
        input("\n➤ Pressione ENTER para voltar...")
    
    except Exception as e:
        print_error(f"Erro: {e}")
        logger.error(f"Erro em logar_com_cookie_salvo: {e}", exc_info=True)


def logar_com_outro_cookie():
    """Loga com um cookie novo (colar)"""
    try:
        clear_screen()
        display_ascii_banner()
        
        print("="*60)
        print("📝 LOGAR COM OUTRO COOKIE")
        print("="*60)
        
        print("\n1. Colar cookie manualmente")
        print("2. Colar do clipboard")
        
        paste_choice = input("\n➤ Escolha (1-2): ").strip()
        
        if paste_choice == '1':
            cookie_value = input("\n🍪 Cole o cookie: ").strip()
        elif paste_choice == '2':
            cookie_value = paste_from_clipboard()
            if not cookie_value:
                print_error("Não foi possível colar do clipboard!")
                input("➤ Pressione ENTER para voltar...")
                return
            print(f"✅ Cookie colado: {cookie_value[:30]}...")
        else:
            print("❌ Opção inválida!")
            input("➤ Pressione ENTER para voltar...")
            return
        
        if cookie_value and len(cookie_value) > 10:
            extrator = RobloxCookieExtractor(timeout=30)
            print("\n🔐 Preparando login automático...")
            extrator.login_with_cookie(cookie_value)
        else:
            print_error("Cookie inválido!")
        
        input("\n➤ Pressione ENTER para voltar...")
    
    except KeyboardInterrupt:
        print_error("Processo cancelado")
    except Exception as e:
        print_error(f"Erro: {e}")
        logger.error(f"Erro em logar_com_outro_cookie: {e}", exc_info=True)


def menu_cookies_salvos():
    """Menu para visualizar cookies salvos"""
    try:
        clear_screen()
        display_ascii_banner()
        
        extrator = RobloxCookieExtractor(timeout=30)
        cookies = extrator.get_saved_cookies()
        
        if not cookies:
            print("\n❌ Nenhum cookie salvo!")
            input("➤ Pressione ENTER para voltar...")
            return
        
        print("="*60)
        print("💾 COOKIES SALVOS")
        print("="*60)
        
        cookie_list = list(cookies.items())
        for idx, (username, cookie_value) in enumerate(cookie_list, 1):
            print(f"\n{idx}. {username}")
            print(f"   📋 Copiar cookie")
        
        choice = input("\n➤ Escolha um cookie para copiar (1-" + str(len(cookie_list)) + "): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(cookie_list):
                username, cookie_value = cookie_list[choice_idx]
                if copy_to_clipboard(cookie_value):
                    print_success(f"Cookie de '{username}' copiado!")
                else:
                    print_error("Erro ao copiar!")
            else:
                print("❌ Escolha inválida!")
        except ValueError:
            print("❌ Digite um número válido!")
        
        input("\n➤ Pressione ENTER para voltar...")
    
    except Exception as e:
        print_error(f"Erro: {e}")
        logger.error(f"Erro em menu_cookies_salvos: {e}", exc_info=True)


def main():
    """Função principal"""
    try:
        logger.info("Aplicação iniciada")
        menu_principal()
    except KeyboardInterrupt:
        print_error("Aplicação encerrada pelo usuário")
        logger.info("Aplicação encerrada pelo usuário")
    except Exception as e:
        print_error(f"Erro fatal: {e}")
        logger.error(f"Erro fatal: {e}", exc_info=True)


if __name__ == "__main__":
    main()
