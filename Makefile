.PHONY: install report annual total help sync sync-daily sync-monthly report-dates backfill-surveys

# Use 'uv run python' consistently to avoid environment path mismatch warnings
# and ensure dependencies like python-dotenv are available.
UV_RUN := uv run python

DB_PATH ?= m_bird.db
CONFIG_PATH ?= config/business_config.json
OUTPUT_DIR ?= reports

install:
	uv sync

help:
	@echo "Standalone Master Reports & Sync Tool"
	@echo "Usage:"
	@echo "  make install                   - Install dependencies"
	@echo "  make report YEAR=2026 MONTH=5 - Generate monthly report"
	@echo "  make annual YEAR=2024         - Generate annual consolidated report"
	@echo "  make total                    - Generate full system report (all history)"
	@echo "  make report-dates FROM=2026-05-25 TO=2026-06-26 - Generate custom date range report"
	@echo "  make sync                     - Run incremental sync (last 60 min)"
	@echo "  make sync-daily               - Run sync for the last 1 day"
	@echo "  make sync-monthly YEAR=2024 MONTH=5 - Run sync for a specific month"
	@echo "  make backfill-surveys         - Re-extract NPS and ratings from existing conversations"
	@echo ""
	@echo "Default sector: Suporte Técnico. Override with SECTOR='Outro Setor'"

annual:
	@if [ -z "$(YEAR)" ]; then \
		echo "Erro: Forneça YEAR. Ex: make annual YEAR=2024"; \
		exit 1; \
	fi
	$(UV_RUN) main.py report --year $(YEAR) --db-path $(DB_PATH) --config-path $(CONFIG_PATH) --output-dir $(OUTPUT_DIR) $(if $(SECTOR),--sector "$(SECTOR)")

total:
	$(UV_RUN) main.py total --db-path $(DB_PATH) --config-path $(CONFIG_PATH) --output-dir $(OUTPUT_DIR) $(if $(SECTOR),--sector "$(SECTOR)")

report:
	$(UV_RUN) main.py report --year $(YEAR) --month $(MONTH) --db-path $(DB_PATH) --config-path $(CONFIG_PATH) --output-dir $(OUTPUT_DIR) $(if $(SECTOR),--sector "$(SECTOR)")

sync:
	$(UV_RUN) main.py sync --db-path $(DB_PATH)

sync-daily:
	$(UV_RUN) main.py sync --messages-days 1 --db-path $(DB_PATH)

sync-monthly:
	@if [ -z "$(YEAR)" ] || [ -z "$(MONTH)" ]; then \
		echo "Erro: Forneça YEAR e MONTH. Ex: make sync-monthly YEAR=2024 MONTH=2"; \
		exit 1; \
	fi
	$(UV_RUN) main.py sync --year $(YEAR) --month $(MONTH) --db-path $(DB_PATH)

report-dates:
	@if [ -z "$(FROM)" ] || [ -z "$(TO)" ]; then \
		echo "Erro: Forneça FROM e TO. Ex: make report-dates FROM=2026-05-25 TO=2026-06-26"; \
		exit 1; \
	fi
	$(UV_RUN) main.py report --from-date $(FROM) --to-date $(TO) --db-path $(DB_PATH) --config-path $(CONFIG_PATH) --output-dir $(OUTPUT_DIR) $(if $(SECTOR),--sector "$(SECTOR)")

backfill-surveys:
	$(UV_RUN) main.py sync --backfill-surveys --db-path $(DB_PATH)
