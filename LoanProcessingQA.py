import subprocess
import sys
import math


# ---------------------------------------------------------
# RUN DEVELOPMENT PROGRAM
# ---------------------------------------------------------

def run_system(
    customer_id,
    age,
    salary,
    existing_loan,
    credit_score,
    employment_type,
    requested_loan,
    tenure
):

    command = [
        sys.executable,
        "LoanProcessingSystem.py",
        str(customer_id),
        str(age),
        str(salary),
        str(existing_loan),
        str(credit_score),
        str(employment_type),
        str(requested_loan),
        str(tenure)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout


# ---------------------------------------------------------
# TEST HELPER
# ---------------------------------------------------------

def run_test(test_number, test_name, test_data, expected_text):

    output = run_system(*test_data)

    passed = expected_text in output

    if passed:
        print(
            f"Test {test_number:02d} - "
            f"{test_name:<40} : PASS"
        )
    else:
        print(
            f"Test {test_number:02d} - "
            f"{test_name:<40} : FAIL"
        )

        print("Expected:")
        print(expected_text)

        print("Actual Output:")
        print(output)

    return passed


# ---------------------------------------------------------
# QA TESTS
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("             LOAN PROCESSING QA TEST SUITE")
    print("=" * 70)

    total_tests = 0
    passed_tests = 0


    # -----------------------------------------------------
    # TEST 1 - MINIMUM AGE
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        1,
        "Minimum age (18)",
        (
            "T001",
            18,
            50000,
            100000,
            780,
            "Salaried",
            500000,
            60
        ),
        "Loan Status          : APPROVED"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 2 - MAXIMUM AGE
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        2,
        "Maximum age (60)",
        (
            "T002",
            60,
            50000,
            100000,
            780,
            "Salaried",
            500000,
            60
        ),
        "Loan Status          : APPROVED"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 3 - INVALID AGE
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        3,
        "Invalid age below minimum",
        (
            "T003",
            17,
            50000,
            100000,
            780,
            "Salaried",
            500000,
            60
        ),
        "Age must be between 18 and 60."
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 4 - INVALID SALARY
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        4,
        "Invalid salary",
        (
            "T004",
            25,
            0,
            100000,
            780,
            "Salaried",
            500000,
            60
        ),
        "Monthly salary must be greater than zero."
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 5 - POOR CREDIT SCORE
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        5,
        "Poor credit score",
        (
            "T005",
            25,
            50000,
            100000,
            550,
            "Salaried",
            500000,
            60
        ),
        "Poor credit score."
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 6 - EXISTING LOAN EXCEEDS THRESHOLD
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        6,
        "Existing loan exceeds threshold",
        (
            "T006",
            30,
            50000,
            2000000,
            780,
            "Salaried",
            500000,
            60
        ),
        "High debt-to-income ratio."
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 7 - HIGH DTI
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        7,
        "High debt-to-income ratio",
        (
            "T007",
            30,
            30000,
            900000,
            780,
            "Salaried",
            300000,
            60
        ),
        "High debt-to-income ratio."
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 8 - SALARIED EMPLOYMENT
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        8,
        "Salaried employment",
        (
            "T008",
            30,
            50000,
            100000,
            780,
            "Salaried",
            500000,
            60
        ),
        "Loan Status          : APPROVED"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 9 - SELF-EMPLOYED
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        9,
        "Self-employed category",
        (
            "T009",
            30,
            50000,
            100000,
            780,
            "Self-Employed",
            500000,
            60
        ),
        "Loan Status          : APPROVED"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 10 - BUSINESS
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        10,
        "Business category",
        (
            "T010",
            30,
            50000,
            100000,
            780,
            "Business",
            500000,
            60
        ),
        "Loan Status          : APPROVED"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 11 - INVALID EMPLOYMENT
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        11,
        "Invalid employment category",
        (
            "T011",
            30,
            50000,
            100000,
            780,
            "Student",
            500000,
            60
        ),
        "Employment type must be"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 12 - BOUNDARY LOAN AMOUNT
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        12,
        "Loan amount at eligibility boundary",
        (
            "T012",
            30,
            50000,
            100000,
            780,
            "Salaried",
            1000000,
            60
        ),
        "Loan Status          : APPROVED"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 13 - LOAN ABOVE ELIGIBLE AMOUNT
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        13,
        "Loan amount above eligibility",
        (
            "T013",
            30,
            50000,
            100000,
            780,
            "Salaried",
            1000001,
            60
        ),
        "Requested loan amount exceeds"
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # TEST 14 - EMI CALCULATION ACCURACY
    # -----------------------------------------------------

    total_tests += 1

    test_data = (
        "T014",
        30,
        50000,
        100000,
        780,
        "Salaried",
        500000,
        60
    )

    output = run_system(*test_data)

    # Expected EMI for:
    # Loan = 500000
    # Interest = 8%
    # Tenure = 60 months

    principal = 500000
    annual_rate = 8.0
    months = 60

    monthly_rate = annual_rate / (12 * 100)

    power = math.pow(
        1 + monthly_rate,
        months
    )

    expected_emi = (
        principal
        * monthly_rate
        * power
    ) / (power - 1)

    emi_text = f"Monthly EMI           : ₹{expected_emi:.2f}"

    if emi_text in output:

        print(
            f"Test 14 - "
            f"{'EMI calculation accuracy':<40} : PASS"
        )

        passed_tests += 1

    else:

        print(
            f"Test 14 - "
            f"{'EMI calculation accuracy':<40} : FAIL"
        )

        print("Expected:")
        print(emi_text)

        print("Actual Output:")
        print(output)


    # -----------------------------------------------------
    # TEST 15 - INVALID NUMERIC INPUT
    # -----------------------------------------------------

    total_tests += 1

    command = [
        sys.executable,
        "LoanProcessingSystem.py",
        "T015",
        "twenty-five",
        "50000",
        "100000",
        "780",
        "Salaried",
        "500000",
        "60"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if "ERROR: Invalid input." in result.stdout:

        print(
            f"Test 15 - "
            f"{'Invalid numeric input':<40} : PASS"
        )

        passed_tests += 1

    else:

        print(
            f"Test 15 - "
            f"{'Invalid numeric input':<40} : FAIL"
        )

        print(result.stdout)


    # -----------------------------------------------------
    # TEST 16 - INVALID TENURE
    # -----------------------------------------------------

    total_tests += 1

    if run_test(
        16,
        "Invalid loan tenure",
        (
            "T016",
            30,
            50000,
            100000,
            780,
            "Salaried",
            500000,
            0
        ),
        "Loan tenure must be greater than zero."
    ):
        passed_tests += 1


    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("                    QA SUMMARY")
    print("=" * 70)

    print(f"Total Tests : {total_tests}")
    print(f"Passed      : {passed_tests}")
    print(f"Failed      : {total_tests - passed_tests}")

    print("-" * 70)

    if passed_tests == total_tests:

        print("OVERALL RESULT : ALL TESTS PASSED")
        print("=" * 70)

        # Jenkins will consider this successful
        sys.exit(0)

    else:

        print("OVERALL RESULT : SOME TESTS FAILED")
        print("=" * 70)

        # Jenkins will consider this a failed build
        sys.exit(1)


if __name__ == "__main__":
    main()
