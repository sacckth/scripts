#!/usr/bin/env python3
def compute_time(ehour0,ehour1,bhour0,bhour1,days):
    from datetime import timedelta
    delta=timedelta(days=days,hours=ehour0,minutes=ehour1) - timedelta(hours=bhour0,minutes=bhour1)
    # returns the value in hours 
    return float(delta.seconds)/3600
def parse_params(args):
    fixed = {'start':{'deposit':150,'monthly':4.00,'reg_fee':35,'dom':-1},
             'bonus':{'deposit':500,'monthly':8.00,'reg_fee':35,'dom':-1}, 
           'comfort':{'deposit':500,'monthly':22.0,'reg_fee':35,'dom':-1}}
    tariffs = { 'start' : 
                 {'s': {'hourly_day':2.00,'hourly_night':0.0,'daily':23.00,'weekly':140,'km_100':0.36,'km_101':0.24},
                  'm': {'hourly_day':2.55,'hourly_night':0.0,'daily':30.00,'weekly':180,'km_100':0.37,'km_101':0.25},
                  'l': {'hourly_day':3.10,'hourly_night':0.0,'daily':36.50,'weekly':220,'km_100':0.39,'km_101':0.25},
                 'xl': {'hourly_day':4.20,'hourly_night':0.0,'daily':42.00,'weekly':250,'km_100':0.44,'km_101':0.29}},
                'bonus' : 
                 {'s': {'hourly_day':1.75,'hourly_night':0.0,'daily':21.00,'weekly':125,'km_100':0.27,'km_101':0.23},
                  'm': {'hourly_day':2.10,'hourly_night':0.0,'daily':25.00,'weekly':145,'km_100':0.28,'km_101':0.24},
                  'l': {'hourly_day':2.45,'hourly_night':0.0,'daily':29.00,'weekly':170,'km_100':0.34,'km_101':0.24},
                 'xl': {'hourly_day':3.55,'hourly_night':0.0,'daily':35.00,'weekly':210,'km_100':0.39,'km_101':0.28}},
                'comfort' : 
                 {'s': {'hourly_day':1.55,'hourly_night':0.0,'daily':17.50,'weekly':105,'km_100':0.24,'km_101':0.19},
                  'm': {'hourly_day':1.90,'hourly_night':0.0,'daily':22.00,'weekly':132,'km_100':0.25,'km_101':0.20},
                  'l': {'hourly_day':2.20,'hourly_night':0.0,'daily':26.50,'weekly':158,'km_100':0.26,'km_101':0.20},
                 'xl': {'hourly_day':2.85,'hourly_night':0.0,'daily':28.50,'weekly':170,'km_100':0.32,'km_101':0.24}}
              }
    tdata = {}
    tdata["days"]   = float(args.days)
    tdata["begin_hour"] = args.b_hour
    tdata["end_hour"]   = args.e_hour
    hours = args.hours
    hoursT = 0
    fare = args.fare
    car_size = args.car_size
    distance = float(args.distance)
    bhour=[int(i) for i in tdata["begin_hour"].split(':')] 
    ehour=[int(i) for i in tdata["end_hour"].split(':')]
    
    if distance < 100:
        dFare = distance * tariffs[fare][car_size]['km_100']
    else:
        deltaD = distance - 100
        dFare = (deltaD * tariffs[fare][car_size]['km_101']) + (100 * tariffs[fare][car_size]['km_100'])
    weeks = 0
    
    if tdata['days'] == 0:
        # early morning hours
        if bhour[0] < 7 :
           bhourD = 7
        # regular hours
        else:
           bhourD = bhour[0]
        # overnight stays
        if ehour[0] <= bhour[0] :
           if hours != 0 :
              hoursT = hours
           else: 
              hoursT = compute_time(ehour[0],ehour[1],bhourD,bhour[1],1)
        else:
           if hours != 0 :
              hoursT = hours
           else: 
              hoursT = compute_time(ehour[0],ehour[1],bhourD,bhour[1],0)          
        tFare = hoursT * tariffs[fare][car_size]['hourly_day']
    elif tdata['days'] > 0  and tdata['days'] < 7: 
        tFare = tdata['days'] * tariffs[fare][car_size]['daily']
    else:
        weeks = tdata['days'] / 7
        tFare = weeks * tariffs[fare][car_size]['weekly']
    tdata['hoursT'] = hoursT
    tdata['tFare'] = tFare
    tdata['dFare'] = dFare
    tdata['weeks'] = weeks
    return tdata
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Calculate CAMBIO car costs")
    parser.add_argument("-t","--tariff", metavar='SUB_TYPE',help="start, bonus or comfort",default='bonus', dest='fare', type=str)
    parser.add_argument("-D","--days", metavar='NR_OF_DAYS',help="Trips longer than 24 hours", default=0, dest='days')
    parser.add_argument("-H","--hours", metavar='NR_OF_HOURS',help="Instead of -b and -e", default=0, dest='hours', type=float)
    parser.add_argument("-d","--distance", metavar='DIST_KM',help="Distance in Km", default=0, dest='distance')            
    parser.add_argument("-b","--begin-time",metavar='HH:MM',default='07:00',dest='b_hour',help="Begin of journey", type=str)
    parser.add_argument("-e","--end-time",metavar='HH:MM',default='23:00',dest='e_hour',help="End of journey", type=str)
    parser.add_argument("-s","--size",metavar='CAR_SIZE',default='s',dest='car_size',help="s, m , l or xl", type=str)
    args = parser.parse_args()
    tdata=parse_params(args)
    print("*---------------------*")
    print("\tSUMMARY: for \"%s\" car with \"%s\" fare" % (args.car_size,args.fare) )
    print("\tDistance: %.2f km"  % float(args.distance) )
    print("\tTotal Hours: %.2f" % (tdata['hoursT']) )
    print("\tTotal Days: %.2f" % (tdata['days']) )
    print("\tTotal Weeks: %.2f" % (tdata['weeks']) )
     
    print("*---------------------*")
    print("\tDistance Fare: %.2f EUR " % (tdata['dFare']) )
    print("\tTime Fare: %.2f EUR"  % (tdata['tFare']) )
    print("\tTotal: %.2f EUR" % (tdata['dFare']+tdata['tFare']) )
    
