from edgar.report.parsers import ReportParser
from edgar.configs import parseOption
import pandas as pd
import xmltodict
from xml.parsers.expat import ExpatError
from xml.etree.ElementTree import ParseError
import logging

log = logging.getLogger(__name__)

class ReportXMLParser(ReportParser):
    def parse(self):
        informationTableStr = self.getInformationTable(
            startKwd=parseOption.report.XML_START_KEYWORD,
            endKwd=parseOption.report.XML_END_KEYWORD,
            startOffset=parseOption.report.XML_START_OFFSET,
            endOffset=parseOption.report.XML_END_OFFSET
        )
        try:
            result = xmltodict.parse(informationTableStr)
            parsedDict = result.get(
                parseOption.report.XML_INFO_TABLE_OUTER_KEYWORD
            ).get(
                parseOption.report.XML_INFO_TABLE_INNER_KEYWORD
            )
            self.parsedData = pd.json_normalize(parsedDict)
            
        except (ExpatError, ParseError) as ex:
            log.warning(f"{ex}. Failed to parse. adsh: {self.adsh}")

        except KeyError as ex:
            log.warning(f"Key {ex} does not exist. adsh: {self.adsh}")
        
