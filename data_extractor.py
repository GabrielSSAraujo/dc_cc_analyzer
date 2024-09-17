import csv

class DataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def extract_data_from_csv(self):
        input_list = []
        output_list = []
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            self.data = csv.reader(file)

            # find indexes of input and output
            first_row = next(self.data)
            initial_index = 0
            final_index = 0
            for index, item in enumerate(first_row):
                if(item == 'comment1'):
                    initial_index = index+1
                elif(item == 'comment2'):
                    final_index = index

            # extract data inputs and outputs
            for row in self.data:
                input_list.append(list(map(int, row[initial_index:final_index])))
                output_list.append(list(map(int, row[final_index+1:len(row)])))

        return input_list, output_list

if __name__ == "__main__":
    data = DataExtractor("./testes/vetores-teste.csv")
    print(data.extract_data_from_csv())