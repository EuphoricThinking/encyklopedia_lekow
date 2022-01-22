import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("firstCol", help = "Number of the first column to match", type=int)
    parser.add_argument("secondCol", help = "Number of the second column to match, multiple content", type=int)
    parser.add_argument("-b", "--fromBeginning", help="Whether full csv", action="store_false")
    parser.add_argument("path", help="Path to the file")
    parser.add_argument("name", help="Name of the file to save")
    args = parser.parse_args()

    return args.firstCol, args.secondCol, args.fromBeginning, args.path, args.name

def open_csv(pathname, fromBeginning):
    with open(pathname, newline = '') as csfile:
        reader = csv.reader(csfile, delimiter=',')
        index = 1 if fromBeginning else 0
        result = [row for row in list(reader)[index:]]

        return result

def create_list_for_table_with_duplicates(csfile, col1, col2):
    result = []

    for row in csfile:
        temp = [row[col1], row[col2]]
        result.append(temp)

    doubled = []

    for row in result:
        res_col_2 = row[1].split(", ")

        for tinyRow in res_col_2:
            doubled.append([row[0], tinyRow])

    return doubled


if __name__ == '__main__':
    first, second, begin, path, name = parse_args()
    res = open_csv(path, begin)
    result = create_list_for_table_with_duplicates(res, first, second)
    print(result)