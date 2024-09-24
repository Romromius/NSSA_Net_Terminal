import datetime
b = datetime.datetime.now()
b = b.replace(year=1)
a = 0
a += b.month * 30 * 24 * 60 * 60
a += b.day * 24 * 60 * 60
a += b.hour * 60 * 60
a += b.minute * 60
a += b.second

print(a)