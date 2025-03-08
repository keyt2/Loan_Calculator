import math
import argparse

# Argument parser setup
parser = argparse.ArgumentParser()
parser.add_argument("--payment", type=float, help="Enter the monthly payment")
parser.add_argument("--principal", type=int, help="Enter the loan principal")
parser.add_argument("--periods", type=int, help="Enter the number of months")
parser.add_argument("--interest", type=float, help="Enter the interest rate")
parser.add_argument("--type", type=str, help="Enter the type of payment")

args = parser.parse_args()

# Calculate nominal monthly interest rate
if  args.interest is not None:
    nominal_interest_rate = args.interest / (12 * 100)

# Annuity calculations
if args.type == "annuity":
    # Case where payment is not provided, but principal, periods, and interest are given
    if args.payment is None and args.principal is not None and args.periods is not None and args.interest is not None:
        if (args.principal < 0 or args.periods < 0 or args.interest < 0):
            print("Incorrect parameters.")
        else:
            # Annuity payment formula
            payment = math.ceil(args.principal * (nominal_interest_rate * math.pow((1 + nominal_interest_rate), args.periods)) / 
                                (math.pow((1 + nominal_interest_rate), args.periods) - 1))
            
            # Calculate overpayment
            total_paid = payment * args.periods
            overpayment = total_paid - args.principal
            print(f"Your monthly payment = {payment}!")
    
            # Print overpayment
            print(f"Overpayment = {overpayment}")

    # Case where principal is not provided, but payment, periods, and interest are given
    elif args.principal is None and args.payment is not None and args.periods is not None and args.interest is not None:
        if  (args.payment < 0 or args.periods < 0 or args.interest < 0):
            print("Incorrect parameters.")
        else:
            principal = math.floor(args.payment / ((nominal_interest_rate * math.pow((1 + nominal_interest_rate), args.periods)) / 
                                                   (math.pow((1 + nominal_interest_rate), args.periods) - 1)))
            print(f"Your loan principal = {principal}!")
            print(f"Overpayment = {args.payment * args.periods - principal}")

    # Case where periods are not provided, but payment, principal, and interest are given
    elif args.periods is None and args.payment is not None and args.principal is not None and args.interest is not None:
        if (args.payment < 0 or args.principal < 0 or args.interest < 0):
            print("Incorrect parameters.")
        else:
            periods = math.ceil(math.log(args.payment / (args.payment - nominal_interest_rate * args.principal), 1 + nominal_interest_rate))
            years = periods // 12
            months = periods % 12
            if months != 0:
                print(f"It will take {years} years and {months} months to repay this loan!")
            else:
                print(f"It will take {years} years to repay this loan!")
            
            # Calculate overpayment
            overpayment = args.payment * periods - args.principal
            print(f"Overpayment = {overpayment}")

    else:
        print("Incorrect parameters.")

# Differentiated payments (diff) calculations
elif args.type == "diff" and args.interest is not None and args.principal is not None and args.periods is not None:
    if (args.principal < 0 or args.periods < 0 or args.interest < 0):
        print("Incorrect parameters.")
    else:
        total_payment = 0
        for i in range(1, args.periods + 1):
            # Calculate the monthly payment for the current month (increasing principal reduction over time)
            monthly_payment = math.ceil(args.principal / args.periods + nominal_interest_rate * (args.principal - (args.principal * (i - 1)) / args.periods))
            print(f"Month {i}: payment is {monthly_payment}")
            total_payment += monthly_payment
    
        # Calculate overpayment for diff type
        overpayment = total_payment - args.principal
        print(f"Overpayment = {overpayment}")

else:
    print("Incorrect parameters.")
