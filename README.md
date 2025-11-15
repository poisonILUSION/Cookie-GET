# 🍪 Cookie-GET

> **Uma ferramenta poderosa e automatizada para extrair cookies de contas Roblox com segurança e eficiência.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat-square)

---

## 📋 Sobre o Projeto

**Cookie-GET** é uma solução automatizada desenvolvida em Python para extrair cookies de autenticação de contas Roblox. O projeto utiliza Selenium para automação de navegador e oferece uma interface simples e intuitiva.

### ✨ Funcionalidades

- 🤖 **Automação Completa** - Extrai cookies automaticamente usando Selenium
- 🔒 **Seguro** - Processa dados localmente, sem enviar para servidores externos
- 📝 **Logging Detalhado** - Rastreia todas as operações com logs estruturados
- 💾 **Armazenamento JSON** - Salva cookies em formato organizado e reutilizável
- 🌐 **Suporte a Firefox** - Integrado com WebDriver Manager para fácil configuração
- ⚡ **Rápido e Eficiente** - Processamento otimizado com timeouts configuráveis

---

## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- Firefox instalado no sistema
- pip (gerenciador de pacotes Python)

### 📦 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/poisonILUSION/Cookie-GET.git
cd Cookie-GET
```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
```bash
python -m venv venv
venv\Scripts\activate  # No Windows
source venv/bin/activate  # No macOS/Linux
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

---

## 💻 Uso

### Execução Básica

```bash
python main.py
```

### Com Input Direto

```bash
echo "https://www.roblox.com/users/2426621935/profile" | python main.py
```

### Fluxo de Operação

1. O programa se conecta ao Firefox via Selenium
2. Navega para o perfil Roblox fornecido
3. Aguarda autenticação manual (se necessário)
4. Extrai os cookies de autenticação
5. Salva os dados em `data/roblox_cookies.json`
6. Exibe informações de sucesso ou erro

---

## 📁 Estrutura do Projeto

```
CookieGet/
├── main.py                 # Arquivo principal da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── config/
│   ├── __init__.py
│   └── settings.py        # Configurações e caminhos
├── core/
│   ├── __init__.py
│   ├── cookie_extractor.py # Lógica principal de extração
│   └── browser.py         # Gerenciamento do navegador
├── data/
│   └── roblox_cookies.json # Cookies armazenados (gerado)
├── logs/                  # Arquivos de log (gerado)
└── utils/
    ├── __init__.py
    └── helpers.py         # Funções auxiliares
```

---

## 🔧 Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `selenium` | >=4.10.0 | Automação de navegador |
| `requests` | >=2.31.0 | Requisições HTTP |
| `webdriver-manager` | >=3.9.1 | Gerenciador de drivers |

---

## ⚙️ Configuração

Edite `config/settings.py` para personalizar:

- 🗂️ Caminhos de arquivo
- 📝 Nível de logging
- ⏱️ Timeouts de conexão
- 🔍 Seletores CSS/XPath

---

## 📊 Exemplo de Saída

```
============================================================
🍪 CookieGet - Extrator de Cookies Roblox
============================================================

🌐 Conectando ao Firefox...
✅ Navegador iniciado com sucesso

📍 Insira a URL do perfil Roblox: https://www.roblox.com/users/2426621935/profile

⏳ Extraindo cookies...
✅ Cookies extraídos com sucesso!
💾 Salvo em: data/roblox_cookies.json
```

---

## 🛡️ Segurança

- ✅ Sem envio de dados para servidores externos
- ✅ Processamento local completo
- ✅ Logs estruturados para auditoria
- ✅ Tratamento de exceções robusto

> ⚠️ **Aviso Legal:** Use esta ferramenta apenas com contas que você possui ou com consentimento explícito do proprietário. O uso não autorizado pode violar os Termos de Serviço do Roblox.

---

## 📝 Logging

Todos os eventos são registrados em:
- 📄 `logs/app.log` - Arquivo de log principal
- 🖥️ Console - Saída em tempo real com cores

**Níveis de Log:**
- `DEBUG` - Informações detalhadas
- `INFO` - Informações gerais
- `WARNING` - Avisos importantes
- `ERROR` - Erros e exceções

---

## 🐛 Troubleshooting

### Erro: "Firefox não encontrado"
```bash
# Instale o Firefox ou configure o caminho em settings.py
```

### Erro: "WebDriver não compatível"
```bash
pip install --upgrade webdriver-manager
```

### Timeout na extração
- Aumente o valor de `timeout` em `main.py`
- Verifique sua conexão de internet
- Confirme que o site Roblox está acessível

---

## 📈 Roadmap

- [ ] Suporte para Chrome/Chromium
- [ ] Interface gráfica (GUI)
- [ ] Extração em lote (múltiplas contas)
- [ ] Integração com Discord Bot
- [ ] Dashboard web para gerenciamento

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📜 Licença

Este projeto está sob a licença **MIT**. 

---

## 👨‍💻 Autor

Desenvolvido por **poisonILUSION** 🚀

---

## 📞 Suporte

Para dúvidas, problemas ou sugestões:
- 📧 Abra uma [Issue](https://github.com/poisonILUSION/Cookie-GET/issues)
- 💬 Participe das [Discussions](https://github.com/poisonILUSION/Cookie-GET/discussions)

---

## 🙏 Agradecimentos

- [Selenium](https://www.selenium.dev/) - Automação web
- [WebDriver Manager](https://github.com/SergeyPirogov/webdrivermanager) - Gerenciamento de drivers
- [Python](https://www.python.org/) - Linguagem incrível

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**
