from . import ReportParser
from typing import List, Dict, Tuple
from edgar.configs import parseOption
import pandas as pd
from io import StringIO
import logging

log = logging.getLogger(__name__)

class ReportTableParser(ReportParser):
    reportRaw: str | None = None
    
    # 'nameOfIssuer',
    # 'titleOfClass',
    # 'cusip',
    # 'value',
    # 'shrsOrPrn.Amt',
    # 'shrsOrPrn.Type',
    # 'investmentDiscretion',
    # 'otherManager',
    # 'votingAuth.Sole',
    # 'votingAuth.Shared',
    # 'votingAuth.None'
    
    headerMapper: Dict = {
        'nameofissuer': 'nameOfIssuer',
        'titleofclass': 'titleOfClass',
        'cusip': 'cusip',
        'value(x$1000)': 'value',
        'shares/prnamt': 'shrsOrPrn.Amt',
        'sh/prn': 'shrsOrPrn.Type',
        'put/call': 'putCall',
        'invstmtdscretn': 'investmentDiscretion',
        'othermanagers': 'otherManager',
        'sole': 'votingAuth.Sole',
        'shared': 'votingAuth.Shared',
        'none': 'votingAuth.None'
    }
    
    def getInformationTable(
        self,
        startKwd: str,
        endKwd: str,
        startOffset: int,
        endOffset: int
    ) -> List[str]:
        startIdx, endIdx = -1, -1
        reportRaw = self.reportRaw.split('\n')
        for index, line in enumerate(reportRaw):
            if line.strip().upper() == startKwd:
                startIdx = index + startOffset
            elif line.strip().upper() == endKwd:
                endIdx = index + endOffset

        if startIdx == -1 or endIdx == -1:
            ex = ValueError("Information Table not Found. Unable to parse data. Please fix the parser")

        return reportRaw[startIdx:endIdx]

    def getColSpecs(self, infoTable: List[str]):
        columnIndicator = infoTable[4]
        colspecs = []
        start = 0
        while start < len(columnIndicator):
            offset = columnIndicator[start+1:].find("<C>")
            if offset == -1:
                colspecs.append((start, self.getMaxLen(infoTable)))
                break
            colspecs.append((start,start+offset+1))
            start += offset+1
        return colspecs
    
    def getMaxLen(self, infoTable):
        limit = min(10, len(infoTable))
        return len(max(infoTable[:limit]))
        
    def getHeaders(self, infoTable: List[str], colspecs: List[Tuple[int, int]]):
        # We need to convert the following header string

        # """                                                   VALUE   SHARES/  SH/ PUT/ INVSTMT    OTHER          VOTING AUTHORITY
        #    NAME OF ISSUER         TITLE OF CLASS     CUSIP   (x$1000) PRN AMT  PRN CALL DSCRETN   MANAGERS     SOLE    SHARED    NONE """

        # into headers = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'shrsOrPrn.Amt', 'shrsOrPrn.Type', 'investmentDiscretion', 'otherManager', 'votingAuth.Sole', 'votingAuth.Shared', 'votingAuth.None']

        # VOTING AUTHORITY is a Larger Category which is not needed.
        upper_header=infoTable[1].replace("VOTING AUTHORITY","")
        lower_header=infoTable[2]
        headersRaw = [
            (upper_header[sp[0] : sp[1]].strip()
            + lower_header[sp[0] : sp[1]].strip()).replace(" ", "").lower()
            for sp in colspecs
        ]
        headers = []
        for h in headersRaw:
            header = self.headerMapper.get(h)
            if header is None:
                log.warning(f"failed to parse {headersRaw}")
                return []
            headers.append(header)
        return headers
            

    def parse(self):
        infoTable = self.getInformationTable(
            startKwd=parseOption.report.TABLE_START_KEYWORD,
            startOffset=parseOption.report.TABLE_START_OFFSET,
            endKwd=parseOption.report.TABLE_END_KEYWORD,
            endOffset=parseOption.report.TABLE_END_OFFSET
        )
        
        colspecs = self.getColSpecs(infoTable=infoTable)
        headers = self.getHeaders(
            infoTable=infoTable,
            colspecs=colspecs
        )
        
        self.parsedData = pd.read_fwf(StringIO("\n".join(infoTable[5:])), colspecs=colspecs, names=headers)
        
        
        