from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
import holidays

@login_required
def agenda(request):
    today = datetime.date.today()
    br_holidays = holidays.Brazil()

    days = []
    for i in range(1, 32):
        try:
            date = datetime.date(today.year, today.month, i)
            name = br_holidays.get(date)
            days.append({
                'day': i,
                'weekday': date.strftime('%A'),
                'holiday': name,
                'is_today': (date == today),
            })
        except:
            continue

    return render(request, 'timeline/agenda.html', {'days': days})