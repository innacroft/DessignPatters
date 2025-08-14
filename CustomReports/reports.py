from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportSection(ABC):
    @abstractmethod
    def generate(self):
        pass

class CoverPage(ReportSection):
    def __init__(self, client_name, logo):
        self.client_name = client_name
        self.logo = logo

    def generate(self):
        logger.info(f"Cover Page: {self.client_name} with logo {self.logo}")

class StatisticalCharts(ReportSection):
    def __init__(self, data):
        self.data = data

    def generate(self):
        logger.info(f"Charts: {self.data}")

class RecentMovementsTable(ReportSection):
    def __init__(self, movements):
        self.movements = movements

    def generate(self):
        logger.info(f"Recent Movements Table: {self.movements}")

class TrendAnalysis(ReportSection):
    def __init__(self, trends):
        self.trends = trends

    def generate(self):
        logger.info(f"Trend Analysis: {self.trends}")

class Footer(ReportSection):
    def __init__(self, advisor_contact):
        self.advisor_contact = advisor_contact

    def generate(self):
        logger.info(f"Footer: {self.advisor_contact}")

class PDFReport:
    def __init__(self, sections):
        self._sections = tuple(sections)

    def generate_report(self):
        logger.info("PDF Report")
        for section in self._sections:
            section.generate()

class PDFReportBuilder:
    def __init__(self):
        self._sections = []

    def add_cover_page(self, client_name, logo):
        self._sections.append(CoverPage(client_name, logo))
        return self

    def add_charts(self, data):
        self._sections.append(StatisticalCharts(data))
        return self

    def add_recent_movements_table(self, movements):
        self._sections.append(
            RecentMovementsTable(movements=movements))
        return self

    def add_trend_analysis(self, trends):
        self._sections.append(TrendAnalysis(trends))
        return self

    def add_footer(self, advisor_contact):
        self._sections.append(Footer(advisor_contact))
        return self

    def build(self):
        if not self._sections:
            raise ValueError("The report cannot be empty. Please add at least one section.")
        return PDFReport(self._sections)

class ReportDirector:
    def __init__(self, builder):
        self._builder = builder

    def construct_full_report(self, client_name, logo, movements, trends, contact):
        return self._builder.add_cover_page(client_name, logo).add_charts(
            "Investment data"
        ).add_recent_movements_table(movements).add_trend_analysis(
            trends).add_footer(contact).build()

if __name__ == '__main__':
    logger.info("=== Generating Custom Report for Client A ===")
    custom_builder = PDFReportBuilder()
    reporte_client_A = custom_builder.add_cover_page("Client A", "logo.png") \
        .add_recent_movements_table("Last 10 movements") \
        .add_footer("contact@advisor.com") \
        .build()
    reporte_client_A.generate_report()

    logger.info("=== Generating Full Standard Report for Client B ===")
    director = ReportDirector(PDFReportBuilder())
    full_report = director.construct_full_report(
        client_name="Client B",
        logo="company_logo.png",
        movements="Investment portfolio movements Q3 2025",
        trends="Market trends analysis - Bullish outlook",
        contact="financial.advisor@company.com"
    )
    full_report.generate_report()
