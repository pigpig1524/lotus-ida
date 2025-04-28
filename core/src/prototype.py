import os
import pandas as pd

class DAHelper:
    def __init__(self,
                data_filepath: str,
                data_description_filepath: str,
                txt_delimiter = '\t'):
        '''
        data_filepath: The path to your CSV, EXCEL, or TXT data file
        data_description_filepath: The path to your TXT data description file
        '''
        self.data_filepath = data_filepath
        self.data_description_filepath = data_description_filepath
        self.txt_delimeter = txt_delimiter
        
        self.data = pd.DataFrame()
        self.data_description = ''
        
        self.supported_data_types = ['.csv', '.txt', '.xlsx', '.xls']
        self.supported_data_description_types = ['.txt']
        
    def set_filepaths(self,
                      data_filepath = '',
                      data_description_filepath = '',
                      txt_delimiter = '\t'):
        if data_filepath != '':
            self.data_filepath = data_filepath
        if data_description_filepath != '':
            self.data_description_filepath = data_description_filepath
        self.txt_delimeter = txt_delimiter
        
    def set_data(self,
                 data):
        self.data = data
            
    def detect_filetypes(self):
        basename_data = os.path.basename(self.data_filepath)
        _, file_extension_data = os.path.splitext(basename_data)
        
        basename_data_description = os.path.basename(self.data_description_filepath)
        _, file_extension_data_description = os.path.splitext(basename_data_description)
        
        return file_extension_data, file_extension_data_description
        
    def load_data(self):
        data_filetype, data_description_filetype = self.detect_filetypes()
        
        if data_filetype not in self.supported_data_types:
            print(f'Data of type: {data_filetype} not supported.')
            return
        if data_description_filetype not in self.supported_data_description_types:
            print(f'Data of type: {data_description_filetype} not supported.')
            return

        if data_filetype == '.xlsx' or data_filetype == '.xls':
            self.data = pd.read_excel(self.data_filepath)
        elif data_filetype == '.csv':
            self.data = pd.read_csv(self.data_filepath)
        elif data_filetype == '.txt':
            self.data = pd.read_csv(self.data_filepath, txt_delimiter=self.txt_delimeter)
        
        with open(self.data_description_filepath, 'r') as f:
            self.data_description = f.read()
            
    def export_data(self, output_filepath):
        '''
        Export to CSV or Excel file
        '''
        basename = os.path.basename(output_filepath)
        _, file_extension = os.path.splitext(basename)
        
        if file_extension == '.csv':
            self.data.to_csv(output_filepath, index=False)
        elif file_extension == '.xlsx':
            self.data.to_excel(output_filepath, index=False)
        else:
            print(f'Export to datatype: {file_extension} not supported.')
        
