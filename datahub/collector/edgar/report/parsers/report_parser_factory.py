
from edgar.report import parsers
from typing import Type
from edgar.accession import Accession


class ReportParserFactory:
    @staticmethod
    def getParserType(reportRaw: str) -> Type[parsers.ReportParser]:
        if "<TABLE>" in reportRaw:
            return parsers.ReportTableParser
        elif "<XML>" in reportRaw:
            return parsers.ReportXMLParser

    @staticmethod
    def getParser(
        parserClass: parsers.ReportParser,
        reportRaw: str,
        accesion: Accession
    ) -> parsers.ReportParser:

        return parserClass(
            reportRaw=reportRaw,
            adsh=accesion.adsh,
            reportDate=accesion.reportDate
        )

    @staticmethod
    def getParserOf(reportRaw: str, accesion: Accession) -> parsers.ReportParser:
        cls = ReportParserFactory.getParserType(reportRaw)
        return ReportParserFactory.getParser(
            parserClass=cls,
            reportRaw=reportRaw,
            accesion=accesion
        )
