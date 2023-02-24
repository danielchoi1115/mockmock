
from pydantic import BaseModel
from pandas import DataFrame
from datetime import datetime
import logging

log = logging.getLogger(__name__)

class ReportParser(BaseModel):
    reportRaw: str
    adsh: str
    reportDate: datetime
    parsedData: DataFrame | None = None

    date_format: str = "%Y%m%d"

    class Config:
        arbitrary_types_allowed = True

    def getParsedReportDate(self):
        start_kwd = "CONFORMED PERIOD OF REPORT:"
        end_kwd = "FILED AS OF DATE:"
        start = self.reportRaw.find(start_kwd) + len(start_kwd)
        end = self.reportRaw.find(end_kwd)
        dateStr = self.reportRaw[start:end].strip()
        
        try:
            return datetime.strptime(dateStr, self.date_format)
        except ValueError as e:
            log.warning(f"{e}, {dateStr} is not a proper date")

    def getInformationTable(
        self,
        startKwd: str,
        endKwd: str,
        startOffset: int,
        endOffset: int
    ) -> str:
        """_summary_

        Args:
            startKwd (str): a string that indicates the start of an information table
            endKwd (str): a string that indicates the end of an information table
            startOffset (int): offset value after the start keyword. Used to ignore unnecessary element such as headers
            endOffset (int): offset value after the end keyword.

        Returns:
            List[str]: A list containing each lines 
        """
        startIdx = self.reportRaw.find(startKwd) + startOffset
        endIdx = self.reportRaw.find(endKwd) + endOffset

        if startIdx == -1 or endIdx == -1:
            ex = ValueError("Information Table not Found.")
            log.warning(f"{ex} adsh: {self.adsh}, startIdx: {startIdx}, endIdx: {endIdx}")
        return self.reportRaw[startIdx:endIdx]

    def parse(self):
        ...

    def postProcess(self):
        self.parsedData.rename(columns={'shrsOrPrnAmt.sshPrnamt': 'shrsOrPrn.Amt'}, inplace=True)
        self.parsedData.rename(columns={'shrsOrPrnAmt.sshPrnamtType': 'shrsOrPrn.Type'}, inplace=True)
        self.parsedData.rename(columns={'votingAuthority.Sole': 'votingAuth.Sole'}, inplace=True)
        self.parsedData.rename(columns={'votingAuthority.Shared': 'votingAuth.Shared'}, inplace=True)
        self.parsedData.rename(columns={'votingAuthority.None': 'votingAuth.None'}, inplace=True)
        
        try:
            for k in ['value', 'shrsOrPrn.Amt', 'votingAuth.Sole', 'votingAuth.Shared', 'votingAuth.None']:
                self.parsedData[k] = self.parsedData[k].astype(int)
        except Exception as ex:
            print(k)
            print(ex)
