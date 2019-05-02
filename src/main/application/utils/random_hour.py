from random import randint

def getRandomTime():
    hour=randint(8,24)
    minute=0 #randint(1,4)*15%60

    if (minute==0):
        minute="00"

    if (hour<10):
        hour="0"+str(hour)

    return str(hour) + ":" + str(minute)

#print(getRandomTime())

def getDuration(start,end):
    start_hours, start_minutes = start.split(':')
    end_hours, end_minutes = end.split(':')

    if(start_hours>end_hours):
        start_hours,end_hours=end_hours,start_hours
        start_minutes,end_minutes=end_minutes,start_minutes
    if (start_hours == end_hours):
        start_minutes,end_minutes=end_minutes,start_minutes

    duration_minutes=(int(end_hours) * 60 + int(end_minutes))-(int(start_hours) * 60 + int(start_minutes))

    return str(duration_minutes//60)

#print(getDuration(getRandomTime(),getRandomTime()))