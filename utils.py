import csv

def write_csv(file_name, matrix):
    f = open(file_name, 'w')
    writer = csv.writer(f)
    writer.writerows(matrix)
    f.close()