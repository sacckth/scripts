#!/usr/bin/env python3
def compute_days(y,m,d,bdate):
    import datetime
    if bdate == '':
        b_date=datetime.datetime.date(datetime.datetime.now())
    else :
        b_date = bdate.split('-')
        b_date = datetime.date(int(b_date[2]),int(b_date[1]),int(b_date[0]))
    target=datetime.date(y,m,d)
    delta=(target - b_date)
    return int(delta.days)


if __name__ == "__main__":
    import argparse
    import datetime
    year=datetime.datetime.now().year
    parser = argparse.ArgumentParser(description="Calcula el número de días restantes/desde la fecha actual o fecha base a una fecha objetivo (fecha por defecto: 13-03-"+str(year)+")")
    parser.add_argument("-d","--dia","--day", metavar='DD', type=int,
                        help="día objetivo", default=13, dest='d')
    parser.add_argument("-m","--month","--mes", metavar='MM', type=int,
                        help="Mes objetivo", default=3, dest='m')
    parser.add_argument("-y","--year","--año","-a", metavar='YYYY', type=int,
                        help="Año objetivo",default=int(year), dest='y')
    parser.add_argument("-e","--event","--evento", metavar='EVENT',
                        help="Nombre del evento",default='', dest='event')
    parser.add_argument("-fo",metavar='DD-MM-YYYY',default='',dest='o_date',help="Fecha objetivo compacta", type=str)
    parser.add_argument("-fb",metavar='DD-MM-YYYY',default='',dest='b_date',help="Fecha base compacta", type=str)
    
    args = parser.parse_args()
    if args.o_date != '' :
       fo = args.o_date.split('-')
       d = int(fo[0])
       m = int(fo[1])
       y = int(fo[2])
    else :
       d = args.d
       m = args.m
       y = args.y

    if args.b_date == '':
       ref = '.'
    else :
       ref = " (ref. "+args.b_date+")."    
    days=compute_days(y, m, d, args.b_date)
    meses = {1:'enero',2:'febrero',3:'marzo',4:'abril',5:'mayo',6:'junio',7:'julio',8:'agosto',9:'septiembre',10:'octubre',11:'noviembre',12:'diciembre'}
    if days > 0:
        if args.event == '':
            print ( '%d días restantes para el %d de %s de %d%s' % (days,d,meses[m],y,ref))
        else:
            print ( "%d días restantes para %s%s" % (days,args.event,ref) )
    else:
         if args.event == '':
            print ( '%d días desde el %d de %s de %d%s' % (abs(days),d,meses[m],y,ref))
         else:
            print ( "%d días desde %s%s" % (abs(days),args.event,ref) )
