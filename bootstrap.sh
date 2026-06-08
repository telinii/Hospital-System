#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "[bootstrap] Projeto: $PROJECT_DIR"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "[bootstrap] Criando virtualenv em $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

echo "[bootstrap] Atualizando pip e instalando dependências..."
# Use pip dentro do venv
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

echo "[bootstrap] Inicializando banco de dados (schema)..."
"$VENV_DIR/bin/python" -c "import main; print('DB inicializado')"

# If --run requested, start uvicorn
if [ "${1:-}" = "--run" ]; then
  echo "[bootstrap] Iniciando servidor (uvicorn)..."
  exec "$VENV_DIR/bin/uvicorn" main:app --reload --host 127.0.0.1 --port 8000
else
  cat <<'EOF'

Bootstrap concluído com sucesso.
Próximos passos:
  1) Ative o virtualenv:  source venv/bin/activate
  2) Rode o servidor localmente:  uvicorn main:app --reload --host 127.0.0.1 --port 8000

Ou execute este script com --run para instalar e iniciar:
  ./bootstrap.sh --run

Acesse a documentação interativa em: http://127.0.0.1:8000/docs

EOF
fi
