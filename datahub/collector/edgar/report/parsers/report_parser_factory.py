
from report.parsers import ReportTableParser, ReportXMLParser, ReportParser
from typing import Type
from accession import Accession


class ReportParserFactory:
    @staticmethod
    def getParserType(reportRaw: str) -> Type[ReportParser]:
        if "<TABLE>" in reportRaw:
            return ReportTableParser
        elif "<XML>" in reportRaw:
            return ReportXMLParser

    @staticmethod
    def getParser(
        parserClass: ReportParser,
        reportRaw: str,
        accesion: Accession
    ) -> ReportParser:

        return parserClass(
            reportRaw=reportRaw,
            adsh=accesion.adsh,
            reportDate=accesion.reportDate
        )

    @staticmethod
    def getParserOf(reportRaw: str, accesion: Accession) -> ReportParser:
        cls = ReportParserFactory.getParserType(reportRaw)
        return ReportParserFactory.getParser(
            parserClass=cls,
            reportRaw=reportRaw,
            accesion=accesion
        )
