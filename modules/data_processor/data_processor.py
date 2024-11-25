import pandas as pd
import logging
import decimal
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataProcessor:
    def __init__(self, files_dir):
        # Load CSV files
        self.files_dir = files_dir
        self.expected_outputs = pd.read_csv(files_dir + "outputs.csv")
        self.actual_results = pd.read_csv(files_dir + "results_sut.csv")
        self.suti_results = pd.read_csv(files_dir + "results_suti.csv")
        self.probes = pd.read_csv(files_dir + "couplings.csv")
        self.pass_rate = 0.0
        self.exercised_percentage = 0.0
        self.compromised_suti = False
        self.results_data = {"global": {}, "couplings": {}, "pass_fail": {}}

        # Load tolerances as a dictionary
        tolerances_df = pd.read_csv(
            files_dir + "tolerances.csv", index_col=0, header=None
        )
        self.tolerances = tolerances_df[
            1
        ].to_dict()  # Column 1 contains tolerance values

    def check_variation(self, row_index, column, dataframe, tolerance):
        """
        Check if the value at the given row and column in a DataFrame
        has varied beyond the specified tolerance compared to its predecessor.
        """
        # Ensure the row_index is valid and has a predecessor
        if row_index <= 0 or row_index >= len(dataframe):
            logging.warning(
                f"Row index {row_index} is out of bounds or has no predecessor."
            )
            return False

        # Retrieve the current and previous values
        current_value = dataframe.at[row_index, column]
        previous_value = dataframe.at[row_index - 1, column]

        # Calculate the absolute difference and check if it exceeds the tolerance
        return (
            round_to_match_decimals(abs(current_value - previous_value), tolerance)
            > tolerance
        )

    def get_coverage(self, func_coverage_list):
        total_coverage = 0
        coverage_count = 0
        for df_func in func_coverage_list:
            total_coverage += df_func.size
            coverage_count += (df_func != "0").sum().sum()
        if total_coverage > 0:
            return round((coverage_count / total_coverage) * 100, 2)
        else:
            return 0

    def get_pass_fail_coverage(self):
        # Initialize pass/fail counters
        total_tests = 0
        passed_tests = 0

        # Perform pass/fail analysis for each row
        for index, row in self.expected_outputs.iterrows():
            total_tests += 1
            pass_case = True
            for column in row.index:
                if column != "Time":
                    expected_value = row[column]
                    actual_value = self.actual_results.at[index, column]
                    suti_value = self.suti_results.at[index, column]
                    tolerance = float(self.tolerances.get(column, 0))

                    # Check if the actual value is within tolerance of the expected output
                    difference = abs(expected_value - actual_value)
                    rounded_difference = round_to_match_decimals(difference, tolerance)
                    if rounded_difference > tolerance:
                        pass_case = False

                    # Check if the difference between actual result and SUTI result exceeds tolerance
                    tolerance = 0.00001
                    difference = abs(actual_value - suti_value)
                    rounded_difference = round_to_match_decimals(difference, tolerance)
                    if rounded_difference > tolerance:
                        logging.warning(
                            f"Warning: Difference between actual result ({actual_value}) and "
                            f"SUTI result ({suti_value}) for '{column}' at index {index} exceeds tolerance ({tolerance})."
                            f"Instrumented SUT may be compromised."
                        )
                        self.compromised_suti = True

            time = str(self.actual_results.at[index, "Time"])
            self.results_data["pass_fail"][time] = pass_case
            # Count passes/fails
            if pass_case:
                passed_tests += 1

        # Calculate and log pass rate
        self.pass_rate = round((passed_tests / total_tests) * 100, 2)
        # print(f"Percentage of passed test cases: {self.pass_rate:.2f}%")
        self.results_data["global"]["pass_fail"] = self.pass_rate

        return self.pass_rate, self.results_data["pass_fail"]

    def analyze(self, function_interface_list):
        tolerance = 0.00001
        # self.probes
        # se entradas variaram de forma independente
        func_coverage_list = []
        for function_interface in function_interface_list:
            inputs = [item.current_name for item in function_interface.input_parameters]
            outputs = [
                item.current_name for item in function_interface.output_parameters
            ]
            input_size = len(inputs)
            list = ["0"] * input_size
            d = {}

            for item in function_interface.output_parameters:
                d[item.current_name] = list

            new_df = pd.DataFrame(data=d, index=inputs)
            new_df.name = function_interface.function_name

            for index, row in self.probes.iterrows():
                if index < 1:
                    continue
                has_changed = []

                for input in inputs:
                    last_row = self.probes.iloc[index - 1]

                    if abs(row[input] - last_row[input]) > tolerance:
                        has_changed.append(input)

                if len(has_changed) == 1:
                    for output in outputs:
                        if abs(row[output] - last_row[output]) > tolerance:
                            new_df.loc[has_changed[0], output] = (
                                str(last_row["Time"]) + "-" + str(row["Time"])
                            )
            func_coverage_list.append(new_df)

        return func_coverage_list

    def get_total_couplings(self):
        size = 0
        for coupling in self.couplings_outputs.values():
            size += len(coupling)
        return size

    def init_couplings_fields_in_results_data(self):
        couplings = self.probes.columns[1:]
        for coupling in couplings:
            self.results_data["couplings"][coupling] = {}
            self.results_data["couplings"][coupling]["related_outputs"] = {}
            for output in self.couplings_outputs:
                couplings_related_to_output = self.couplings_outputs[output]
                if coupling in couplings_related_to_output:
                    self.results_data["couplings"][coupling]["related_outputs"][
                        output
                    ] = {}
                    self.results_data["couplings"][coupling]["related_outputs"][output][
                        "covered"
                    ] = False
                    self.results_data["couplings"][coupling]["related_outputs"][output][
                        "time_of_coverage"
                    ] = []


def round_to_match_decimals(number, reference):
    # Determine the number of decimal places in the reference number
    decimal_places = abs(decimal.Decimal(str(reference)).as_tuple().exponent)
    # Round the number to match the decimal places of the reference
    return round(number, decimal_places)
