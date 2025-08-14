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
        if not sections:
            raise ValueError("Report sections cannot be empty")
        if not isinstance(sections, (list, tuple)):
            raise TypeError("Sections must be a list or tuple")

        for i, section in enumerate(sections):
            if not isinstance(section, ReportSection):
                raise TypeError(f"Section {i} must be an instance of ReportSection")

        self._sections = tuple(sections)  # Inmutable

    def generate_report(self):
        logger.info("=== PDF Report Generation Started ===")
        try:
            for section in self._sections:
                section.generate()
            logger.info("=== PDF Report Generation Completed ===")
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise

class PDFReportBuilder:
    def __init__(self):
        self._sections = []
        self._has_cover_page = False
        self._has_footer = False

    def add_cover_page(self, client_name, logo):
        try:
            if not client_name or not client_name.strip():
                raise ValueError("Client name cannot be empty")
            if not logo or not logo.strip():
                raise ValueError("Logo path cannot be empty")
            if self._has_cover_page:
                raise ValueError("Cover page already added. Only one cover page allowed per report")

            self._sections.append(CoverPage(client_name, logo))
            self._has_cover_page = True
            logger.info("Cover page added successfully for client: %s", client_name)
            return self
        except ValueError as e:
            logger.error("Error adding cover page: %s", e)
            raise

    def add_charts(self, data):
        try:
            if not data or not data.strip():
                raise ValueError("Charts data cannot be empty")
            self._sections.append(StatisticalCharts(data))
            logger.info("Charts section added successfully")
            return self
        except ValueError as e:
            logger.error("Error adding charts: %s", e)
            raise

    def add_recent_movements_table(self, movements):
        try:
            if not movements or not movements.strip():
                raise ValueError("Movements data cannot be empty")
            self._sections.append(
                RecentMovementsTable(movements=movements))
            logger.info("Recent movements table added successfully")
            return self
        except ValueError as e:
            logger.error("Error adding recent movements table: %s", e)
            raise

    def add_trend_analysis(self, trends):
        try:
            if not trends or not trends.strip():
                raise ValueError("Trends data cannot be empty")
            self._sections.append(TrendAnalysis(trends))
            logger.info("Trend analysis section added successfully")
            return self
        except ValueError as e:
            logger.error("Error adding trend analysis: %s", e)
            raise

    def add_footer(self, advisor_contact):
        try:
            if not advisor_contact or not advisor_contact.strip():
                raise ValueError("Advisor contact cannot be empty")
            if self._has_footer:
                raise ValueError(
                    "Footer already added. Only one footer allowed per report")

            self._sections.append(Footer(advisor_contact))
            self._has_footer = True
            logger.info("Footer added successfully")
            return self
        except ValueError as e:
            logger.error("Error adding footer: %s", e)
            raise

    def build(self):
        try:
            if not self._sections:
                raise ValueError(
                    "The report cannot be empty. Please add at least one section.")

            if not self._has_cover_page:
                raise ValueError(
                    "Report must have a cover page. Use add_cover_page() first.")

            if not self._has_footer:
                raise ValueError(
                    "Report must have a footer. Use add_footer() before building.")

            report = PDFReport(self._sections)
            logger.info("Report built successfully with %d sections", len(self._sections))
            self._reset()
            return report
        except ValueError as e:
            logger.error("Error building report: %s", e)
            raise

    def _reset(self):
        """Reset builder state for safe reuse"""
        self._sections = []
        self._has_cover_page = False
        self._has_footer = False


class ReportDirector:
    def __init__(self, builder):
        self._builder = builder

    def construct_full_report(self, client_name, logo, movements, trends,
                             contact):
        return self._builder.add_cover_page(client_name, logo).add_charts(
            "Investment data"
        ).add_recent_movements_table(movements).add_trend_analysis(
            trends).add_footer(contact).build()


if __name__ == '__main__':
    logger.info("=== Generating Custom Report for Client A ===")
    universal_builder = PDFReportBuilder()

    reporte_client_A = universal_builder.add_cover_page("Client A", "logo.png") \
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

    logger.info("=== Example 2 - Builder reused automatically ===")
    report2 = universal_builder.add_cover_page("Client D", "logo2.png") \
        .add_charts("Market data") \
        .add_footer("contact2@advisor.com") \
        .build()
    report2.generate_report()

    logger.info("=== Example 3 - Complex report with same builder ===")
    report3 = universal_builder.add_cover_page("Client E", "logo3.png") \
        .add_charts("Investment performance") \
        .add_recent_movements_table("Recent portfolio changes") \
        .add_trend_analysis("Q4 2025 projections") \
        .add_footer("senior.advisor@company.com") \
        .build()
    report3.generate_report()

    logger.info("=== Example 4 (missing cover page) ===")
    universal_builder.add_footer("contact@advisor.com").build()

    logger.info("=== Example 5 (empty client name) ===")
    universal_builder.add_cover_page("", "logo.png")

    logger.info("=== Example 6 (empty builder) ===")
    universal_builder.build()
