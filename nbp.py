import json
import urllib.request
from calendar import monthrange
from statistics import mean, stdev
import matplotlib.pyplot as plt

# "http://api.nbp.pl/api/exchangerates/rates/A/USD/2020-02-01/2020-02-"+str(days)+"?format=json"

def nbp_in_months(cur, year, month):
    week, days = monthrange(year, int(month))
    adres = "http://api.nbp.pl/api/exchangerates/rates/A/{0}/{3}-{1}-01/{3}-{1}-{2}?format=json".format(cur, month, days, year)
    with urllib.request.urlopen(adres) as url:
        data = json.loads(url.read().decode())
    return data['rates']


def currency_statistics():
    currency = ['usd', 'eur', 'gbp']
    for cur in currency:
        months =['01', '02', '03', '04', '05', '06', '07', '08', '09']
        mids =[]
        max_month = '01'
        max_value = 0
        for month in months:
            rates = nbp_in_months(cur, 2020, month)
            mmax = 0
            mmin = 1000
            for element in rates:
                mid = element['mid']
                mids.append(mid)
                if mid > mmax:
                    mmax = mid
                if mid < mmin :
                    mmin = mid
            diff = mmax - mmin
            if diff > max_value:
                max_month = month
                max_value = diff
        print("Waluta", cur)
        print("Minimum", min(mids))
        print("Maximum", max(mids))
        print("Średnia", mean(mids))
        print("Odchylenie", stdev(mids))
        print("Max month:", max_month, " max value:", max_value)
        print("================")

## WYKRESY
m = '03'
c = 'eur'
y = 2020
rates = nbp_in_months(cur=c,year=y,month=m)
days = [ ]
mids = []
for el in rates:
    days.append(int(el["effectiveDate"][-2:]))   #slices w pythonie działa na listach i stringach
    mids.append(el['mid'])
print(days)
print(mids)
plt.plot(days, mids)
plt.xlabel("Dzień miesiąca")
plt.ylabel("Kurs "+c)
#plt.show()
plt.savefig("kurs.jpg")