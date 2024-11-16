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
        self.inputs = pd.read_csv(files_dir + "inputs.csv")
        self.expected_outputs = pd.read_csv(files_dir + "outputs.csv")
        self.actual_results = pd.read_csv(files_dir + "results_sut.csv")
        self.suti_results = pd.read_csv(files_dir + "results_suti.csv")
        self.couplings = pd.read_csv(files_dir + "couplings.csv")
        self.pass_rate = 0.0
        self.exercised_percentage = 0.0
        self.compromised_suti = False
        self.results_data = {"global": {}, "couplings": {}, "pass_fail": {}}
        self.couplings_outputs = self.load_couplings_outputs(
            files_dir + "data_couplings_flow/couplings_data.json"
        )

        # Load tolerances as a dictionary
        tolerances_df = pd.read_csv(
            files_dir + "tolerances.csv", index_col=0, header=None
        )
        self.tolerances = tolerances_df[
            1
        ].to_dict()  # Column 1 contains tolerance values

    def load_couplings_outputs(self, json_file_path):
        """Load the couplings outputs JSON file and return it as a dictionary."""
        try:
            with open(json_file_path, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            logging.error(f"Error loading couplings outputs JSON file: {e}")
            return {}

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

    def analyze(self):
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
        print(f"Percentage of passed test cases: {self.pass_rate:.2f}%")
        self.results_data["global"]["pass_fail"] = self.pass_rate

        # Perform couplings analysis
        self.analyze_couplings()

    def get_total_couplings(self):
        size = 0
        for coupling in self.couplings_outputs.values():
            size += len(coupling)
        return size

    def analyze_couplings(self):
        total_couplings = 0
        exercised_couplings = 0
        covered_couplings = 0

        # Check each coupling's values against the tolerances
        for coupling in self.couplings.columns[1:]:  # Skip the "Time" column
            total_couplings += 1  # o total de acoplamentos pode ser extraido do couplings-data.json(soma da qtde de acoplamentos de cada saida)
            coupling_exercised = False
            coupling_covered = False
            coupling_analyzed = False
            coverage_time = []

            # Iterate through values in the coupling column
            for index in range(1, len(self.couplings)):
                # Check if the coupling's value has changed compared to its previous value
                tolerance = float(self.tolerances.get(coupling, 0))
                if self.check_variation(index, coupling, self.couplings, tolerance):
                    coupling_exercised = True
                    exercised_couplings += 1
                    break  # Stop further checks as it is already exercised

            # Check if the coupling is responsible for covering a change in the output
            for index in range(1, len(self.actual_results)):
                if coupling_analyzed:
                    break
                for output_column in self.actual_results.columns:
                    if output_column == "Time":
                        continue

                    # Check if the output has changed compared to its previous value
                    output_tolerance = float(self.tolerances.get(output_column, 0))
                    if self.check_variation(
                        index, output_column, self.actual_results, output_tolerance
                    ):
                        related_couplings = self.couplings_outputs.get(
                            output_column, []
                        )
                        # Count how many related couplings have changed at this index
                        changed_couplings = [
                            rel_coupling
                            for rel_coupling in related_couplings
                            if self.check_variation(
                                index,
                                rel_coupling,
                                self.couplings,
                                float(self.tolerances.get(rel_coupling, 0)),
                            )
                        ]
                        # If only one related coupling has changed, mark it as 'covered'
                        if len(changed_couplings) == 1 and (
                            coupling in changed_couplings
                        ):
                            coupling_covered = True
                            covered_couplings += 1
                            coupling_analyzed = True
                            previous_time = str(
                                self.actual_results.at[index - 1, "Time"]
                            )
                            time_of_coverage = str(
                                self.actual_results.at[index, "Time"]
                            )
                            coverage_time = [previous_time, time_of_coverage]
                            break  # No need to check further outputs for this coupling

            self.results_data["couplings"][coupling] = {}
            self.results_data["couplings"][coupling]["exercised"] = coupling_exercised
            self.results_data["couplings"][coupling]["covered"] = coupling_covered
            self.results_data["couplings"][coupling]["time_of_coverage"] = coverage_time

        # Calculate and print the percentage of exercised and covered couplings
        self.exercised_percentage = (
            round((exercised_couplings / total_couplings) * 100, 2)
            if total_couplings
            else 0
        )
        self.covered_percentage = (
            round((covered_couplings / self.get_total_couplings()) * 100, 2)
            if total_couplings
            else 0
        )
        print(f"Percentage of exercised couplings: {self.exercised_percentage:.2f}%")
        print(f"Percentage of covered couplings: {self.covered_percentage:.2f}%")
        self.results_data["global"]["DC_CC_simple_coverage"] = self.exercised_percentage
        self.results_data["global"][
            "DC_CC_independent_coverage"
        ] = self.covered_percentage

        # Writing results_data to a JSON file
        with open(self.files_dir + "results_data.json", "w") as json_file:
            json.dump(self.results_data, json_file, indent=4)
        json_file.close()


def round_to_match_decimals(number, reference):
    # Determine the number of decimal places in the reference number
    decimal_places = abs(decimal.Decimal(str(reference)).as_tuple().exponent)
    # Round the number to match the decimal places of the reference
    return round(number, decimal_places)
