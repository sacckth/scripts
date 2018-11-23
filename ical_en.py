#!/usr/bin/env python3

def createEvent (cal,args):
    from datetime import datetime
    from icalendar import Event, vCalAddress, vText, vDatetime
    import pytz
    for i in range(0,args.nr_events):
        print ("\tGenerating event %i of %i...\n" % (i+1,args.nr_events))
        eventData = getEventData(args)
        event = Event()
        bdate=[int(i) for i in eventData["begin_date"].split('-')]
        bhour=[int(i) for i in eventData["begin_hour"].split(':')] 
        edate=[int(i) for i in eventData["end_date"].split('-')]
        ehour=[int(i) for i in eventData["end_hour"].split(':')]
        btz = pytz.timezone(eventData["begin_timezone"])
        etz = pytz.timezone(eventData["end_timezone"])
        event["summary"]   = eventData["summary"]
        event["organizer"] = vCalAddress('MAILTO:'+eventData["organizer"])
        event["dtstart"]   = vDatetime(datetime(bdate[2],bdate[1],bdate[0],bhour[0],bhour[1],0,tzinfo=btz))
        event["dtend"]     = vDatetime(datetime(edate[2],edate[1],edate[0],ehour[0],ehour[1],0,tzinfo=etz))
        event["dtstamp"]   = vDatetime(datetime(bdate[2],bdate[1],bdate[0],bhour[0],bhour[1],0,tzinfo=btz))
        event["location"]  = vText(eventData["location"])
        event["description"] = vText(eventData["description"])
        event['uid'] = "xOxO-"+str(datetime.timestamp(datetime.now()))+"-XoXo"
        event['priority'] = 5
        cal.add_component(event)
    return cal
def displayInput(eventData) :
    correct = "n"
    for key, value in eventData.items() :
        print ("%s: %s" % (str(key),str(value)) )
    correct = input ("Is this information correct? y/n: " )    
    return correct
def getEventData(args):
    eventData = {} 
    eventData["summary"]           = args.event
    eventData["location"]          = args.location
    eventData["description"]       = args.descr
    eventData["organizer"]         = args.organizer
    eventData["begin_date"]        = args.b_date
    eventData["begin_hour"]        = args.b_hour
    eventData["begin_timezone"]    = args.b_tz
    eventData["end_date"]          = args.e_date
    eventData["end_hour"]          = args.e_hour
    eventData["end_timezone"]      = args.e_tz
    if args.nr_events == 1 :
       print ( 'Generanting event %s...' % (args.event))
       return eventData
    else :
        correct = "n"
        while correct != 'y' :
            print ( '\n===============================================')
            eventData["summary"] = input("Event Summary: ")
            loc = input("Give location, press ENTER to use default ("+eventData["location"]+")?: ")
            if loc != '':
                eventData["location"] = loc
            desc = input("Do you want to add a description? y/n: ")
            if desc == "y":
                eventData["description"] = input("\tProvide a description: ")
            else :
                eventData["description"] = "XoXo."
            bdate = input("Give a begin date DD-MM-AAAA, press ENTER to use today's date ("+args.b_date+"): ")
            if bdate == '':
                eventData["begin_date"] = args.b_date
            else : 
                eventData["begin_date"] = bdate
            bhour = input("Give begin time HH:MM, press ENTER to use default ("+args.b_hour+"): ")
            if bhour == '':
                eventData["begin_hour"] = args.b_hour
            else :
                eventData["begin_hour"] = bhour
            btz   = input("Give begin time zone, press ENTER to use default ("+args.b_tz+"): ")
            if btz == '' :
                eventData["begin_timezone"] = args.b_tz
            else :
                eventData["begin_timezone"] = btz
            edate = input("Give end date DD-MM-AAAA, press ENTER to use same as begin date ("+eventData["begin_date"]+"): ")
            if edate == '':
                eventData["end_date"] = eventData["begin_date"]
            else :
                eventData["end_date"] = edate
            ehour = input("Give end time HH:MM, press ENTER to use default ("+args.e_hour+"): ")
            if ehour == '':
                eventData["end_hour"] = args.e_hour
            else :
                eventData["end_hour"] = ehour
            etz  = input("Give end timezone, press ENTER to use same as intial timezone ("+eventData["begin_timezone"]+"): ")
            if etz == '' :
                eventData["end_timezone"] = eventData["begin_timezone"]
            else :
                eventData["end_timezone"] = etz
            correct = displayInput(eventData)
    return eventData

def displayCal(cal):
   return print(cal.to_ical().decode().replace('\r\n', '\n').strip())
if __name__ == "__main__":
    from icalendar import Calendar
    import argparse
    import fileinput
    import pytz
    from datetime import datetime
    parser = argparse.ArgumentParser(description="Create .ics cal events")
    parser.add_argument("-e","--event", metavar='EVENT',
                        help="Event summary",default='Dummy Event', dest='event')
    parser.add_argument("-d","--description", metavar='DESCRIPTION',
                        help="Event description",default='', dest='descr')                     
    parser.add_argument("-B","--begin",metavar='DD-MM-YYYY',default=str(datetime.date(datetime.now()).strftime("%d-%m-%Y")),
                        dest='b_date',help="Begin date", type=str)
    parser.add_argument("-E","--end",metavar='DD-MM-YYYY',default=str(datetime.date(datetime.now()).strftime("%d-%m-%Y")),
                        dest='e_date',help="End date", type=str)
    parser.add_argument("-t","--begin-time",metavar='HH:MM',default='00:00',dest='b_hour',help="Begin of event", type=str)
    parser.add_argument("-T","--end-time",metavar='HH:MM',default='23:59',dest='e_hour',help="End of event", type=str)
    parser.add_argument("-bz","--begin-timezone",metavar='TZ',default='Europe/Brussels',dest='b_tz',help="Timezone begin of event", type=str)
    parser.add_argument("-ez","--end-timezone",metavar='TZ',default='Europe/Brussels',dest='e_tz',help="Timexone end of event", type=str)
    parser.add_argument("-l","--location",metavar='LOCATION',default='Antwerp, Belgium',dest='location',help="Location", type=str)
    parser.add_argument("-o","--organizer",metavar='ORGANIZER',default='sergioachavez@gmail.com',dest='organizer',help="Organizer", type=str)
    parser.add_argument("-n","--nr-events",metavar='NR_EVENTS',default='1',dest='nr_events',help="Number of events", type=int)
    parser.add_argument("-f","--file",metavar='FILENAME',default='mycal.ics',dest='filename',help="Filename with .ics extension", type=str)
    parser.add_argument("-Z","--display-timezone",action='store_true',dest='dt')
        
    args = parser.parse_args()
    if args.dt:
        print  ("[" + ", ".join( str(x) for x in pytz.all_timezones) + "]")
        exit()
    cal = Calendar()
    cal.add('prodid', '-//My calendar//Sergio//')
    cal.add('version', '1.0')
    cal.add('calscale',"GREGORIAN")
    cal = createEvent(cal,args)
    f = open(args.filename, 'wb')    
    f.write(cal.to_ical())
    f.close()
    print ('\nGenerated %s file\n' % (args.filename))
    displayCal(cal)