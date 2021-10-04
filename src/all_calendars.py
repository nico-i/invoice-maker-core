from cal_setup import get_calendar_service

service = get_calendar_service()
# Call the Calendar API
print('Getting list of calendars')
calendars_result = service.calendarList().list().execute()

calendars = calendars_result.get('items', [])

if not calendars:
    print('No calendars found.')
for calendar in calendars:
    summary = calendar['summary']
    cal_id = calendar['id']
    primary = "Primary" if calendar.get('primary') else ""
    print("%s\t%s\t%s" % (summary, cal_id, primary))