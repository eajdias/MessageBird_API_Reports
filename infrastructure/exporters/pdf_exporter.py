import os
import logging
import re
from typing import List, Any
from fpdf import FPDF
from rich.console import Console

logger = logging.getLogger("standalone.pdf_exporter")
console = Console()

_HEADER_COLOR = (26, 58, 92)
_SECTION_COLOR = (220, 230, 241)
_LABEL_COLOR = (240, 240, 240)

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000026FF"
    "]+", flags=re.UNICODE
)

def _sanitize(text: str) -> str:
    if not text:
        return ""
    text = _EMOJI_PATTERN.sub("", str(text))
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text

class _OSPDF(FPDF):
    def header(self):
        self.set_fill_color(*_HEADER_COLOR)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "ORDEM DE SERVIÇO DE ASSISTÊNCIA TÉCNICA DE SOFTWARE",
                  align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    def _section(self, title: str):
        self.set_fill_color(*_SECTION_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 6, f"  {_sanitize(title)}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def _row(self, label: str, value: str, label_w: float = 45):
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 8)
        self.cell(label_w, 6, f" {_sanitize(label)}", fill=True, border=1)
        self.set_font("Helvetica", "", 8)
        self.multi_cell(self.epw - label_w, 6, f" {_sanitize(value)}", border=1,
                        new_x="LMARGIN", new_y="NEXT")

    def _two_cols(self, l1: str, v1: str, l2: str, v2: str, label_w: float = 45):
        half = self.epw / 2
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 8)
        self.cell(label_w, 6, f" {_sanitize(l1)}", fill=True, border=1)
        self.set_font("Helvetica", "", 8)
        self.cell(half - label_w, 6, f" {_sanitize(v1)}", border=1)
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 8)
        self.cell(label_w, 6, f" {_sanitize(l2)}", fill=True, border=1)
        self.set_font("Helvetica", "", 8)
        self.cell(self.epw - 2 * label_w - (half - label_w), 6, f" {_sanitize(v2)}",
                  border=1, new_x="LMARGIN", new_y="NEXT")

class PDFExporter:
    def export_os_pdfs(self, output_dir: str, header: List[str], data: List[List[Any]]):
        os.makedirs(output_dir, exist_ok=True)
        generated = 0

        for row in data:
            try:
                protocolo = str(row[0])
                if not protocolo: continue

                pdf_path = os.path.join(output_dir, f"OS_{protocolo}.pdf")

                pdf = _OSPDF(orientation="P", unit="mm", format="A4")
                pdf.alias_nb_pages()
                pdf.set_margins(15, 15, 15)
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                pdf.set_fill_color(*_LABEL_COLOR)
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(35, 7, " PROTOCOLO No:", fill=True, border=1)
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 7, f"  {_sanitize(protocolo)}", border=1, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

                pdf._section("DADOS DO CLIENTE")
                pdf._row("Cliente:", str(row[4]))
                pdf._two_cols("E-mail:", str(row[6]), "Telefone:", str(row[5]))
                pdf._two_cols("Documento:", str(row[7]), "ID BD:", protocolo)
                pdf.ln(2)

                pdf._section("EQUIPAMENTO OU SISTEMA")
                pdf._two_cols("Sistema:", str(row[8]), "Produto:", str(row[8]))
                pdf.ln(2)

                pdf._section("DETALHAMENTO DOS DEFEITOS")
                pdf._two_cols("Motivo:", str(row[10]), "Ocorrência:", str(row[11]))

                desc = str(row[15])
                if len(desc) > 500: desc = desc[:497] + "..."
                pdf._row("Descrição:", desc)

                lw = 45
                half = pdf.epw / 2
                pdf.set_fill_color(*_LABEL_COLOR)
                pdf.set_font("Helvetica", "B", 8)
                pdf.cell(lw, 6, " Reclamação?", fill=True, border=1)
                pdf.set_font("Helvetica", "", 8)
                reclamacao = "SIM" if int(row[14] or 0) > 0 else "NÃO"
                pdf.cell(half - lw, 6, f" {_sanitize(reclamacao)}", border=1)

                pdf.set_fill_color(*_LABEL_COLOR)
                pdf.set_font("Helvetica", "B", 8)
                pdf.cell(lw, 6, " Retornante no mês?", fill=True, border=1)
                pdf.set_font("Helvetica", "", 8)
                pdf.cell(pdf.epw - 2 * lw - (half - lw), 6, " N/A", border=1,
                         new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

                pdf._section("MÉTRICAS DE ATENDIMENTO (NPS)")
                pdf._two_cols("Nota do Técnico:", str(row[12]), "Nota NPS:", str(row[13]))
                pdf.ln(2)

                pdf._section("ANÁLISE DO RELATÓRIO (GP/GQ)")
                pdf._row("Agente:", str(row[2]))
                pdf._row("Departamento:", str(row[9]))
                pdf._two_cols("Data Início:", str(row[1]), "Duração:", str(row[16]))

                pdf.set_fill_color(*_LABEL_COLOR)
                pdf.set_font("Helvetica", "B", 8)
                pdf.cell(lw, 6, " Abrir Ação Corretiva:", fill=True, border=1)
                pdf.set_font("Helvetica", "", 8)
                acao = "NÃO"
                pdf.cell(pdf.epw - lw, 6, f" {_sanitize(acao)}", border=1,
                         new_x="LMARGIN", new_y="NEXT")

                pdf.output(pdf_path)
                generated += 1
            except Exception as e:
                logger.error(f"Erro ao gerar PDF para OS {row[0]}: {e}")

        console.print(f"  [green]Ordens de Serviço geradas:[/] {generated} arquivo(s) em {output_dir}")
        return generated
