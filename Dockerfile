# Imagem base oficial com Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos da aplicação
COPY . .

# Instala dependências
RUN pip install --upgrade pip && pip install flask reportlab requests

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para iniciar o Flask
CMD ["flask", "run", "--host=0.0.0.0"]
