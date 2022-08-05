import csv
import dataclasses
from dataclasses import dataclass
from random import randint

FILENAME = 'engagements.csv'


class Engagements:
    # Datatypes
    @dataclass
    class CSVStruct:
        x: int = 0
        y: int = 0
        friendlyCasualties: int = 0
        enemyCasualties: int = 0

        # Function which defines how we print
        def __str__(self):
            output_string = ""
            for field in dataclasses.fields(self):
                output_string += f"{field.name} = {getattr(self, field.name)}\t"
            return output_string

    def GenerateCSV(self):
        csv_list = []
        for i in range(100):
            arg_list = []
            # Generating argument list dynamically
            for field in dataclasses.fields(self.CSVStruct):
                arg_list.append(field.type(randint(0, 100)))
            temp_csv = self.CSVStruct(randint(0, 50), randint(0, 50), randint(0, 100), randint(0, 100))
            csv_list.append(temp_csv)
        # Creating file everytime we open, we close
        csv_file = open(FILENAME, 'w+', newline='')  # newline is blank as csvfile adds it
        csv_writer = csv.writer(csv_file, dialect='excel')

        # Getting column names
        row_names = {field.name: field.type for field in dataclasses.fields(self.CSVStruct)}

        # Writing column names to files
        csv_writer.writerow(row_names)

        # Writing rows
        for i in csv_list:
            csv_writer.writerow([i.x, i.y, i.enemyCasualties, i.friendlyCasualties])

        # We close the file here, DO NOT FORGET
        csv_file.close()

    def ReadCSV(self) -> list[CSVStruct]:
        # opening file
        csv_file = open(FILENAME, 'r+')
        reader = csv.reader(csv_file, dialect='excel')

        engagements = []

        # getting count of variables in our csv file
        colums = [field.type for field in
                  dataclasses.fields(self.CSVStruct)]  # Getting a list of types for each variable
        collum_count = colums.__len__()

        # looping through each row
        for row in reader:
            # converting to struct
            try:
                args = []
                for i in range(collum_count):
                    args.append(colums[i](row[i]))  # This syntax is wierd, but this converts the variable to our type
                    int('1')
                engagements.append(self.CSVStruct(*args))
            except:
                continue
        # Always remember to close file!
        csv_file.close()

        return engagements

    def FindMostDangerousAllyZone(self, engagements: list[CSVStruct]) -> list[CSVStruct]:

        most_dangerous = self.CSVStruct()

        # Used if we have multiple
        most_dangerous_list = []
        for engagement in engagements:
            # checking equality
            # if same number of casualties as current most dang
            if engagement.friendlyCasualties == most_dangerous.friendlyCasualties:
                most_dangerous_list.append(engagement)

            # Means we find most dangerous
            if engagement.friendlyCasualties > most_dangerous.friendlyCasualties:
                most_dangerous = engagement
                # need to reset list since new most dangerous
                most_dangerous_list = [engagement]

        return most_dangerous_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Creates the class
    engagements = Engagements()

    # Generates the file with random data
    engagements.GenerateCSV()

    # Contains all of our engagements from the file
    engagementList = engagements.ReadCSV()
    for i in engagements.FindMostDangerousAllyZone(engagementList):
        print(i)
