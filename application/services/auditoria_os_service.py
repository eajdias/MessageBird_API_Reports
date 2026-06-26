from typing import List, Any, Tuple
from application.interfaces.repository import ReportRepository
from domain import constants, logic


class AuditoriaOSService:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    async def build_report(self, start_date: str, end_date: str, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        rows = await self.repository.fetch_auditoria_os_raw(start_date, end_date)

        # Count chats per contact to determine "Reabertura" (client had >1 chat in period)
        contact_chat_count = {}
        for r in rows:
            cnts_id = r["cnts_id"]
            if cnts_id:
                contact_chat_count[cnts_id] = contact_chat_count.get(cnts_id, 0) + 1

        data_list = []
        for r in rows:
            agnt_name = r["agnt_name"] or "Não Mapeado"
            grp = constants.get_agent_group(agnt_name)
            if agent_group and grp != agent_group:
                continue

            created = logic.format_local_dt(r["cnvs_created"])
            dept = constants.resolve_dept(r["cnvs_dept"])
            contact_reason = constants.resolve_reason(r["cnvs_dept"], r["cnvs_contact_reason"])
            occurrence = constants.resolve_occurrence(r["cnvs_dept"], r["cnvs_contact_reason"], r["cnvs_occurrence"])

            # Centralized duration calculation
            duration = logic.calculate_ticket_duration(r["cnvs_created"], r["cnvs_updated"])

            # Reabertura: contact had more than 1 chat in the period
            cnts_id = r["cnts_id"]
            has_reopening = contact_chat_count.get(cnts_id, 0) > 1

            data_list.append([
                r["cnvs_bird"],
                created,
                agnt_name,
                r["cnts_name"] or "Desconhecido",
                r["cnts_phone"] or "",
                r["cnvs_tax_id"] or "",
                r["cnvs_software"] or "",
                dept,
                contact_reason,
                occurrence,
                r["cnvs_rating_agent"] if r["cnvs_rating_agent"] is not None else "",
                r["cnvs_rating_nps"] if r["cnvs_rating_nps"] is not None else "",
                "Sim" if has_reopening else "Não",
                r["cnvs_description"] or "",
                duration if duration > 0 else "N/D",
                r["cnvs_id"],
                f"./OS/OS_{r['cnvs_bird']}.pdf" if r["cnvs_bird"] else ""
            ])

        return constants.OS_HEADER, data_list

    async def build_report_all(self, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        rows = await self.repository.fetch_auditoria_os_raw_all()

        # Count chats per contact to determine "Reabertura" (client had >1 chat in period)
        contact_chat_count = {}
        for r in rows:
            cnts_id = r["cnts_id"]
            if cnts_id:
                contact_chat_count[cnts_id] = contact_chat_count.get(cnts_id, 0) + 1

        data_list = []
        for r in rows:
            agnt_name = r["agnt_name"] or "Não Mapeado"
            grp = constants.get_agent_group(agnt_name)
            if agent_group and grp != agent_group:
                continue

            created = logic.format_local_dt(r["cnvs_created"])
            dept = constants.resolve_dept(r["cnvs_dept"])
            contact_reason = constants.resolve_reason(r["cnvs_dept"], r["cnvs_contact_reason"])
            occurrence = constants.resolve_occurrence(r["cnvs_dept"], r["cnvs_contact_reason"], r["cnvs_occurrence"])

            # Centralized duration calculation
            duration = logic.calculate_ticket_duration(r["cnvs_created"], r["cnvs_updated"])

            # Reabertura: contact had more than 1 chat in the period
            cnts_id = r["cnts_id"]
            has_reopening = contact_chat_count.get(cnts_id, 0) > 1

            data_list.append([
                r["cnvs_bird"],
                created,
                agnt_name,
                r["cnts_name"] or "Desconhecido",
                r["cnts_phone"] or "",
                r["cnvs_tax_id"] or "",
                r["cnvs_software"] or "",
                dept,
                contact_reason,
                occurrence,
                r["cnvs_rating_agent"] if r["cnvs_rating_agent"] is not None else "",
                r["cnvs_rating_nps"] if r["cnvs_rating_nps"] is not None else "",
                "Sim" if has_reopening else "Não",
                r["cnvs_description"] or "",
                duration if duration > 0 else "N/D",
                r["cnvs_id"],
                f"./OS/OS_{r['cnvs_bird']}.pdf" if r["cnvs_bird"] else ""
            ])

        return constants.OS_HEADER, data_list
