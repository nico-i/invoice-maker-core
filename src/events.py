import io
from datetime import datetime


def get_events(service, cal_id, start_date, end_date):
    tfformat = '%Y-%m-%dT%H:%M:%S.000000Z'
    print('2. Getting List of events from the ' + start_date.strftime(
        '%d.%m.%y at %H:%M') + ' to the ' + end_date.strftime('%d.%m.%y at %H:%M')+'.')
    events_result = service.events().list(
        calendarId=cal_id, timeMin=start_date.strftime(tfformat), timeMax=end_date.strftime(tfformat),
        maxResults=200, singleEvents=True,
        orderBy='startTime').execute()
    all_events = events_result.get('items', [])
    events = []
    if not all_events:
        print('3. No events found.')
    else:
        for event in all_events:
            tpformat = '%Y-%m-%dT%H:%M:%S%z'
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            event_date = ''
            if(len(start) == 10):
                tpformat =  "%Y-%m-%d"
            event_date = datetime.strptime(start, tpformat).strftime('%d.%m.%y')
            duration = (datetime.strptime(end, tpformat) -
                        datetime.strptime(start, tpformat)).total_seconds() / 3600
            duration_str = datetime.strptime(start, tpformat).strftime(
                '%H:%M') + '–' + datetime.strptime(end, tpformat).strftime('%H:%M')

            events.append(
                (event_date, duration_str, event['summary'], duration))
    return events
