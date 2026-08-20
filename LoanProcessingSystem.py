import sys
import math


def print_rejected(customer_id, reason):
    print()
    print("=" * 50)
    print("       BANKING LOAN APPROVAL SYSTEM")
    print("=" * 50)
    print(f"Customer ID          : {customer_id}")
    print("Loan Status          : REJECTED")
    print(f"Rejection Reason     : {reason}")
    print("=" * 50)


def main():

    # --------------------------------------------------
    # CHECK INPUT COUNT
    # --------------------------------------------------

    if len(sys.argv) != 9:
        print("ERROR: Invalid number of inputs...Please enter the correct inputs")
        print()
        print("Usage:")
        print(
            "python LoanProcessingSystem.py "
            "<CustomerID> <Age> <Salary> <ExistingLoan> "
            "<CreditScore> <EmploymentType> "
            "<RequestedLoan> <Tenure>"
        )
        return

    try:

        # --------------------------------------------------
        # READ INPUTS
        # --------------------------------------------------

        customer_id = sys.argv[1]
        age = int(sys.argv[2])
        monthly_salary = float(sys.argv[3])
        existing_loan = float(sys.argv[4])
        credit_score = int(sys.argv[5])
        employment_type = sys.argv[6]
        requested_loan = float(sys.argv[7])
        loan_tenure = int(sys.argv[8])

        # --------------------------------------------------
        # INPUT VALIDATION
        # --------------------------------------------------

        if age < 18 or age > 60:
            print_rejected(
                customer_id,
                "Age must be between 18 and 60."
            )
            return

        if monthly_salary <= 0:
            print_rejected(
                customer_id,
                "Monthly salary must be greater than zero."
            )
            return

        if existing_loan < 0:
            print_rejected(
                customer_id,
                "Existing loan amount cannot be negative."
            )
            return

        if credit_score < 0 or credit_score > 900:
            print_rejected(
                customer_id,
                "Credit score must be between 0 and 900."
            )
            return

        if requested_loan <= 0:
            print_rejected(
                customer_id,
                "Requested loan amount must be greater than zero."
            )
            return

        if loan_tenure <= 0:
            print_rejected(
                customer_id,
                "Loan tenure must be greater than zero."
            )
            return

        # --------------------------------------------------
        # EMPLOYMENT VALIDATION
        # --------------------------------------------------

        valid_employment = employment_type.lower() in [
            "salaried",
            "self-employed",
            "business"
        ]

        if not valid_employment:
            print_rejected(
                customer_id,
                "Employment type must be "
                "Salaried, Self-Employed, or Business."
            )
            return

        # --------------------------------------------------
        # DTI CALCULATION
        # --------------------------------------------------
        #
        # Assumption:
        # Existing loan is converted into a monthly
        # obligation using a 60-month period.
        #

        existing_monthly_obligation = existing_loan / 60

        dti = (
            existing_monthly_obligation
            / monthly_salary
        ) * 100

        # --------------------------------------------------
        # ELIGIBLE LOAN AMOUNT
        # --------------------------------------------------
        #
        # Assumption:
        # Maximum eligible loan = 20 × monthly salary
        #

        eligible_loan = monthly_salary * 20

        # --------------------------------------------------
        # INTEREST RATE
        # --------------------------------------------------

        if credit_score >= 750:
            interest_rate = 8.0

        elif credit_score >= 600:
            interest_rate = 10.0

        else:
            interest_rate = 12.0

        # --------------------------------------------------
        # APPROVAL CHECK
        # --------------------------------------------------

        approved = True
        rejection_reason = ""

        if credit_score < 600:

            approved = False
            rejection_reason = "Poor credit score."

        elif dti > 40:

            approved = False
            rejection_reason = "High debt-to-income ratio."

        elif requested_loan > eligible_loan:

            approved = False
            rejection_reason = (
                "Requested loan amount exceeds "
                "eligible loan amount."
            )

        # --------------------------------------------------
        # EMI CALCULATION
        # --------------------------------------------------

        monthly_rate = interest_rate / (12 * 100)

        if monthly_rate == 0:

            emi = requested_loan / loan_tenure

        else:

            power = math.pow(
                1 + monthly_rate,
                loan_tenure
            )

            emi = (
                requested_loan
                * monthly_rate
                * power
            ) / (power - 1)

        # --------------------------------------------------
        # DISPLAY RESULT
        # --------------------------------------------------

        print()
        print("=" * 50)
        print("       BANKING LOAN APPROVAL SYSTEM")
        print("=" * 50)

        print(f"Customer ID          : {customer_id}")
        print(f"Age                  : {age}")
        print(f"Monthly Salary       : ₹{monthly_salary:.2f}")
        print(f"Existing Loan Amount : ₹{existing_loan:.2f}")
        print(f"Credit Score         : {credit_score}")
        print(f"Employment Type      : {employment_type}")
        print(f"Requested Loan       : ₹{requested_loan:.2f}")
        print(f"Loan Tenure          : {loan_tenure} months")

        print("-" * 50)

        print(f"Debt-to-Income Ratio : {dti:.2f}%")
        print(f"Eligible Loan Amount : ₹{eligible_loan:.2f}")
        print(f"Interest Rate        : {interest_rate:.2f}%")
        print(f"Monthly EMI          : ₹{emi:.2f}")

        print("-" * 50)

        if approved:

            print("Loan Status          : APPROVED")

        else:

            print("Loan Status          : REJECTED")
            print(f"Rejection Reason     : {rejection_reason}")

        print("=" * 50)


    # --------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------

    except ValueError:

        print()
        print("ERROR: Invalid input.")
        print(
            "Age, salary, loan amount, credit score "
            "and tenure must be valid numbers."
        )

    except Exception as e:

        print()
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
