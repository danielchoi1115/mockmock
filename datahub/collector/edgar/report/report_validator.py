from .parsers import ReportParser
import logging

log = logging.getLogger(__name__)

class ReportValidator:
    def validateParsedData(self, reportParser: ReportParser):
        self.validateParsedDate(reportParser)
        ...
        self.validateTableEntries(reportParser)

    def validateParsedDate(self, reportParser: ReportParser):
        parsedDate = reportParser.getParsedReportDate()
        if parsedDate != reportParser.reportDate:
            ex = ValueError("Report Date unmatch.")
            log.warning(f"{ex} adsh: {reportParser.adsh}, parsedDate: {parsedDate}, scrappedDate: {reportParser.reportDate}")
            raise ex

    def validateTableEntries(self, reportParser: ReportParser):
        try:
            self.checkHasAllKeys(reportParser)
            self.checkTypes(reportParser)
            self.hasCorrectValues(reportParser)
            # {
            #     'nameOfIssuer': '111 INC',
            #     'titleOfClass': 'ADS',
            #     'cusip': '68247Q102',
            #     'value': '336',
            #     'shrsOrPrnAmt': {
            #         'sshPrnamt': '111347',
            #         'sshPrnamtType': 'SH'
            #     },
            #     'investmentDiscretion': 'SOLE',
            #     'otherManager': '0',
            #     'votingAuthority': {
            #         'Sole': '111347',
            #         'Shared': '0',
            #         'None': '0'
            #     }
            # }
        except:
            ...

    def checkHasAllKeys(self, reportParser: ReportParser):
        keyList = [
            'nameOfIssuer',
            'titleOfClass',
            'cusip',
            'value',
            'shrsOrPrnAmt.sshPrnamt',
            'shrsOrPrnAmt.sshPrnamtType',
            'investmentDiscretion',
            'otherManager',
            'votingAuthority.Sole',
            'votingAuthority.Shared',
            'votingAuthority.None'
        ]
        parsedKeys = set(reportParser.parsedData.keys())
        for key in keyList:
            if key not in parsedKeys:
                raise KeyError(f"key `{key}` does not exist")

    def checkTypes(self, reportParser: ReportParser):
        try:
            reportParser.parsedData['cusip'] = reportParser.parsedData['cusip'].astype(int)
        except Exception as ex:
            print(ex)

    def hasCorrectValues(self, ereportParser: ReportParser):
        ...
        # if entry.get('titleOfClass').upper() not in {'COM', 'COM CL A', 'COM CL B', 'COM CL C', 'CL A', 'CL B', 'CL C', 'ADS'}:
        #     return False


reportValidator = ReportValidator()
