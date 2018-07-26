#!/usr/bin/env python3

def createEvent (cal,eventData):
   from datetime import datetime
   from icalendar import Event, vCalAddress, vText, Calendar, vDatetime
   import pytz
   correct = "n"
   while correct != 's' :
        event = Event()
        tempCal = Calendar()
        if eventData["summary"] == '':
            eventData["summary"] = "Dummy event" 
        print ("\tGenerando evento <<%s>>...\n" % (eventData["summary"]))
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
        print("La información es correcta?:\n") 
        tempCal.add_component(event)
        displayCal(tempCal)
        correct = input("\n Correcto? s/n: ")
        if correct == "s":
            cal.add_component(event)
   return cal
def displayCal(cal):
   return print(cal.to_ical().decode().replace('\r\n', '\n').strip())  
if __name__ == "__main__":
    from icalendar import Calendar
    import argparse
    import fileinput
    from datetime import datetime
    parser = argparse.ArgumentParser(description="Crea eventos de calendario en formato .ics")
    parser.add_argument("-e","--evento", metavar='EVENT',
                        help="Nombre del evento",default='', dest='event')
    parser.add_argument("-d","--descripcion", metavar='DESCRIPTION',
                        help="Descripcion del evento",default='', dest='descr')                     
    parser.add_argument("-I","--inicio",metavar='DD-MM-YYYY',default=str(datetime.date(datetime.now()).strftime("%d-%m-%Y")),
                        dest='b_date',help="Fecha de inicio", type=str)
    parser.add_argument("-F","--fin",metavar='DD-MM-YYYY',default=str(datetime.date(datetime.now()).strftime("%d-%m-%Y")),
                        dest='e_date',help="Fecha de fin", type=str)
    parser.add_argument("-ti","--tiempo-inicio",metavar='HH:MM',default='00:00',dest='b_hour',help="Hora de inicio", type=str)
    parser.add_argument("-tf","--tiempo-fin",metavar='HH:MM',default='23:59',dest='e_hour',help="Hora de fin", type=str)
    parser.add_argument("-zi","--zona-inicio",metavar='TZ',default='Europe/Brussels',dest='b_tz',help="Zona horaria de inicio", type=str)
    parser.add_argument("-zf","--zona-fin",metavar='TZ',default='Europe/Brussels',dest='e_tz',help="Zona horaria de fin", type=str)
    parser.add_argument("-u","--ubicacion","-l",metavar='LOCATION',default='Antwerp, Belgium',dest='location',help="Ubicacion", type=str)
    parser.add_argument("-o","--organizador",metavar='ORGANIZER',default='sergioachavez@gmail.com',dest='organizer',help="Organizador", type=str)
    parser.add_argument("-n","--nr-events",metavar='NR_EVENTS',default='1',dest='nr_events',help="Número de eventos", type=int)
    parser.add_argument("-f","--archivo","-a",metavar='FILENAME',default='mycal.ics',dest='filename',help="Nombre de archivo", type=str)
        
    args = parser.parse_args()
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
       print ( 'Generando evento %s...' % (args.event))
       cal = createEvent(cal,eventData)  
       f = open(args.filename, 'wb')
    else :
        for i in range(0,args.nr_events):
            print ( '\n====== Generando evento %i de %i ======' % (i+1,args.nr_events))
            eventData["summary"] = input("Nombre del evento: ")
            loc = input("Da la ubicación, ENTER para usar default ("+args.location+")?: ")
            if loc == '':
                eventData["location"] = args.location
            else :
                eventData["location"] = loc
            desc = input("Deseas agregar una descripción? s/n: ")
            if desc == "s":
                eventData["description"] = input("\tDa una descripción: ")
            eventData["organizer"]  = args.organizer
            eventData["BDate"] = input("Da la fecha de inicio DD-MM-AAAA, ENTER para usar el día de hoy ("+args.b_date+"): ")
            if eventData["BDate"] == '':
                eventData["BDate"] = args.b_date
            eventData["BHour"] = input("Da la hora de inicio HH:MM, ENTER para usar default ("+args.b_hour+"): ")
            if eventData["BHour"] == '':
                eventData["BHour"] = args.b_hour
            eventData["Btz"]   = input("Da la zona horaria de inicio, ENTER para usar default ("+args.b_tz+"): ")
            if eventData["Btz"] == '' :
                eventData["Btz"] = args.b_tz
            eventData["EDate"] = input("Da la fecha de fin DD-MM-AAAA, ENTER para usar mismo día que el de inicio ("+eventData["BDate"]+"): ")
            if eventData["EDate"] == '':
                eventData["EDate"] = eventData["BDate"]
            eventData["EHour"] = input("Da la hora de fin HH:MM, ENTER para usar default ("+args.e_hour+"): ")
            if eventData["EHour"] == '':
                eventData["EHour"] = args.e_hour
            eventData["Etz"]   = input("Da la zona horaria de fin, ENTER para usar la misma zona de inicio ("+eventData["Btz"]+"): ")
            if eventData["Etz"] == '' :
                eventData["Etz"] = eventData["Btz"]
            cal = createEvent(cal,eventData)
    f = open(args.filename, 'wb')    
    f.write(cal.to_ical())
    f.close()
    print ('\nArchivo %s generado\n' % (args.filename))
    displayCal(cal)
