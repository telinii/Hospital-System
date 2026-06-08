PRAGMA foreign_keys = ON;

-- Tabelas básicas para o protótipo
CREATE TABLE IF NOT EXISTS patients (
  patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  dob TEXT,
  document TEXT,
  contact_phone TEXT
);

CREATE TABLE IF NOT EXISTS units (
  unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  type TEXT
);

CREATE TABLE IF NOT EXISTS queue_entries (
  entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
  unit_id INTEGER NOT NULL REFERENCES units(unit_id),
  patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
  priority INTEGER NOT NULL DEFAULT 3,
  status TEXT NOT NULL DEFAULT 'waiting',
  created_at TEXT NOT NULL,
  notes TEXT
);

-- Seed: unidade padrão para testes (idempotente)
INSERT OR IGNORE INTO units (unit_id, name, type) VALUES (1, 'Emergência - Triagem', 'triage');
