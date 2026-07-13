import unittest
import json
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from infrastructure.exporters.excel_exporter import (
    ExcelExporter, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT,
    COLOR_ALERT, COLOR_WARNING, COLOR_SURFACE, COLOR_TEXT_LIGHT,
    auto_width,
)
from infrastructure.exporters._bsc_writer import (
    _kpi_excel_formula, _TIPO_LABELS,
)
from domain.constants import AGENTS_HEADER, DEPARTMENTS_HEADER, KPI_CONFIG


class TestExporterStyle(unittest.TestCase):
    def setUp(self):
        self.exporter = ExcelExporter()

    def test_palette_has_all_required_colors(self):
        self.assertTrue(COLOR_PRIMARY.startswith("#"))
        self.assertTrue(COLOR_SECONDARY.startswith("#"))
        self.assertTrue(COLOR_ACCENT.startswith("#"))
        self.assertTrue(COLOR_ALERT.startswith("#"))
        self.assertTrue(COLOR_WARNING.startswith("#"))
        self.assertTrue(COLOR_SURFACE.startswith("#"))
        self.assertTrue(COLOR_TEXT_LIGHT.startswith("#"))

    def test_agent_header_has_correct_columns(self):
        expected_headers = [
            "Dept maior atendimento", "Grupo", "Nome do Agente",
            "Total de Chats", "% do Departamento",
        ]
        for h in expected_headers:
            self.assertIn(h, AGENTS_HEADER)

    def test_department_header_has_correct_columns(self):
        self.assertIn("Departamento", DEPARTMENTS_HEADER)
        self.assertIn("Total de Chats", DEPARTMENTS_HEADER)
        self.assertIn("SLA Compliance (%)", DEPARTMENTS_HEADER)

    def test_kpi_config_has_all_required_metrics(self):
        t1 = KPI_CONFIG.get("Suporte Técnico", {}).get("t1", [])
        metric_names = [m["name"] for m in t1]
        required = [
            "Elogios de atendimento / Feedback",
            "NPS (Net Promoter Score)",
            "Feedback Negativo (Penalidade)",
            "Atendimentos | Ligações Finalizados",
            "Instalações e Migrações",
            "Assiduidade (sem faltas)",
            "Indicação Comercial",
            "Indicação Comercial - Vendida",
            "Updates, Treinamentos e Tarefas (N1 a N3)",
        ]
        for r in required:
            self.assertIn(r, metric_names, f"Missing KPI metric: {r}")

    def test_kpi_config_t2_has_updates_treinamentos_tarefas(self):
        t2 = KPI_CONFIG.get("Suporte Técnico", {}).get("t2", [])
        names = [m["name"] for m in t2]
        for r in ["Updates", "Treinamentos", "Tarefa N1", "Tarefa N2", "Tarefa N3"]:
            self.assertIn(r, names)

    def test_kpi_config_has_penalidades_setoriais(self):
        penalidades = KPI_CONFIG.get("Suporte Técnico", {}).get("penalidades_setoriais", [])
        self.assertGreater(len(penalidades), 0)
        self.assertEqual(penalidades[0]["name"], "Ligações Perdidas (Setor)")

    def test_bsc_escalonado_percentual_formula(self):
        kpi = {"tipo": "escalonado_percentual", "meta": ">40%", "peso": 30,
               "niveis": [{"min": 40, "pts": 30, "extra_per_unit": 0.75}, {"min": 35, "pts": 15}, {"min": 30, "pts": 10}],
               "cap": 60}
        formula = _kpi_excel_formula("A1", kpi)
        self.assertTrue(formula.startswith("=IF"))
        self.assertIn("A1", formula)
        self.assertIn("40", formula)
        self.assertIn("60", formula)

    def test_bsc_escalonado_nps_formula(self):
        kpi = {"tipo": "escalonado_nps", "meta": ">=70/63/50", "peso": 30,
               "niveis": [{"min": 70, "pts": 30}, {"min": 63, "pts": 15}, {"min": 50, "pts": 5}]}
        formula = _kpi_excel_formula("B2", kpi)
        self.assertTrue(formula.startswith("=IF"))
        self.assertIn("B2", formula)
        self.assertIn("70", formula)

    def test_bsc_penalidade_taxa_formula(self):
        kpi = {"tipo": "penalidade_taxa", "peso": -5, "threshold": 10, "extra_peso": -1, "cap": None}
        formula = _kpi_excel_formula("C3", kpi)
        self.assertTrue(formula.startswith("=IF"))
        self.assertIn("C3", formula)

    def test_bsc_sim_nao_assiduidade_formula(self):
        kpi = {"tipo": "sim_nao_assiduidade", "meta": 0, "peso": 35}
        formula = _kpi_excel_formula("D4", kpi)
        self.assertIn("D4", formula)
        self.assertIn("35", formula)

    def test_bsc_tipo_labels_cover_all_types(self):
        used_types = set()
        for group, config in KPI_CONFIG.items():
            for t in config.get("t1", []):
                if t.get("tipo") and t["tipo"] != "-":
                    used_types.add(t["tipo"])
        for t in config.get("penalidades_setoriais", []):
            if t.get("tipo"):
                used_types.add(t["tipo"])
        missing = used_types - set(_TIPO_LABELS.keys())
        self.assertEqual(len(missing), 0, f"Missing TIPO_LABELS for: {missing}")

    def test_auto_width_no_error(self):
        from xlsxwriter import Workbook
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            wb = Workbook(f.name)
            ws = wb.add_worksheet()
            header = ["Name", "Value"]
            data = [["Alice", 100], ["Bob", 200]]
            auto_width(ws, header, data)
            wb.close()
            os.unlink(f.name)

    def test_tab_names_no_special_chars(self):
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 _-çãáàâéêíóôúü")
        safe_names = ["Resumo Executivo", "Visão Geral", "BSC", "Desempenho Agentes", "Qualidade", "Demanda", "_data"]
        for name in safe_names:
            for c in name:
                self.assertIn(c, allowed, f"Character '{c}' not allowed in tab name '{name}'")

    def test_metadata_exists_in_dto(self):
        from application.interfaces.exporter import DashboardDTO
        self.assertTrue(hasattr(DashboardDTO, "prev_month_metrics"))
        self.assertTrue(hasattr(DashboardDTO, "tabular_header"))
        self.assertTrue(hasattr(DashboardDTO, "bsc_kpi_config"))

    def test_bsc_config_no_old_jira_references(self):
        t1 = KPI_CONFIG.get("Suporte Técnico", {}).get("t1", [])
        t2 = KPI_CONFIG.get("Suporte Técnico", {}).get("t2", [])
        all_names = [m["name"] for m in t1 + t2]
        for name in all_names:
            self.assertNotIn("JIRA", name, f"Found old JIRA reference: {name}")
        self.assertNotIn("Contribuição para base Conhecimento", [m["name"] for m in t1])

    def test_elogios_threshold_updated(self):
        t1 = KPI_CONFIG.get("Suporte Técnico", {}).get("t1", [])
        elogios = next(m for m in t1 if "Elogios" in m["name"])
        niveis = elogios.get("niveis", [])
        self.assertEqual(niveis[0]["min"], 40)

    def test_nps_threshold_updated(self):
        t1 = KPI_CONFIG.get("Suporte Técnico", {}).get("t1", [])
        nps = next(m for m in t1 if "NPS" in m["name"])
        niveis = nps.get("niveis", [])
        self.assertEqual(niveis[-1]["min"], 50)

    def test_feedback_negativo_threshold_updated(self):
        t1 = KPI_CONFIG.get("Suporte Técnico", {}).get("t1", [])
        fn = next(m for m in t1 if "Negativo" in m["name"])
        self.assertEqual(fn["threshold"], 5)
        self.assertEqual(fn.get("cap"), -30)
        self.assertEqual(fn["extra_peso"], -5)

    def test_atendimentos_peso_updated(self):
        t1 = KPI_CONFIG.get("Suporte Técnico", {}).get("t1", [])
        atd = next(m for m in t1 if "Atendimentos" in m["name"])
        self.assertEqual(atd["peso"], 10)

    def test_exec_targets_defined(self):
        from domain.constants import EXEC_TARGETS
        for key in ("nps_real", "sla_compliance", "csat_elogio", "art_medio", "cobertura_avaliados"):
            self.assertIn(key, EXEC_TARGETS)
            self.assertIn("direction", EXEC_TARGETS[key])

    def test_load_bsc_config_exec_targets(self):
        import tempfile
        from infrastructure.config_loader import load_bsc_config
        from domain import constants
        original = constants.EXEC_TARGETS
        yaml_text = "EXEC_TARGETS:\n  foo: { green: 1, amber: 2, direction: higher }\n"
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(yaml_text)
            path = f.name
        try:
            load_bsc_config(path)
            self.assertIn("foo", constants.EXEC_TARGETS)
        finally:
            constants.EXEC_TARGETS = original
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
