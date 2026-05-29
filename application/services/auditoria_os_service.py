from typing import List, Any, Tuple
from application.interfaces.repository import ReportRepository
from domain import constants, logic


class AuditoriaOSService:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    async def build_report(self, start_date: str, end_date: str, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        rows = await self.repository.fetch_auditoria_os_raw(start_date, end_date)

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

            data_list.append([
                r["cnvs_id"],
                created,
                agnt_name,
                grp,
                r["cnts_name"] or "Desconhecido",
                r["cnts_phone"] or "",
                r["cnts_custom1"] or "",
                r["cnts_custom2"] or "",
                r["cnvs_software"] or "",
                dept,
                contact_reason,
                occurrence,
                r["cnvs_rating_agent"] if r["cnvs_rating_agent"] is not None else "",
                r["cnvs_rating_nps"] if r["cnvs_rating_nps"] is not None else "",
                r["cnvs_reopened_count"] or 0,
                r["cnvs_description"] or "",
                r["calc_duration_min"] if r["calc_duration_min"] is not None else "N/D"
            ])

        return constants.OS_HEADER, data_list

    async def build_report_all(self, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        rows = await self.repository.fetch_auditoria_os_raw_all()

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

            data_list.append([
                r["cnvs_id"],
                created,
                agnt_name,
                grp,
                r["cnts_name"] or "Desconhecido",
                r["cnts_phone"] or "",
                r["cnts_custom1"] or "",
                r["cnts_custom2"] or "",
                r["cnvs_software"] or "",
                dept,
                contact_reason,
                occurrence,
                r["cnvs_rating_agent"] if r["cnvs_rating_agent"] is not None else "",
                r["cnvs_rating_nps"] if r["cnvs_rating_nps"] is not None else "",
                r["cnvs_reopened_count"] or 0,
                r["cnvs_description"] or "",
                r["calc_duration_min"] if r["calc_duration_min"] is not None else "N/D"
            ])

        return constants.OS_HEADER, data_list
