import os
import logging
import re
from typing import List, Any, Dict
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

# Chat history colors
_CLIENT_BG = (230, 240, 250)      # Light blue for client messages
_AGENT_BG = (240, 240, 240)       # Light gray for agent messages
_CLIENT_TEXT = (26, 58, 92)       # Dark blue for client text
_AGENT_TEXT = (80, 80, 80)        # Dark gray for agent text

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
    "\U0001F900-\U0001F9FF"
    "\U00002702-\U000027B0"
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "\U00002640"
    "\U00002642"
    "\U00002695"
    "\U00002696"
    "\U00002708"
    "\U00002764"
    "\U00002714"
    "\U00002716"
    "\U0000270A"
    "\U0000270B"
    "\U0001F44D"
    "\U0001F44E"
    "\U0001F44A"
    "\U0001F44B"
    "\U0001F44C"
    "\U0001F44F"
    "\U0001F64F"
    "\U0001F450"
    "\U0001F4AA"
    "\U0001F446"
    "\U0001F447"
    "\U0001F448"
    "\U0001F449"
    "\U0001F440"
    "\U0001F442"
    "\U0001F443"
    "\U0001F445"
    "\U0001F48D"
    "\U0001F48E"
    "\U0001F484"
    "\U0001F483"
    "\U0001F486"
    "\U0001F487"
    "\U0001F488"
    "\U0001F489"
    "\U0001F48A"
    "\U0001F48B"
    "\U0001F48C"
    "\U0001F48D"
    "\U0001F48E"
    "\U0001F48F"
    "\U0001F490"
    "\U0001F491"
    "\U0001F492"
    "\U0001F493"
    "\U0001F494"
    "\U0001F495"
    "\U0001F496"
    "\U0001F497"
    "\U0001F498"
    "\U0001F499"
    "\U0001F49A"
    "\U0001F49B"
    "\U0001F49C"
    "\U0001F49D"
    "\U0001F49E"
    "\U0001F49F"
    "\U0001F4A0"
    "\U0001F4A1"
    "\U0001F4A2"
    "\U0001F4A3"
    "\U0001F4A4"
    "\U0001F4A5"
    "\U0001F4A6"
    "\U0001F4A7"
    "\U0001F4A8"
    "\U0001F4A9"
    "\U0001F4AA"
    "\U0001F4AB"
    "\U0001F4AC"
    "\U0001F4AD"
    "\U0001F4AE"
    "\U0001F4AF"
    "\U0001F4B0"
    "\U0001F4B1"
    "\U0001F4B2"
    "\U0001F4B3"
    "\U0001F4B4"
    "\U0001F4B5"
    "\U0001F4B6"
    "\U0001F4B7"
    "\U0001F4B8"
    "\U0001F4B9"
    "\U0001F4BA"
    "\U0001F4BB"
    "\U0001F4BC"
    "\U0001F4BD"
    "\U0001F4BE"
    "\U0001F4BF"
    "\U0001F4C0"
    "\U0001F4C1"
    "\U0001F4C2"
    "\U0001F4C3"
    "\U0001F4C4"
    "\U0001F4C5"
    "\U0001F4C6"
    "\U0001F4C7"
    "\U0001F4C8"
    "\U0001F4C9"
    "\U0001F4CA"
    "\U0001F4CB"
    "\U0001F4CC"
    "\U0001F4CD"
    "\U0001F4CE"
    "\U0001F4CF"
    "\U0001F4D0"
    "\U0001F4D1"
    "\U0001F4D2"
    "\U0001F4D3"
    "\U0001F4D4"
    "\U0001F4D5"
    "\U0001F4D6"
    "\U0001F4D7"
    "\U0001F4D8"
    "\U0001F4D9"
    "\U0001F4DA"
    "\U0001F4DB"
    "\U0001F4DC"
    "\U0001F4DD"
    "\U0001F4DE"
    "\U0001F4DF"
    "\U0001F4E0"
    "\U0001F4E1"
    "\U0001F4E2"
    "\U0001F4E3"
    "\U0001F4E4"
    "\U0001F4E5"
    "\U0001F4E6"
    "\U0001F4E7"
    "\U0001F4E8"
    "\U0001F4E9"
    "\U0001F4EA"
    "\U0001F4EB"
    "\U0001F4EC"
    "\U0001F4ED"
    "\U0001F4EE"
    "\U0001F4EF"
    "\U0001F4F0"
    "\U0001F4F1"
    "\U0001F4F2"
    "\U0001F4F3"
    "\U0001F4F4"
    "\U0001F4F5"
    "\U0001F4F6"
    "\U0001F4F7"
    "\U0001F4F8"
    "\U0001F4F9"
    "\U0001F4FA"
    "\U0001F4FB"
    "\U0001F4FC"
    "\U0001F4FD"
    "\U0001F4FE"
    "\U0001F4FF"
    "\U0001F500"
    "\U0001F501"
    "\U0001F502"
    "\U0001F503"
    "\U0001F504"
    "\U0001F505"
    "\U0001F506"
    "\U0001F507"
    "\U0001F508"
    "\U0001F509"
    "\U0001F50A"
    "\U0001F50B"
    "\U0001F50C"
    "\U0001F50D"
    "\U0001F50E"
    "\U0001F50F"
    "\U0001F510"
    "\U0001F511"
    "\U0001F512"
    "\U0001F513"
    "\U0001F514"
    "\U0001F515"
    "\U0001F516"
    "\U0001F517"
    "\U0001F518"
    "\U0001F519"
    "\U0001F51A"
    "\U0001F51B"
    "\U0001F51C"
    "\U0001F51D"
    "\U0001F51E"
    "\U0001F51F"
    "\U0001F520"
    "\U0001F521"
    "\U0001F522"
    "\U0001F523"
    "\U0001F524"
    "\U0001F525"
    "\U0001F526"
    "\U0001F527"
    "\U0001F528"
    "\U0001F529"
    "\U0001F52A"
    "\U0001F52B"
    "\U0001F52C"
    "\U0001F52D"
    "\U0001F52E"
    "\U0001F52F"
    "\U0001F530"
    "\U0001F531"
    "\U0001F532"
    "\U0001F533"
    "\U0001F534"
    "\U0001F535"
    "\U0001F536"
    "\U0001F537"
    "\U0001F538"
    "\U0001F539"
    "\U0001F53A"
    "\U0001F53B"
    "\U0001F53C"
    "\U0001F53D"
    "\U0001F53E"
    "\U0001F53F"
    "\U0001F540"
    "\U0001F541"
    "\U0001F542"
    "\U0001F543"
    "\U0001F544"
    "\U0001F545"
    "\U0001F546"
    "\U0001F547"
    "\U0001F548"
    "\U0001F549"
    "\U0001F54A"
    "\U0001F54B"
    "\U0001F54C"
    "\U0001F54D"
    "\U0001F54E"
    "\U0001F54F"
    "\U0001F550"
    "\U0001F551"
    "\U0001F552"
    "\U0001F553"
    "\U0001F554"
    "\U0001F555"
    "\U0001F556"
    "\U0001F557"
    "\U0001F558"
    "\U0001F559"
    "\U0001F55A"
    "\U0001F55B"
    "\U0001F55C"
    "\U0001F55D"
    "\U0001F55E"
    "\U0001F55F"
    "\U0001F560"
    "\U0001F561"
    "\U0001F562"
    "\U0001F563"
    "\U0001F564"
    "\U0001F565"
    "\U0001F566"
    "\U0001F567"
    "\U0001F568"
    "\U0001F569"
    "\U0001F56A"
    "\U0001F56B"
    "\U0001F56C"
    "\U0001F56D"
    "\U0001F56E"
    "\U0001F56F"
    "\U0001F570"
    "\U0001F571"
    "\U0001F572"
    "\U0001F573"
    "\U0001F574"
    "\U0001F575"
    "\U0001F576"
    "\U0001F577"
    "\U0001F578"
    "\U0001F579"
    "\U0001F57A"
    "\U0001F57B"
    "\U0001F57C"
    "\U0001F57D"
    "\U0001F57E"
    "\U0001F57F"
    "\U0001F580"
    "\U0001F581"
    "\U0001F582"
    "\U0001F583"
    "\U0001F584"
    "\U0001F585"
    "\U0001F586"
    "\U0001F587"
    "\U0001F588"
    "\U0001F589"
    "\U0001F58A"
    "\U0001F58B"
    "\U0001F58C"
    "\U0001F58D"
    "\U0001F58E"
    "\U0001F58F"
    "\U0001F590"
    "\U0001F591"
    "\U0001F592"
    "\U0001F593"
    "\U0001F594"
    "\U0001F595"
    "\U0001F596"
    "\U0001F597"
    "\U0001F598"
    "\U0001F599"
    "\U0001F59A"
    "\U0001F59B"
    "\U0001F59C"
    "\U0001F59D"
    "\U0001F59E"
    "\U0001F59F"
    "\U0001F5A0"
    "\U0001F5A1"
    "\U0001F5A2"
    "\U0001F5A3"
    "\U0001F5A4"
    "\U0001F5A5"
    "\U0001F5A6"
    "\U0001F5A7"
    "\U0001F5A8"
    "\U0001F5A9"
    "\U0001F5AA"
    "\U0001F5AB"
    "\U0001F5AC"
    "\U0001F5AD"
    "\U0001F5AE"
    "\U0001F5AF"
    "\U0001F5B0"
    "\U0001F5B1"
    "\U0001F5B2"
    "\U0001F5B3"
    "\U0001F5B4"
    "\U0001F5B5"
    "\U0001F5B6"
    "\U0001F5B7"
    "\U0001F5B8"
    "\U0001F5B9"
    "\U0001F5BA"
    "\U0001F5BB"
    "\U0001F5BC"
    "\U0001F5BD"
    "\U0001F5BE"
    "\U0001F5BF"
    "\U0001F5C0"
    "\U0001F5C1"
    "\U0001F5C2"
    "\U0001F5C3"
    "\U0001F5C4"
    "\U0001F5C5"
    "\U0001F5C6"
    "\U0001F5C7"
    "\U0001F5C8"
    "\U0001F5C9"
    "\U0001F5CA"
    "\U0001F5CB"
    "\U0001F5CC"
    "\U0001F5CD"
    "\U0001F5CE"
    "\U0001F5CF"
    "\U0001F5D0"
    "\U0001F5D1"
    "\U0001F5D2"
    "\U0001F5D3"
    "\U0001F5D4"
    "\U0001F5D5"
    "\U0001F5D6"
    "\U0001F5D7"
    "\U0001F5D8"
    "\U0001F5D9"
    "\U0001F5DA"
    "\U0001F5DB"
    "\U0001F5DC"
    "\U0001F5DD"
    "\U0001F5DE"
    "\U0001F5DF"
    "\U0001F5E0"
    "\U0001F5E1"
    "\U0001F5E2"
    "\U0001F5E3"
    "\U0001F5E4"
    "\U0001F5E5"
    "\U0001F5E6"
    "\U0001F5E7"
    "\U0001F5E8"
    "\U0001F5E9"
    "\U0001F5EA"
    "\U0001F5EB"
    "\U0001F5EC"
    "\U0001F5ED"
    "\U0001F5EE"
    "\U0001F5EF"
    "\U0001F5F0"
    "\U0001F5F1"
    "\U0001F5F2"
    "\U0001F5F3"
    "\U0001F5F4"
    "\U0001F5F5"
    "\U0001F5F6"
    "\U0001F5F7"
    "\U0001F5F8"
    "\U0001F5F9"
    "\U0001F5FA"
    "\U0001F5FB"
    "\U0001F5FC"
    "\U0001F5FD"
    "\U0001F5FE"
    "\U0001F5FF"
    "]+", flags=re.UNICODE
)

def _sanitize(text: str) -> str:
    if not text:
        return ""
    text = str(text)
    # Remove all non-Latin-1 characters (including emojis)
    result = []
    for char in text:
        try:
            char.encode("latin-1")
            result.append(char)
        except UnicodeEncodeError:
            pass
    return "".join(result)

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

    def _chat_history_header(self, protocolo: str, client_name: str, phone: str):
        self.set_fill_color(*_HEADER_COLOR)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, " HISTÓRICO DE MENSAGENS", align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)
        
        # Client info bar
        self.set_fill_color(*_SECTION_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(25, 7, " OS:", fill=True, border="B")
        self.set_font("Helvetica", "", 9)
        self.cell(50, 7, f" {_sanitize(protocolo)}", border="B")
        
        self.set_fill_color(*_LABEL_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(25, 7, " Cliente:", fill=True, border="B")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 7, f" {_sanitize(client_name)}", border="B", new_x="LMARGIN", new_y="NEXT")
        
        self.set_fill_color(*_SECTION_COLOR)
        self.set_font("Helvetica", "B", 9)
        self.cell(25, 7, " Telefone:", fill=True, border="B")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 7, f" {_sanitize(phone)}", border="B", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def _chat_message(self, sender: str, content: str, timestamp: str, is_client: bool = True):
        # Calculate available width
        margin = 15
        max_width = self.epw - 2 * margin
        
        # Sender and timestamp line
        self.set_font("Helvetica", "B", 8)
        if is_client:
            self.set_text_color(*_CLIENT_TEXT)
            label = f"[CLIENTE] {sender}"
        else:
            self.set_text_color(*_AGENT_TEXT)
            label = f"[AGENTE] {sender}"
        
        time_label = timestamp
        self.cell(0, 5, f"{_sanitize(label)}  |  {_sanitize(time_label)}", new_x="LMARGIN", new_y="NEXT")
        
        # Message bubble
        self.set_font("Helvetica", "", 9)
        self.set_text_color(0, 0, 0)
        
        if is_client:
            self.set_fill_color(*_CLIENT_BG)
        else:
            self.set_fill_color(*_AGENT_BG)
        
        # Calculate message height
        lines = self.multi_cell(max_width - 10, 5, _sanitize(content), dry_run=True, output="LINES")
        msg_height = len(lines) * 5 + 4
        
        # Check if we need a new page
        if self.get_y() + msg_height > self.h - 20:
            self.add_page()
        
        # Draw message bubble
        y_start = self.get_y()
        self.set_x(margin + 5)
        self.multi_cell(max_width - 10, 5, _sanitize(content), fill=True, border="B",
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(3)


class PDFExporter:
    def export_os_pdfs(self, output_dir: str, header: List[str], data: List[List[Any]], 
                       messages_dict: Dict[int, List[Dict[str, Any]]] = None):
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

                # 6. Chat History (Page 2+)
                if messages_dict:
                    cnvs_id = row[15]  # ID BD
                    messages = messages_dict.get(cnvs_id, [])
                    
                    if messages:
                        pdf.add_page()
                        pdf._chat_history_header(protocolo, _val(row[3]), _val(row[4]))
                        
                        for msg in messages:
                            # Messages are now dictionaries
                            timestamp = msg.get("msgs_created", "")
                            content = msg.get("msgs_content", "")
                            direction = msg.get("msgs_direction", "")
                            agnt_name = msg.get("agnt_name", "")
                            cnts_name = msg.get("cnts_name", "Cliente")
                            
                            if timestamp:
                                # Format timestamp to show only time
                                try:
                                    if " " in str(timestamp):
                                        timestamp = str(timestamp).split(" ")[1][:5]
                                except:
                                    pass
                            
                            if not content:
                                continue
                            
                            is_client = (direction == "received")
                            if is_client:
                                sender = cnts_name
                            else:
                                sender = agnt_name if agnt_name else "Agente"
                            
                            pdf._chat_message(sender, str(content), str(timestamp), is_client)

                pdf.output(pdf_path)
                generated += 1

            except Exception as e:
                logger.error(f"Failed to generate PDF for row {row}: {e}")

        logger.info(f"Generated {generated} OS PDFs in {output_dir}")
