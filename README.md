# Manager Cert

Obter informações e extrair cadeia de certificados no formato .PEM utilizando API REST.

---

<h2 align="center">👷 Projeto em construção 👷</h2>

---

## Motivador

Existem sistemas/aplicações que não se autoresolvem com certificados de sites HTTPS.  
Quando está preste a expirar o certificado, existe uma grande atenção voltada ao site para obter o novo certificado quanto mais rápido possível e alterar no sistemas/aplicações, com objetivo  ter menos impacto possível no seu funcionamento.  
O projeto está sendo dividido em três partes:

* Criar API para busca informações e fazer o download dos certificados no formato .PEM. ✅ Finalizado
* Desenvolver um banco de dados para ar quais sites serão monitorados. ⚙️ Construção
* Implementar um mecanismo de monitoramento contínuo dos certificados. ⚙️ Construção

Além disso, essa iniciativa serve como uma oportunidade prática de aprendizado, permitindo a exploração de novos frameworks, como o FastAPI no qual não tenho conhecimento, e a compreensão de conceitos importantes.

## ✔️ Técnicas e tecnologias utilizadas

* ``Python 3.11``
* ``FastAPI 0.103.1``
* ``Redis``
* ``Docker``
* ``API REST``
* ``API First``

## 📋 Pré-requisitos

Necessário ter docker instalado na sua máquina.

## 🛠️ Abrir e rodar o projeto

1. Realize fork do repositório.
2. Realize git clone do repositório.
3. Realize o git clone para sua máquina.
4. Navegue até a pasta e execute o comando `docker compose up -d --build` .
5. Após inicializar os containeres, pode acessar a documentação através: <http://localhost:8081/docs> .

## 🔨 Funcionalidades do projeto

* `Funcionalidade 1` - `Obtem cadeia .PEM`: Realiza uma consulta no site, no qual obtem a cadeia do certificado no formato .PEM. Ao incluir a query `download=true` será feito o download do arquivo.

* `Funcionalidade 2` - `Obtem informações do certificado`: A aplicação retornará algumas informações do certificado Base do site no qual foi realizado a consulta.  
  * Retorno da pesquisa:

    ```json
    {
    "nome": "string",
    "numeroSerie": "string",
    "emissor": "string",
    "validoNaoAntes": "string",
    "validoNaoDepois": "string"
    }
    ```
