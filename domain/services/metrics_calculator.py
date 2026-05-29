from datetime import datetime
from typing import List, Optional

class MetricsCalculator:
    @staticmethod
    def calculate_nps(scores: List[float]) -> Optional[float]:
        """Calcula o NPS (Net Promoter Score)."""
        valid_scores = [v for v in scores if isinstance(v, (int, float))]
        if not valid_scores:
            return None
        promoters = sum(1 for v in valid_scores if v >= 9)
        detractors = sum(1 for v in valid_scores if v <= 6)
        total = len(valid_scores)
        return round((promoters - detractors) / total * 100, 2)

    @staticmethod
    def calculate_sla_rate(arts: List[float], threshold: int = 60) -> Optional[float]:
        """Calcula a taxa de conformidade SLA (%) baseada no ART."""
        valid_arts = [a for a in arts if isinstance(a, (int, float))]
        if not valid_arts:
            return None
        hits = sum(1 for a in valid_arts if a <= threshold)
        return round((hits / len(valid_arts)) * 100, 2)

    @staticmethod
    def calculate_rating_average(values: List[float]) -> Optional[float]:
        """Alias para calculate_average, focado em ratings."""
        return MetricsCalculator.calculate_average(values)

    @staticmethod
    def calculate_frt(start_dt: Optional[datetime], first_resp_dt: Optional[datetime]) -> Optional[float]:
        """Calcula o FRT (First Response Time) em minutos."""
        if not start_dt or not first_resp_dt or start_dt.date() != first_resp_dt.date():
            return None
        
        delta = (first_resp_dt - start_dt).total_seconds() / 60
        return round(delta, 2) if delta > 0 else 0.0

    @staticmethod
    def calculate_average(values: List[float]) -> Optional[float]:
        """Calcula a média de uma lista de valores."""
        valid_values = [v for v in values if isinstance(v, (int, float))]
        if not valid_values:
            return None
        return round(sum(valid_values) / len(valid_values), 2)

    @staticmethod
    def calculate_nps_distribution(scores: List[float]) -> dict:
        """Calcula a distribuição quantitativa do NPS (Promotores, Neutros, Detratores)."""
        valid_scores = [v for v in scores if isinstance(v, (int, float))]
        dist = {"promoters": 0, "passives": 0, "detractors": 0}
        for v in valid_scores:
            if v >= 9:
                dist["promoters"] += 1
            elif v >= 7:
                dist["passives"] += 1
            else:
                dist["detractors"] += 1
        return dist

    @staticmethod
    def calculate_rating_distribution(values: List[float]) -> dict:
        """Calcula a distribuição quantitativa das notas (1 a 5)."""
        valid_values = [v for v in values if isinstance(v, (int, float))]
        dist = {str(i): 0 for i in range(1, 6)}
        for v in valid_values:
            key = str(int(v))
            if key in dist:
                dist[key] += 1
        return dist
