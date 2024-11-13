import pandas as pd
from fpdf import FPDF

# Step 1: Set path to desired directory

#path = "/dc_cc_analyzer/data/"
#inputs_file = (path + "inputs.csv")
#outputs_file = (path + "outputs.csv")
#results_file = (path + "results.csv")
#coupling_file = (path + "coupling.csv")
#SUT_path = (path + "SUT/")
#testvector_path = (path + "test_vector/")
inputs_file = ("inputs.csv")
outputs_file = ("outputs.csv")
coupling_file = ("couplings.csv")
SUT_file = ("results_sut.csv")
SUTI_file  = ("results_suti.csv")
testvector_file = ("test_vec.csv")

# Step 2: Read each CSV file into a DataFrame
inputs_df = pd.read_csv(inputs_file)
outputs_df = pd.read_csv(outputs_file, index_col=0)
coupling_df = pd.read_csv(coupling_file, index_col=0)
sut_df = pd.read_csv(SUT_file, index_col=0)
suti_df = pd.read_csv(SUTI_file, index_col=0)
testvector_df = pd.read_csv(testvector_file)

# Step 3: Organize dataframes
combined_df = pd.concat([inputs_df, coupling_df], axis=1)
#combined_df = pd.merge(inputs_df, coupling_df, left_index=True, right_index=True, how='outer')
df = pd.DataFrame(combined_df) # Treating data issues
df.fillna('', inplace=True) # fills NaN with empty string
display(df)

#Step 4 - Create class PDF
class PDF(FPDF):
    def header(self):
        title_w = self.get_string_width('DC/CC Analyzer') + 6
        doc_w = self.w - 2 * self.l_margin
        self.set_x((doc_w - title_w) / 2)
        self.set_font('times', 8, 20)
        self.cell(title_w,10, 'DC/CC Analyzer', border=True, align='C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('times', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font('times','I',8)
        self.cell(0,10, f'Página {self.page_no()}', align = 'C')
        #self.image('/content/drive/My Drive/Colab Notebooks/logo.png', 10, self.y + 5, w=20)

#Step 5 - Create PDF Object
pdf = FPDF('L', 'mm', 'A3')
#Layout ('P', 'L') Unit ('mm', 'cm', 'in') format ('A3', 'A4'default, 'A5', 'Letter', 'Legal', (100,150))
#Page Break #self.set_text_color(169,169,169)
#pdf.set_auto_page_break(auto = True, margin = 15)

#Define metadata
pdf.set_title('DC/CC Analyzer Report')
pdf.set_author('Aline Andreotti, Bruno Alvarenga, Gabriel Santos, Gustavo Pinheiro, Moacir Galdino')

#Create Github link
website = 'https://github.com/GabrielSSAraujo/dc_cc_analyzer.git'

#Step 6 - Fill up document
#Add page
pdf.add_page()
pdf.set_font('times', '', 16)
#Font 'B' bold, 'U' underline, 'I' italics, '' regular, combinations string 'BUI'
#times, courier, helvetica, symbol, arial
#add text w = width h = height

# Summary section
pdf.cell(0,10, 'Data Coupling/Control Coupling Analyzer', border=False, align='C')
pdf.ln()
pdf.cell(0, 10, f"Github location: https://github.com/GabrielSSAraujo/dc_cc_analyzer.git", link = website)
pdf.ln()
pdf.cell(0, 10, f"Project: Software Under Test")
pdf.ln()
pdf.cell(0, 10, f"Test Vector: {testvector_file}")
pdf.ln()
pdf.cell(0, 10, f"DC/CC Coverage: %")
pdf.ln(10)

# Calculate table dimensions
num_columns = len(df.columns)
col_width = (pdf.w - 2 * pdf.l_margin) / num_columns

# Add table header
pdf.set_font("helvetica", 'B', 12)
for col in df.columns:
    pdf.cell(col_width, 10, txt=col, border=1)
pdf.ln()

# Add table body
pdf.set_font("helvetica", '', 12)
for index, row in df.iterrows():
    if pdf.y > pdf.page_break_trigger:
        pdf.add_page()
        pdf.set_font("helvetica", 'B', 12)
        for col in df.columns:
            pdf.cell(col_width, 10, text=col, border=1)
        pdf.ln()
        pdf.set_font("helvetica", '', 12)
    for col in df.columns:
        pdf.cell(col_width, 10, text=str(row[col]), border=1)
    pdf.ln()

#Step 7 - Output pdf file
pdf.output('report.pdf')

