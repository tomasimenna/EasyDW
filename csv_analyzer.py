import csv, time

class csvFile():
    def __init__(self, csv_path):

        col_names = []
        data_dict = {}

        def csv_to_lists(path):
            with open(path, encoding='utf-8') as csvf:
                csvReader = csv.DictReader(csvf)

                first_row = next(csvReader)
                for key in first_row:
                    col_names.append(key)

                for key in col_names:
                    data_dict[key] = []

                for row in csvReader:
                    for key in col_names:
                        data_dict[key].append(row[key])

                return data_dict

        # Take the data dictionary and analyze it to understand the type of data (to SQL 'Numeric' or 'Varchar'), together with the length of the longest value.
        def clasify_data(data):
            for key in data:
                ls = data[key]
                #try:
                #    ls = list(map(float, ls))
                #    data[key] = ['Real', None]
                #except:
                max_len = len(max(ls, key=len))
                max_len = 50 if max_len <= 50 else 255
                data[key] = ['Varchar', max_len]
                
            return data

        while True:
            try:
                data = csv_to_lists(path = csv_path)
                self.structure = clasify_data(data = data)
                break
            
            except:
                time.sleep(1)
