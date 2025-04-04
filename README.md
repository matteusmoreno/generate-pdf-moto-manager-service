# 🛠️ MotoManager - Gerador de Relatórios PDF

Este projeto é responsável por gerar **relatórios em PDF** de ordens de serviço (OS) da aplicação MotoManager, utilizando **Flask** e **ReportLab**.

## 📄 Descrição

A partir do ID de uma ordem de serviço, o sistema consome os dados correspondentes e gera um arquivo PDF com:

- Informações do cliente
- Dados da motocicleta
- Lista de produtos utilizados
- Preço da mão de obra e custo total
- Status da OS
- Datas relevantes (criação, início, atualização, finalização, cancelamento)

---

## 📦 Tecnologias Utilizadas

- Python 3.9+
- Flask
- ReportLab (geração de PDF)

---

## 🚀 Como executar localmente

1. Clone o repositório:

```bash
  git clone https://github.com/seu-usuario/motomanger-pdf-generator.git
  cd motomanger-pdf-generator
```

2. Crie um ambiente virtual:

```bash
  python -m venv venv
  source venv/bin/activate  # Linux / Mac
  venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
  pip install -r requirements.txt
```

## 📥 Gerar PDF de uma Ordem de Serviço

Acesse no navegador:

```
http://localhost:5000/generate_pdf/<id_os>
```

Substitua `<id_os>` pelo ID da ordem de serviço desejada.

## 🛠️ Estrutura do Projeto

```
├── app.py              # Código principal da API Flask
├── static/
│   └── logo.png        # (Opcional) Logo da empresa para aparecer no topo do PDF
├── README.md           # Este arquivo
├── requirements.txt    # Dependências do projeto
```

## 📌 Observações
- O logo da empresa deve ser colocado na pasta `static/` com o nome `logo.png` para aparecer no PDF.

## 📄 Licença
Este projeto está licenciado sob a MIT License.


