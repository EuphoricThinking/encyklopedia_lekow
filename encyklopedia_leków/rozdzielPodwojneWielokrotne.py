import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file")
    parser.add_argument("name", help="Name of the file to save")
    args = parser.parse_args()

    return args.path, args.name

def open_csv(pathname):
    with open(pathname, newline = '') as csfile:
        reader = csv.reader(csfile, delimiter=',')
        result = [row for row in list(reader)[1:]]

        return result

def create_list_for_table_with_duplicates(csv_read):
    result = []

    for row in csv_read:
        ingredients = row[1].split(', ')
        result.append([ingredients[0], row[0]])
        if len(ingredients) > 1:
            for ing in ingredients[1:]:
                result.append([ing, ""])

    return result

def save_csv(result, name):
    with open(name + ".csv", 'w') as opcsv:
        writer = csv.writer(opcsv)
        writer.writerow(["Nazwa_polska", "Nazwa_miedzynarodowa"])
        writer.writerows(result)

if __name__ == '__main__':
    path, name = parse_args()
    res = open_csv(path)
    result = create_list_for_table_with_duplicates(res)
    print(result)

    save_csv(result, name)
