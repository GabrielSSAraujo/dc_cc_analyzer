import pandas as pd
import json
from fpdf import FPDF


# Step 4 - Create class PDF
class Printer:
    def __init__(self, path, test_vector_path):
        # Step 1: Set path to directory
        self.path = path
        self.website = "https://github.com/GabrielSSAraujo/dc_cc_analyzer.git"

        # Step 2: Read each CSV file into a DataFrame
        self.inputs_df = pd.read_csv(self.path + "inputs.csv")
        self.outputs_df = pd.read_csv(self.path + "outputs.csv", index_col=0)
        self.coupling_df = pd.read_csv(self.path + "couplings.csv")
        self.test_vector_path = test_vector_path
        self.df = None
        self.website = self.website
        # Step 4.1 - Create FPDF Object
        self.pdf = FPDF("L", "mm", "A3")
        self.pdf.set_title("DC/CC Analyzer Report")
        self.pdf.set_author(
            "Aline Andreotti, Bruno Alvarenga, Gabriel Santos, Gustavo Pinheiro, Moacir Galdino"
        )

    def get_data_frame_from_json(self):
        with open(self.path + "results_data.json", "r") as f:
            return json.load(f)

    # Step 5 - Fill up document
    def generate_report(self):
        # using pandas data frame
        self.json_df = self.get_data_frame_from_json()
        num_columns = len(self.json_df)

        pass_fail_rate = self.json_df["global"]["pass_fail"]
        dc_cc_coverage1 = self.json_df["global"]["DC_CC_simple_coverage"]
        dc_cc_coverage2 = self.json_df["global"]["DC_CC_independent_coverage"]

        # Add first page
        self.pdf.add_page()
        self.pdf.set_font("times", "", 16)
        # First section
        self.pdf.cell(
            0, 10, "Data Coupling/Control Coupling Report", border=False, align="C"
        )
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Github location: {self.website}", link=self.website)
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Project: Software Under Test")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Test Vector: {self.test_vector_path}")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Pass/Fail: {pass_fail_rate}%")
        self.pdf.ln(10)
        self.pdf.cell(0, 10, f"DC/CC Simple Coverage: {dc_cc_coverage1}%")
        self.pdf.ln(10)
        self.pdf.cell(0, 10, f"DC/CC Independent Coverage: {dc_cc_coverage2}%")
        self.pdf.ln(10)

        col_width = (self.pdf.w - 2 * self.pdf.l_margin) / num_columns

        # Second section - COUPLING STATUS
        couplings_list = self.json_df["couplings"]
        cols = ["couplings"]
        for col in self.outputs_df.columns:
            cols.append(col)

        formatted_data_frame = pd.DataFrame(columns=cols)
        print(formatted_data_frame.columns)
        for coupling in couplings_list:
            teste = []
            for output in couplings_list[str(coupling)]["related_outputs"]:
                teste.append(output)
            print(str(coupling) + ":" + str(teste))

        # Third section - COUPLING VALUES
        self.pdf.set_font("helvetica", "B", 12)
        for col in self.df.columns:
            self.pdf.cell(col_width, 10, txt=col, border=1)
        self.pdf.ln()

        self.pdf.set_font("helvetica", "", 12)
        for index, row in self.df.iterrows():
            if self.pdf.y > self.pdf.page_break_trigger:
                self.pdf.add_page()
                self.pdf.set_font("helvetica", "B", 12)
                for col in self.df.columns:
                    self.pdf.cell(col_width, 10, text=col, border=1)
                self.pdf.ln()
                self.pdf.set_font("helvetica", "", 12)
            for col in self.df.columns:
                self.pdf.cell(col_width, 10, text=str(row[col]), border=1)
            self.pdf.ln()

        # Fourth section (Coupling graph)
        self.pdf.add_page()  # Add a new page
        self.pdf.image(
            "data/data_couplings_flow/dc_graph.png", x=100, y=100, w=200
        )  # Adjust x, y, and w as needed
        self.pdf.ln()  # Move cursor below the image
        self.pdf.set_font("helvetica", "", 12)
        self.pdf.cell(0, 10, "Coupling Graph", 0, 1, "C")  # Centered caption

        # Close document
        self.pdf.output("report.pdf")
