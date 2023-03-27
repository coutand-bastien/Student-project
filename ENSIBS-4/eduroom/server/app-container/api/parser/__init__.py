from api.parser.ICalendarGetter import ICalendarGetter
from api.parser.ICalendarParser import ICalendarParser

url = 'https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=1&calType=ical&firstDate=2022-08-31&lastDate=2023-07-01&resources=6149'

calendar = ICalendarGetter(url, 'api/parser/ics/ensibs.ics')
calendar = ICalendarParser(calendar.get_calendar())
calendar = calendar.parse()