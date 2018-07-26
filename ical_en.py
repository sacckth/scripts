#!/usr/bin/env python3

def createEvent (cal,eventData):
   from datetime import datetime
   from icalendar import Event, vCalAddress, vText, Calendar, vDatetime
   import pytz
   correct = "n"
   while correct != 'y' :
        event = Event()
        tempCal = Calendar()
        if eventData["summary"] == '':
            eventData["summary"] = "Dummy event" 
        print ("\tGenerating event <<%s>>...\n" % (eventData["summary"]))
        bdate=[int(i) for i in eventData["BDate"].split('-')]
        bhour=[int(i) for i in eventData["BHour"].split(':')] 
        edate=[int(i) for i in eventData["EDate"].split('-')]
        ehour=[int(i) for i in eventData["EHour"].split(':')]
        btz = pytz.timezone(eventData["Btz"])
        etz = pytz.timezone(eventData["Etz"])
        event["summary"]   = eventData["summary"]
        event["organizer"] = vCalAddress('MAILTO:'+eventData["organizer"])
        event["dtstart"]   = vDatetime(datetime(bdate[2],bdate[1],bdate[0],bhour[0],bhour[1],0,tzinfo=btz))
        event["dtend"]     = vDatetime(datetime(edate[2],edate[1],edate[0],ehour[0],ehour[1],0,tzinfo=etz))
        event["dtstamp"]   = vDatetime(datetime(bdate[2],bdate[1],bdate[0],bhour[0],bhour[1],0,tzinfo=btz))
        event["location"]  = vText(eventData["location"])
        if eventData["description"] == '':
            event["description"] = vText("XoXo.")
        else:
            event["description"] = vText(eventData["description"])
        event['uid'] = "xOxO-"+str(datetime.timestamp(datetime.now()))+"-XoXo"
        event['priority'] = 5
        print("Verify info:\n") 
        tempCal.add_component(event)
        displayCal(tempCal)
        correct = input("\n Correct? y/n: ")
        if correct == "y":
            cal.add_component(event)
   return cal
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
                        help="Event summary",default='', dest='event')
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
    eventData = {} 
    eventData["summary"]      = args.event
    eventData["location"]     = args.location
    eventData["description"]  = args.descr
    eventData["organizer"]    = args.organizer
    eventData["BDate"]        = args.b_date
    eventData["BHour"]        = args.b_hour
    eventData["Btz"]          = args.b_tz
    eventData["EDate"]        = args.e_date
    eventData["EHour"]        = args.e_hour
    eventData["Etz"]          = args.e_tz
    
    if eventData["BDate"] == '' :
      eventData["BDate"] = str(datetime.date(datetime.now()).strftime("%d-%m-%Y"))
    if eventData["EDate"] == '' :
      eventData["EDate"] = str(datetime.date(datetime.now()).strftime("%d-%m-%Y"))
    if args.nr_events == 1 :
       print ( 'Generanting %s...' % (args.event))
       cal = createEvent(cal,eventData)  
       f = open(args.filename, 'wb')
    else :
        for i in range(0,args.nr_events):
            print ( '\n====== Generating event %i of %i ======' % (i+1,args.nr_events))
            eventData["summary"] = input("Event Summary: ")
            loc = input("Give location, press ENTER to use default ("+args.location+")?: ")
            if loc == '':
                eventData["location"] = args.location
            else :
                eventData["location"] = loc
            desc = input("Do you want to add a description? y/n: ")
            if desc == "y":
                eventData["description"] = input("\tProvide a description: ")
            eventData["organizer"]  = args.organizer
            eventData["BDate"] = input("Give a begin date DD-MM-AAAA, press ENTER to use today's date ("+args.b_date+"): ")
            if eventData["BDate"] == '':
                eventData["BDate"] = args.b_date
            eventData["BHour"] = input("Give begin time HH:MM, press ENTER to use default ("+args.b_hour+"): ")
            if eventData["BHour"] == '':
                eventData["BHour"] = args.b_hour
            eventData["Btz"]   = input("Give begin time zone, press ENTER to use default ("+args.b_tz+"): ")
            if eventData["Btz"] == '' :
                eventData["Btz"] = args.b_tz
            eventData["EDate"] = input("Give end date DD-MM-AAAA, press ENTER to use same as begin date ("+eventData["BDate"]+"): ")
            if eventData["EDate"] == '':
                eventData["EDate"] = eventData["BDate"]
            eventData["EHour"] = input("Give end time HH:MM, press ENTER to use default ("+args.e_hour+"): ")
            if eventData["EHour"] == '':
                eventData["EHour"] = args.e_hour
            eventData["Etz"]   = input("Give end timezone, press ENTER to use same as intial timezone ("+eventData["Btz"]+"): ")
            if eventData["Etz"] == '' :
                eventData["Etz"] = eventData["Btz"]
            cal = createEvent(cal,eventData)
    f = open(args.filename, 'wb')    
    f.write(cal.to_ical())
    f.close()
    print ('\nGenerated %s file\n' % (args.filename))
    displayCal(cal)
