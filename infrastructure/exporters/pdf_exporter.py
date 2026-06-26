import os
import logging
import re
from typing import List, Any
from fpdf import FPDF
from rich.console import Console

logger = logging.getLogger("standalone.pdf_exporter")
console = Console()

_HEADER_COLOR = (26, 58, 92)      # Dark Blue MessageBird style
_SECTION_COLOR = (235, 240, 245)  # Very light blue for section headers
_LABEL_COLOR = (245, 245, 245)    # Light gray for labels
_BRAND_COLOR = (0, 102, 204)      # Primary Brand Blue
_SUCCESS_COLOR = (34, 139, 34)    # Green for promoters
_DANGER_COLOR = (220, 53, 69)     # Red for detractors/complaints
_DANGER_BG = (255, 230, 230)      # Light red background

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
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 12, " ORDEM DE SERVIÇO - ASSISTÊNCIA TÉCNICA",
                  align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(0, 0, 0)

    def _section(self, title: str):
        self.set_fill_color(*_SECTION_COLOR)
        self.set_text_color(*_HEADER_COLOR)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, f"  {_sanitize(title).upper()}", fill=True, border="B", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def _row(self, label: str, value: str, label_w: float = 45, val_color=None, bg_color=None):
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(label_w, 7, f" {_sanitize(label)}", fill=True, border="B")
        
        self.set_font("Helvetica", "", 9)
        if val_color: self.set_text_color(*val_color)
        if bg_color: self.set_fill_color(*bg_color)
        
        fill = True if bg_color else False
        self.multi_cell(self.epw - label_w, 7, f" {_sanitize(value)}", border="B", fill=fill,
                        new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def _two_cols(self, l1: str, v1: str, l2: str, v2: str, label_w: float = 45, v1_color=None, v2_color=None):
        half = self.epw / 2
        
        # Col 1
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(label_w, 7, f" {_sanitize(l1)}", fill=True, border="B")
        
        self.set_font("Helvetica", "", 9)
        if v1_color: self.set_text_color(*v1_color)
        self.cell(half - label_w, 7, f" {_sanitize(v1)}", border="B")
        self.set_text_color(0, 0, 0)
        
        # Col 2
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(label_w, 7, f" {_sanitize(l2)}", fill=True, border="B")
        
        self.set_font("Helvetica", "", 9)
        if v2_color: self.set_text_color(*v2_color)
        self.cell(self.epw - 2 * label_w - (half - label_w), 7, f" {_sanitize(v2)}",
                  border="B", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def _protocol_header(self, protocolo: str):
        self.set_fill_color(*_BRAND_COLOR)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 10)
        self.cell(40, 8, " ID DA OS: ", fill=True)
        
        self.set_fill_color(240, 248, 255) # Light brand blue
        self.set_text_color(*_HEADER_COLOR)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"  {_sanitize(protocolo)}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(4)


class PDFExporter:
    def export_os_pdfs(self, output_dir: str, header: List[str], data: List[List[Any]]):
        os.makedirs(output_dir, exist_ok=True)
        generated = 0

        def _val(v):
            v = str(v).strip()
            if not v or v.lower() in ("none", "nan", "n/d", ""):
                return "N/A"
            return v

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

                # 1. Protocolo Destacado
                pdf._protocol_header(protocolo)

                # 2. Dados do Cliente
                pdf._section("Dados do Cliente")
                pdf._row("Cliente:", _val(row[3]))
                pdf._row("Telefone:", _val(row[4]))
                # Documento is row[5] (cnvs_tax_id), ID BD is row[15] (cnvs_id)
                pdf._two_cols("Documento:", _val(row[5]), "ID BD:", _val(row[15]))
                pdf.ln(4)

                # 3. Equipamento ou Sistema
                pdf._section("Equipamento / Sistema")
                sistema = _val(row[6])
                # Redundancy fix: if we only have one field for system/product, 
                # keep product as N/A to avoid repeating the same value.
                produto = "N/A"
                pdf._two_cols("Sistema:", sistema, "Produto:", produto)
                pdf.ln(4)

                # 4. Detalhamento dos Defeitos
                pdf._section("Detalhamento do Atendimento")
                pdf._two_cols("Motivo:", _val(row[8]), "Ocorrência:", _val(row[9]))

                desc = str(row[13])
                if not desc.strip(): desc = "Sem descrição detalhada."
                if len(desc) > 800: desc = desc[:797] + "..."
                
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_fill_color(*_LABEL_COLOR)
                pdf.cell(0, 7, " Descrição relatada:", fill=True, new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 6, f"{_sanitize(desc)}", border="B", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)

                # Reclamação com Alerta Visual
                reclamacao_row = row[12] if isinstance(row[12], str) else "Sim" if (row[12] or 0) > 0 else "Não"
                reclamacao = "SIM" if reclamacao_row == "Sim" else "NÃO"
                rec_bg = _DANGER_BG if reclamacao == "SIM" else None
                rec_color = _DANGER_COLOR if reclamacao == "SIM" else None
                
                pdf._row("Houve Reclamação?", reclamacao, val_color=rec_color, bg_color=rec_bg)
                pdf._row("Retornante no mês?", "N/A")
                pdf.ln(4)

                # 5. Métricas e Análise
                pdf._section("Métricas e Análise (GP/GQ)")
                
                # Formatação Condicional NPS
                nps_val = _val(row[11])
                nps_color = None
                try:
                    nps_int = int(nps_val)
                    if nps_int >= 9:
                        nps_color = _SUCCESS_COLOR
                    elif nps_int <= 6:
                        nps_color = _DANGER_COLOR
                except:
                    pass
                
                pdf._two_cols("Nota do Técnico:", _val(row[10]), "Nota NPS:", nps_val, v2_color=nps_color)
                pdf._two_cols("Agente:", _val(row[2]), "Departamento:", _val(row[7]))
                pdf._two_cols("Data Início:", _val(row[1]), "Duração (min):", _val(row[14]))
                pdf._row("Abrir Ação Corretiva:", "NÃO")

                pdf.output(pdf_path)
                generated += 1

            except Exception as e:
                logger.error(f"Failed to generate PDF for row {row}: {e}")

        logger.info(f"Generated {generated} OS PDFs in {output_dir}")
