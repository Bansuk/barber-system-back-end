# Barber System 💈

Um sistema completo de gestão para barbearias desenvolvido com Flask, permitindo o gerenciamento eficiente de clientes, funcionários, serviços e agendamentos através de uma API RESTful moderna e bem documentada.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
  - [Arquitetura](#arquitetura)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Integração com NumVerify](#-integração-com-numverify)
  - [O que é NumVerify?](#o-que-é-numverify)
  - [Como Obter uma Chave API](#como-obter-uma-chave-api)
  - [Planos Disponíveis](#planos-disponíveis)
  - [Licença de Uso](#licença-de-uso)
  - [Endpoints que Utilizam o NumVerify](#endpoints-que-utilizam-o-numverify)
  - [Configuração](#configuração)
  - [Comportamento da Validação](#comportamento-da-validação)
  - [Exemplo de Resposta da API](#exemplo-de-resposta-da-api)
- [Pré-requisitos](#-pré-requisitos)
  - [Para Execução Local](#para-execução-local)
  - [Para Execução com Docker](#para-execução-com-docker)
- [Instalação e Configuração](#-instalação-e-configuração)
  - [Execução Local](#execução-local)
  - [Execução com Docker](#execução-com-docker)
- [Uso](#-uso)
  - [Acessando a Documentação Interativa](#acessando-a-documentação-interativa)
  - [Exemplo de Requisições](#exemplo-de-requisições)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação da API](#-documentação-da-api)
  - [Principais Endpoints](#principais-endpoints)
- [Contato](#-contato)

## 🎯 Sobre o Projeto

O **Barber System** é uma solução backend robusta para gerenciar todos os aspectos operacionais de uma barbearia. O sistema oferece uma API REST completa com validações, documentação automática via OpenAPI/Swagger, e integração com serviços externos para validação de dados.

### Arquitetura

O projeto segue uma arquitetura em camadas bem definida:
- **Routes**: Endpoints da API
- **Business**: Lógica de negócio
- **Repositories**: Acesso aos dados
- **Validations**: Validação de entrada
- **Schemas**: Serialização/deserialização com Marshmallow
- **Models**: Modelos de dados SQLAlchemy

## ✨ Funcionalidades

- **👥 Gestão de Funcionários**: Cadastro completo, listagem e gerenciamento de profissionais da barbearia
- **📋 Gerenciamento de Clientes**: Registro e organização de clientes com validação de dados
- **✂️ Controle de Serviços**: Definição, precificação e listagem dos serviços oferecidos
- **📅 Sistema de Agendamentos**: Marcação e visualização de horários disponíveis
- **📱 Validação de Telefone**: Integração com API externa para validação de números
- **📖 Documentação Automática**: Interface Swagger UI para exploração da API

## 🛠️ Tecnologias Utilizadas

[![Python](https://img.shields.io/badge/python-3.10+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Flask](https://img.shields.io/badge/flask-3.1.0-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**Principais Dependências:**
- **Flask 3.1.0**: Framework web minimalista e poderoso
- **Flask-Smorest**: Extensão para criar APIs REST com OpenAPI
- **Flask-SQLAlchemy**: ORM para gerenciamento de banco de dados
- **Marshmallow**: Validação e serialização de objetos
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **Flask-CORS**: Suporte a Cross-Origin Resource Sharing

## 📱 Integração com NumVerify

O sistema utiliza a API do **NumVerify** para validação de números de telefone em tempo real, garantindo que apenas números válidos sejam cadastrados no sistema.

### O que é NumVerify?

[NumVerify](https://numverify.com/) é um serviço de validação de números de telefone que fornece:
- ✅ Validação de formato de números telefônicos internacionais
- 🌍 Identificação de país e operadora
- 📍 Detecção de tipo de linha (móvel, fixo, VoIP)
- 🔍 Verificação de números válidos e ativos

### Como Obter uma Chave API

1. **Acesse o site**: [https://numverify.com/](https://numverify.com/)

2. **Crie uma conta gratuita**:
   - Clique em "Get Free API Key" ou "Sign Up Free"
   - Preencha o formulário de registro
   - Confirme seu e-mail

3. **Acesse seu Dashboard**:
   - Após o login, você verá sua `API Key` no painel
   - Copie a chave para usar no arquivo `.env`

### Planos Disponíveis

| Plano | Requisições/mês | Preço | Ideal para |
|-------|----------------|-------|------------|
| **Free** | 100 | Gratuito | Desenvolvimento e testes |
| **Basic** | 5.000 | $9.99/mês | Pequenos projetos |
| **Professional** | 50.000 | $39.99/mês | Aplicações em produção |
| **Enterprise** | Personalizado | Sob consulta | Grande volume |

> **💡 Nota**: O plano gratuito é suficiente para desenvolvimento e testes. Para produção, considere os planos pagos.

### Licença de Uso

- **Plano Gratuito**: Apenas para uso pessoal, desenvolvimento e testes
- **Planos Pagos**: Uso comercial permitido
- Consulte os [Termos de Serviço](https://numverify.com/terms) para detalhes completos

### Endpoints que Utilizam o NumVerify

O serviço de validação de telefone é utilizado automaticamente nos seguintes endpoints:

#### 👥 Clientes
- **`POST /customer`**: Valida o número de telefone ao criar um novo cliente
- **`PATCH /customer/<customer_id>`**: Valida o número se o campo `phone_number` for atualizado

#### 👔 Funcionários
- **`POST /employee`**: Valida o número de telefone ao criar um novo funcionário
- **`PATCH /employee/<employee_id>`**: Valida o número se o campo `phone_number` for atualizado

### Configuração

Configure sua chave API no arquivo `.env`:

```env
API_KEY=sua_chave_numverify_aqui
URL=https://apilayer.net/api/validate
```

### Comportamento da Validação

- ✅ **Número válido**: O cadastro/atualização prossegue normalmente
- ❌ **Número inválido**: Retorna erro `422 Unprocessable Entity` com mensagem descritiva
- ⚠️ **API indisponível**: Se a API estiver fora do ar ou a chave for inválida, o sistema registrará um aviso mas permitirá o cadastro

### Exemplo de Resposta da API

Quando um número é validado, a API NumVerify retorna informações detalhadas:

```json
{
  "valid": true,
  "number": "5511999999999",
  "local_format": "(11) 99999-9999",
  "international_format": "+55 11 99999-9999",
  "country_prefix": "+55",
  "country_code": "BR",
  "country_name": "Brazil",
  "location": "São Paulo",
  "carrier": "Claro",
  "line_type": "mobile"
}
```

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

### Para Execução Local

- **Python**: versão 3.10 ou superior
  ```bash
  python --version  # ou python3 --version
  ```

- **pip**: gerenciador de pacotes Python (geralmente incluído com Python)
  ```bash
  pip --version  # ou pip3 --version
  ```

- **Git**: para clonar o repositório
  ```bash
  git --version
  ```

### Para Execução com Docker

- **Docker**: versão 20.10 ou superior
  ```bash
  docker --version
  ```

- **Docker Compose**: versão 2.0 ou superior
  ```bash
  docker-compose --version
  ```

## 🚀 Instalação e Configuração

### Execução Local

#### 1. Clone o Repositório

```bash
git clone https://github.com/Bansuk/barber-system-back-end.git
cd barber-system-back-end
```

#### 2. Configure as Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configuração. Você precisa criar um arquivo `.env` baseado no arquivo de exemplo fornecido.

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

Edite o arquivo `.env` e configure as seguintes variáveis:

```env
# API Key para validação de números de telefone (numverify)
API_KEY=sua_chave_api_aqui

# URL da API de validação
URL=https://apilayer.net/api/validate

# Formatação de resposta JSON (opcional)
PRETTIFY_JSON_RESPONSE=1
```

> **⚠️ Importante:** 
> - Sem a chave API, a validação de telefone não funcionará corretamente

#### 3. Crie um Ambiente Virtual (Recomendado)

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
# No Linux/macOS:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

#### 4. Instale as Dependências

Com o ambiente virtual ativado, instale todas as dependências necessárias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Execute o Projeto

Inicie o servidor de desenvolvimento:

```bash
python3 app.py
```

Ou usando o comando Flask:

```bash
flask run
```

A aplicação estará disponível em: **http://localhost:5000**

Para desativar o ambiente virtual quando terminar:
```bash
deactivate
```

---

### Execução com Docker

O Docker permite executar o projeto de forma isolada e consistente, sem necessidade de instalar Python e dependências localmente.

#### 1. Clone o Repositório

```bash
git clone https://github.com/Bansuk/barber-system-back-end.git
cd barber-system-back-end
```

#### 2. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

Edite o arquivo `.env` conforme descrito na seção de [Execução Local](#2-configure-as-variáveis-de-ambiente).

> **💡 Dica:** O Docker Compose carregará automaticamente as variáveis do arquivo `.env`

#### 3. Construa e Execute com Docker Compose

```bash
# Construir a imagem e iniciar o container
docker-compose up --build
```

A aplicação estará disponível em: **http://localhost:5000**

## 📖 Uso

### Acessando a Documentação Interativa

Com o projeto em execução (local ou Docker), acesse a documentação interativa Swagger UI:

**🔗 http://localhost:5000/api/docs/swagger-ui**

A interface Swagger permite:
- 📚 Visualizar todos os endpoints disponíveis
- 🧪 Testar as requisições diretamente pelo navegador
- 📝 Ver schemas de requisição e resposta
- ✅ Validar respostas e códigos de status

### Exemplo de Requisições

#### Criar um Cliente

```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "phone": "+5511999999999",
    "email": "joao@example.com"
  }'
```

#### Listar Serviços

```bash
curl http://localhost:5000/api/services
```

#### Criar um Agendamento

```bash
curl -X POST http://localhost:5000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "employee_id": 1,
    "service_id": 1,
    "appointment_date": "2024-12-10T10:00:00"
  }'
```

## 📁 Estrutura do Projeto

```
barber-system-back-end/
├── app.py                      # Ponto de entrada da aplicação
├── settings.py                 # Configurações e variáveis de ambiente
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Configuração Docker
├── docker-compose.yml          # Orquestração de containers
├── .env.example                # Exemplo de variáveis de ambiente
├── README.md                   # Este arquivo
│
├── business/                   # Camada de lógica de negócio
│   ├── appointment_business.py
│   ├── customer_business.py
│   ├── employee_business.py
│   └── service_business.py
│
├── database/                   # Configuração de banco de dados
│   ├── config.py
│   ├── db_setup.py
│   └── models/                 # Modelos SQLAlchemy
│       ├── appointment.py
│       ├── customer.py
│       ├── employee.py
│       ├── service.py
│       └── ...
│
├── repositories/               # Camada de acesso a dados
│   ├── appointment_repository.py
│   ├── customer_repository.py
│   ├── employee_repository.py
│   └── service_repository.py
│
├── routes/                     # Definição de rotas/endpoints
│   ├── appointment_routes.py
│   ├── customer_routes.py
│   ├── employee_routes.py
│   ├── service_routes.py
│   └── docs/                   # Documentação OpenAPI
│
├── schemas/                    # Schemas Marshmallow
│   ├── appointment_schema.py
│   ├── customer_schema.py
│   ├── employee_schema.py
│   └── service_schema.py
│
├── services/                   # Integrações externas
│   └── numverify.py            # Validação de telefone
│
└── validations/                # Validações de negócio
    ├── appointment_validation.py
    ├── customer_validation.py
    ├── employee_validation.py
    └── service_validation.py
```

## 📖 Documentação da API

A documentação completa da API está disponível através do Swagger UI quando o servidor está em execução:

**🔗 http://localhost:5000/api/docs/swagger-ui**

### Principais Endpoints

#### 👥 Clientes (Customers)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/customers` | Lista todos os clientes |
| `POST` | `/customer` | Cria um novo cliente |
| `PATCH` | `/customer/<customer_id>` | Atualiza parcialmente um cliente |
| `DELETE` | `/customer/<customer_id>` | Remove um cliente |

#### 👔 Funcionários (Employees)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/employees` | Lista todos os funcionários |
| `POST` | `/employee` | Cria um novo funcionário |
| `PATCH` | `/employee/<employee_id>` | Atualiza parcialmente um funcionário |
| `DELETE` | `/employee/<employee_id>` | Remove um funcionário |

#### ✂️ Serviços (Services)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/services` | Lista todos os serviços |
| `POST` | `/service` | Cria um novo serviço |
| `PATCH` | `/service/<service_id>` | Atualiza parcialmente um serviço |
| `DELETE` | `/service/<service_id>` | Remove um serviço |

#### 📅 Agendamentos (Appointments)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/appointments` | Lista todos os agendamentos |
| `POST` | `/appointment` | Cria um novo agendamento |
| `PATCH` | `/appointment/<appointment_id>` | Atualiza parcialmente um agendamento |
| `DELETE` | `/appointment/<appointment_id>` | Remove um agendamento |

## 📞 Contato

**Bruno Balbuena**

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:brunobalbuena@gmail.com)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruno-balbuena-778336138/)

---
