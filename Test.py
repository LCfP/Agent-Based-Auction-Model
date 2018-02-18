from math import floor

production_status = 0
production_rate = 3


hours_in_day = 12
day = 4
storage = 0

for hour in range(hours_in_day * day):
    production_status += production_rate / hours_in_day

    print(production_status, "at hour", hour % hours_in_day, "at day",floor(hour / hours_in_day))

    if production_status >= 1:
        storage += 1
        production_status -= 1
        print("added shipment to storage")

print(storage)




