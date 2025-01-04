from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import sys, subprocess

def main():
    date = datetime.strptime(input("Please enter the start date 'YYYY-MM-DD' format: "), "%Y-%m-%d")
    
    month = int(input("Please enter how many months: "))
    future_month = future_date(date, month)
    months_difference = remaining_months(future_month)
    remainingdays = remaining_days(months_difference, future_month)
    
    date1 = datetime.strftime(date, "%B %d, %Y")
    result1 = datetime.strftime(future_month, "%B %d, %Y")
    print(f"\nThe contract started on {date1} after {month} month is: {result1}")
    
    print(f"The contract left: {months_difference} month (includes current month) and {remainingdays} days\n\n")

    ETF = input("Do you wish to calculate the possible ETF? Y/N: ").lower()
    if ETF == "y":
        amount1 = 0.00
        amount = float(input("How much is the contract amount?: "))
        indicator = input("Is the next months bill generated? Y/N: ").lower()
        amount1 = float(input("How much is the outstanding balance? 'if paid put 0': "))
        day_etf = etf_calculator_day(future_month, amount)
        notice = day_notice(amount)
        etf = etf_calculator_month(future_month, months_difference, amount1, amount, day_etf, notice,indicator)
        if etf[0] == etf[1]:
            print(f"\n\nThe final bill is: {etf[1]}")
            print(f"30 day Notice: {etf[2]}\n\n")
        else:
            print(f"\n\nThe final bill is: {etf[0]}")
            print(f"30 day Notice: {etf[2]}\n\n")
    else:
        print("Thank you for using the program\n\n")
    
    R = input("Rerun the program? Y/N: ").lower()

    if R == "y":
        subprocess.run('cls', shell=True)
        main()


#This function will return the future date with param of start date and the months
def future_date(start_date, month):
    #This code will compute the futer months base on the month user input    
    future_date = start_date + relativedelta(months =+ month, days =- 1)
    #returning the the future date    
    return future_date

def remaining_months(futuredate):
    today = datetime.today()
    if futuredate.year >= today.year:
        if futuredate.month > today.month:
            return (futuredate.year - today.year) * 12 + (futuredate.month - today.month)
        else:
            return 0
    else:
        return 0

def remaining_days(month_result, future_date):
    if month_result <= 1:
        return 0
    else:
        return future_date.day

def etf_calculator_month(future, result, amount1, amount, day, notice, indicator):
    today = datetime.today()
    if future.year >= today.year:
        if future.month > today.month:
            if indicator == 'y':
                current_bill_N = round((result - 2) * amount + amount1 + day, 2)
                current_bill_Y = round((result - 1) * amount + day, 2)
                notice = "Still in a contract"
                return current_bill_N, current_bill_Y, notice
            else:
                current_bill_N = round((result - 1) * amount + amount1 + day, 2)
                current_bill_Y = round((result - 1) * amount + day, 2)
                notice = "Still in a contract"
                return current_bill_N, current_bill_Y, notice
        else:
            current_bill_N = round(amount1 + notice, 2)
            current_bill_Y = round(notice, 2)
            notice = round(amount1 + notice, 2)
            return current_bill_N, current_bill_Y, notice
    else:
        current_bill_N = round(amount1 + notice, 2)
        current_bill_Y = round(notice, 2)
        notice = round(amount1 + notice, 2)
        return current_bill_N, current_bill_Y, notice

def etf_calculator_day(result, amount):
    day = result + relativedelta(days =+ 1)
    if day.day == 1:
        return round(amount, 2)
    else:
        num_days = calendar.monthrange(result.year, result.month)[1]
        per_day = amount / num_days
        return round(result.day * per_day, 2)
        
def day_notice(amount):
    today = datetime.today()
    per_day = amount / 30
    notice = today + relativedelta(days =+ 30)
    return round(notice.day * per_day, 2)

if __name__ == "__main__":
    main()
