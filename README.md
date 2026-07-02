FilaHospital - Protótipo (instruções para iniciantes)

Pré-requisitos
- Python 3.8+ instalado
- (Opcional) curl para testar endpoints

Passos para rodar localmente
1. Abra um terminal e vá para a pasta do projeto:
   cd /home/seu_usuario/filahospital

2. Crie e ative um virtualenv (recomendado):
   python3 -m venv venv
   source venv/bin/activate

3. Instale dependências:
   pip install -r requirements.txt

4. Rode a aplicação (UVicorn):
   uvicorn main:app --reload --host 127.0.0.1 --port 8000

5. Abra a documentação interativa em:
   http://127.0.0.1:8000/docs

Testes rápidos (exemplos curl)
- Criar paciente:
  curl -s -X POST "http://127.0.0.1:8000/patients" -H "Content-Type: application/json" -d '{"name":"Maria Silva","dob":"1985-04-20","document":"12345678900","contact_phone":"+5511999999999"}' | jq

- Inserir na fila (use unit_id 1 seedado):
  curl -s -X POST "http://127.0.0.1:8000/units/1/queue/entries" -H "Content-Type: application/json" -d '{"patient_id":1,"priority":3,"notes":"Queixa: dor leve"}' | jq

- Listar fila da unidade 1:
  curl -s "http://127.0.0.1:8000/units/1/queue" | jq

Observações para iniciantes
- O protótipo usa um banco SQLite local (filahospital.db). O arquivo e as tabelas são criados automaticamente na primeira execução.
- Para evoluir o projeto: adicionar autenticação, migrações com Alembic, testes automatizados e Docker/Helm para deploy.

Se quiser, eu posso:
- Gerar um Dockerfile e docker-compose para rodar facilmente
- Adicionar autenticação simples (login JWT)
- Gerar scripts de migração Alembic

Diga qual próximo passo prefere e eu guio você passo a passo.
