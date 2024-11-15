import pandas as pd
import json
from fpdf import FPDF

# Step 1: Set path to directory
website = 'https://github.com/GabrielSSAraujo/dc_cc_analyzer.git'
path = ".../dc_cc_analyzer/"
inputs_file = (path + "data/inputs.csv")
outputs_file = (path + "data/outputs.csv")
results_file = (path + "data/results.csv")
coupling_file = (path + "data/couplings.csv")
#SUT_file = (path + "tests/data/results_sut.csv")
#SUTI_file = (path + "tests/data/results_suti.csv")
testvector_file = (path + "tests/data/test_vectors/TestVec_VCP-500-VC-01.csv")
graph_file = (path + 'utils/graph.png')
json_file = (path + "data/coupling_data.json")


# Step 2: Read each CSV file into a DataFrame
inputs_df = pd.read_csv(inputs_file)
outputs_df = pd.read_csv(outputs_file, index_col=0)
coupling_df = pd.read_csv(coupling_file)
#sut_df = pd.read_csv(SUT_file, index_col=0)
#suti_df = pd.read_csv(SUTI_file, index_col=0)
testvector_df = pd.read_csv(testvector_file)
# Step 2.1: Read json dictionary
with open(json_file, 'r') as f:
    df_json = json.load(f)

# Step 3: Organize dataframes
combined_df = coupling_df
#combined_df = pd.concat([coupling_df,df_json], axis=1)
#combined_df = pd.merge(inputs_df, coupling_df, left_index=True, right_index=True, how='outer')
df = pd.DataFrame(combined_df) # Treating data issues
#df.fillna('', inplace=True) # fills NaN with empty string

#Json content
#print(df_json['key1']) # Accessing a value using a key
#print(df_json[0])     # Accessing a value using an index
num_columns = len(df.columns)
#num_columns_table2 = len(self.df_json.columns)_columns_table2
dc_cc_coverage1 = 80
dc_cc_coverage2 = 60

#Step 4 - Create class PDF
class Printer:
    def __init__(self, df, df_json):
        self.df = df
        self.df_json = df_json
        self.website = website
        #Step 4.1 - Create FPDF Object
        self.pdf = FPDF('L', 'mm', 'A3')
        self.pdf.set_title('DC/CC Analyzer Report')
        self.pdf.set_author('Aline Andreotti, Bruno Alvarenga, Gabriel Santos, Gustavo Pinheiro, Moacir Galdino')
#Step 5 - Fill up document
    def generate_report(self):
        #Add first page
        self.pdf.add_page()
        self.pdf.set_font('times', '', 16)
        #First section
        self.pdf.cell(0, 10, 'Data Coupling/Control Coupling Report', border=False, align='C')
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Github location: {website}", link=website)
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Project: Software Under Test")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Test Vector: {testvector_file}")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"DC/CC Simple Coverage: {dc_cc_coverage1}%")
        self.pdf.ln(10)
        self.pdf.cell(0, 10, f"DC/CC Independent Coverage: {dc_cc_coverage2}%")
        self.pdf.ln(10)

        col_width = (self.pdf.w - 2 * self.pdf.l_margin) / num_columns
       
        #Second section - COUPLING STATUS
           
        #Third section - COUPLING VALUES
        self.pdf.set_font("helvetica", 'B', 12)
        for col in self.df.columns:
            self.pdf.cell(col_width, 10, txt=col, border=1)
        self.pdf.ln()

        self.pdf.set_font("helvetica", '', 12)
        for index, row in self.df.iterrows():
            if self.pdf.y > self.pdf.page_break_trigger:
                self.pdf.add_page()
                self.pdf.set_font("helvetica", 'B', 12)
                for col in self.df.columns:
                    self.pdf.cell(col_width, 10, text=col, border=1)
                self.pdf.ln()
                self.pdf.set_font("helvetica", '', 12)
            for col in self.df.columns:
                self.pdf.cell(col_width, 10, text=str(row[col]), border=1)
            self.pdf.ln()

        #Fourth section (Coupling graph) 
        self.pdf.add_page()  # Add a new page
        self.pdf.image(graph_file, x=100, y=100, w=200)  # Adjust x, y, and w as needed
        self.pdf.ln()  # Move cursor below the image
        self.pdf.set_font('helvetica', '', 12) 
        self.pdf.cell(0, 10, 'Coupling Graph', 0, 1, 'C')  # Centered caption
        
        #Close document
        self.pdf.output('report.pdf')

#Step 7 - Create printer object / Generate output file
printer = Printer(df, df_json)
printer.generate_report()
