import subprocess
import sys
import math


def run_system(data):
    command = [
        sys.executable,
        "LoanProcessingSystem.py"
    ] + [str(x) for x in data]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout


def test(number, name, data, expected):

    output = run_system(data)

    if expected in output:
        print(f"Test {number:02d} - {name:<35} : PASS")
        return True

    print(f"Test {number:02d} - {name:<35} : FAIL")
    print("Expected:", expected)
    print("Actual:", output.strip())

    return False


def main():

    print("=" * 65)
    print("          LOAN PROCESSING QA TEST SUITE")
    print("=" * 65)

    tests = [

        # Test 1
        (
            "Minimum age",
            ("T001", 18, 50000, 100000, 780,
             "Salaried", 500000, 60),
            "Loan Status          : APPROVED"
        ),

        # Test 2
        (
            "Maximum age",
            ("T002", 60, 50000, 100000, 780,
             "Salaried", 500000, 60),
            "Loan Status          : APPROVED"
        ),

        # Test 3
        (
            "Invalid age",
            ("T003", 17, 50000, 100000, 780,
             "Salaried", 500000, 60),
            "Age must be between 18 and 60."
        ),

        # Test 4
        (
            "Invalid salary",
            ("T004", 25, 0, 100000, 780,
             "Salaried", 500000, 60),
            "Monthly salary must be greater than zero."
        ),

        # Test 5
        (
            "Poor credit score",
            ("T005", 25, 50000, 100000, 550,
             "Salaried", 500000, 60),
            "Poor credit score."
        ),

        # Test 6
        (
            "High existing loan",
            ("T006", 30, 50000, 2000000, 780,
             "Salaried", 500000, 60),
            "High debt-to-income ratio."
        ),

        # Test 7
        (
            "High DTI",
            ("T007", 30, 30000, 900000, 780,
             "Salaried", 300000, 60),
            "High debt-to-income ratio."
        ),

        # Test 8
        (
            "Salaried employment",
            ("T008", 30, 50000, 100000, 780,
             "Salaried", 500000, 60),
            "Loan Status          : APPROVED"
        ),

        # Test 9
        (
            "Self-employed",
            ("T009", 30, 50000, 100000, 780,
             "Self-Employed", 500000, 60),
            "Loan Status          : APPROVED"
        ),

        # Test 10
        (
            "Business category",
            ("T010", 30, 50000, 100000, 780,
             "Business", 500000, 60),
            "Loan Status          : APPROVED"
        ),

        # Test 11
        (
            "Invalid employment",
            ("T011", 30, 50000, 100000, 780,
             "Student", 500000, 60),
            "Employment type must be"
        ),

        # Test 12
        (
            "Loan at eligibility limit",
            ("T012", 30, 50000, 100000, 780,
             "Salaried", 1000000, 60),
            "Loan Status          : APPROVED"
        ),

        # Test 13
        (
            "Loan above eligibility",
            ("T013", 30, 50000, 100000, 780,
             "Salaried", 1000001, 60),
            "Requested loan amount exceeds"
        ),

        # Test 14 - EMI
        (
            "EMI calculation",
            ("T014", 30, 50000, 100000, 780,
             "Salaried", 500000, 60),
            None
        ),

        # Test 15
        (
            "Invalid numeric input",
            ("T015", "twenty-five", 50000, 100000, 780,
             "Salaried", 500000, 60),
            "ERROR: Invalid input."
        ),

        # Test 16
        (
            "Invalid tenure",
            ("T016", 30, 50000, 100000, 780,
             "Salaried", 500000, 0),
            "Loan tenure must be greater than zero..."
        )
    ]


    passed = 0


    for number, (name, data, expected) in enumerate(tests, 1):

        # Special check for EMI
        if number == 14:

            output = run_system(data)

            principal = 500000
            rate = 8 / (12 * 100)
            months = 60

            emi = (
                principal
                * rate
                * (1 + rate) ** months
            ) / (
                (1 + rate) ** months - 1
            )

            try:

                line = next(
                    line for line in output.splitlines()
                    if "Monthly EMI" in line
                )

                actual = float(
                    line.split("₹")[1]
                )

                passed_emi = math.isclose(
                    actual,
                    emi,
                    abs_tol=0.01
                )

            except (StopIteration, ValueError, IndexError):

                passed_emi = False


            if passed_emi:

                print(
                    f"Test 14 - "
                    f"{'EMI calculation':<35} : PASS"
                )

                passed += 1

            else:

                print(
                    f"Test 14 - "
                    f"{'EMI calculation':<35} : FAIL"
                )

                print(
                    f"Expected EMI: ₹{emi:.2f}"
                )

                print("Actual:", output.strip())

        else:

            if test(
                number,
                name,
                data,
                expected
            ):
                passed += 1


    failed = len(tests) - passed


    print("=" * 65)
    print("                       QA SUMMARY")
    print("=" * 65)

    print(f"Total Tests : {len(tests)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    print("-" * 65)


    if failed == 0:

        print("OVERALL RESULT : ALL TESTS PASSED")
        print("=" * 65)

        # Jenkins SUCCESS
        sys.exit(0)

    else:

        print("OVERALL RESULT : SOME TESTS FAILED")
        print("=" * 65)

        # Jenkins FAILURE
        sys.exit(1)


if __name__ == "__main__":
    main()