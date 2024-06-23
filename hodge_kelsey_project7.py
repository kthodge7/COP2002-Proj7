# Kelsey Hodge
# COP2002-0T1
# November 25th, 2022
# JSON Conversion Program
""" This program is designed to import and read information from a csv file
    in order to extract each row of data and convert it into proper JSON
    format to be used in JavaScript.
    """

class ConvertToJSON():
    """ Class with funtions to process an input csv file. Class methods
        will import, reorganize, and format data from the csv file into 
        header and data rows, and store the formatted data inside a
        dictionary. The data can be printed to the screen as well as
        written to a new file in proper JSON format.
        """
    
    def __init__(self, inputFile, outputFile):
        """ Initializes an instance of class ConvertToJSON with four
            attributes. Attributes are defined for an input file, an
            output file, and two empty lists to be used during
            data processing.
            """
        
        self.inputFile=inputFile
        self.outputFile=outputFile
        self.formattedHeaderList=[] # Empty list attribute to store formatted headers.
        self.listOfRows=[] # Empty list attribute to store row data.
        
       
    def readHeaders(self):
        """ Read first line of input file, separate the strings by comma,
            then add them to the header list and return the list.
            """     
        
        with open(self.inputFile, "r") as fileObject:
            headerRowList=[] # Empty list to store header data.
            headerRowString=fileObject.readline()

            # Split the string of headers and store values in a new list.
            headerRowList=headerRowString.split(",") 
           
        return headerRowList 

    def stripHeaderList(self):
        """ Remove whitespace from headers, store them in a new list,
            and return the list.
            """
        
        headerRowList=self.readHeaders()

        # New list to store headers stripped of whitespace.
        strippedHeaderList=[headerItem.strip() for headerItem in headerRowList] 

        return strippedHeaderList

    def formatHeaderList(self):
        """ Format all header items with surrounding double quotation marks.
            Add formatted headers to a new list, and return the list.
            """
        
        strippedHeaderList=self.stripHeaderList()
        for headerItem in strippedHeaderList:

            # Add formatting to all headers.
            formattedHeaderItem=("\""+headerItem+"\"")

            # Add formatted headers to a list attribute of the class instance.
            self.formattedHeaderList.append(formattedHeaderItem) 

        return self.formattedHeaderList

    def readRowStrings(self):
        """ Read lines from input file and store each line as a string
            into a new list. Return the list. """
        
        with open(self.inputFile, "r") as fileObject:
            listOfRowStrings=fileObject.readlines()

        return listOfRowStrings 


    def createListOfRows(self):
        """ Take string of each row, separate it by comma into a list,
            and store them in a new list of row data. Save each new list
            into a single list attribute of the class instance, and return the list.
            """

        listOfRowStrings=self.readRowStrings()

        # Determine number of row items to be processed by the length of their list.
        for i in range(1, len(listOfRowStrings)): # Start at index 1 to skip the header row.

            # Extract string from each row.
            singleRowString=listOfRowStrings[i]

            # Split the row string by comma.
            singleRowList=singleRowString.split(",")

            # Save split data into a list attribute of the class instance.
            self.listOfRows.append(singleRowList)
            
        return self.listOfRows

    def getSingleRowList(self):
        """ Extract and return the first row of list data from the list of rows.
            """
        
        listOfRows=self.createListOfRows()
        singleRowList=listOfRows[0]
                
        return singleRowList

    def removeRowWhiteSpace(self):
        """ Remove whitespace from row items, store them in a new list,
            and return the list.
            """
        
        singleRowList=self.getSingleRowList()
        singleStrippedRow=[rowItem.strip() for rowItem in singleRowList]

        return singleStrippedRow


    def formatNonStrings(self):
        """ Apply formatting to row items depending on which condition
            the value meets.
            """
        
        singleStrippedRow=self.removeRowWhiteSpace()
        fullyFormattedRow=[] # New list to store formatted row data.

        for rowItem in singleStrippedRow:

            # try-except block checks if row item can be reassigned
            # as an integer value, and upon success appends the row
            # item as an integer to a new list. If a ValueError is
            # raised, the data is checked against different conditions
            # and formatted appropriately for JSON depending on which 
            # condition is met. The processed and formatted row item is 
            # appended to a new list, and the list is returned.
            try:
                rowItem=int(rowItem)
            except ValueError:

                # Converts strings to lowercase for JSON compatibility.
                if(rowItem=="True" or rowItem=="False"):
                    rowItemLower=rowItem.lower()
                    fullyFormattedRow.append(rowItemLower)

                # Add double quotations around strings for JSON compatibility.
                if(rowItem!="true" and rowItem!="false" and rowItem!="null"):
                    rowItem=("\""+rowItem+"\"")
                    fullyFormattedRow.append(rowItem)

                # Remove double quotation marks from around string for JSON compatibility.
                if(rowItem=="null"):
                    rowItem.replace("\"", "")
                    fullyFormattedRow.append(rowItem)
            else:
                fullyFormattedRow.append(int(rowItem))

        return fullyFormattedRow
    
    def createRowDictionary(self):
        """ Get list representing a single row and match each list
            item with a corresponding header value into a key:value pair.
            Then add this key:value pair to a new dictionary and return
            the dictionary.
            """
        
        fullyFormattedRow=self.formatNonStrings()
        rowDictionary={} # Empty dictionary to hold header and row data as key-value pairs.

        # Determine number of row items to be processed by the length of the class instance header list.
        for i in range(0, len(self.formattedHeaderList)):

            # Extract value from list of header items and list of row items at the index of variable i.
            headerRowItem=self.formattedHeaderList[i]
            singleRowItem=fullyFormattedRow[i]

            # Add extracted values as a key-value pair to a new dictionary.
            rowDictionary[headerRowItem]=singleRowItem

        return rowDictionary

    def preformatForPrint(self):
        """ Add double quotation marks around, and a trailing comma to
            the end of all key:value pairs in the dictionary. Specific
            formatting is determined by try-except block. Concatenate
            each formatted key:value pair into a single line of key:value
            pairs, and return the new string.
            """
        
        rowDictionary=self.createRowDictionary()
        rowString="" # Empty string to hold all key:value pair strings.
        
        for headerItem, rowItem in rowDictionary.items():

            # try-except block checks if the key:value pair can be
            # formatted into a string without raising a TypeError.
            # Upon success the pair is formatted for JSON and concatenated
            # to a string. If a TypeError is raised, the integer row item
            # is defined as a string, the pair is formatted for JSON, and
            # concatenated to the string.
            try:
                rowString1=(""+headerItem+":"+rowItem+",")
            except TypeError:
                rowString1=(""+headerItem+":"+str(rowItem)+",")
            else:
                rowString1=(""+headerItem+":"+rowItem+",")
                
                
            rowString+=rowString1 # Concatenate formatted key:value pair string to the new string.
            
        return rowString

    def formatForPrint(self):
        """ Applies final formatting to the row of data being processed,
            prints the data to the screen, and writes it to a new output
            file with correct JSON formating. The first row of data in 
            the list of rows is deleted, and class methods are repeated
            the same number of times as the original length of the list
            of rows.
            """
        
        listOfRows=self.createListOfRows()

        # Variable to set the condition of the while loop.
        lengthListOfRows=len(listOfRows)

        # Variable to set the condition of the while loop.
        i=0

        # Variable used to represent an incrementing value for the print
        # statement.
        j=1 
        
        with open (self.outputFile, "a") as fileObject:

            # While loop will run until it has processed all rows from the file.
            while(i<lengthListOfRows):
                
                printToScreen=self.preformatForPrint()

                # Remove the trailing comma from row string for proper
                # JSON formatting.
                printToScreen=printToScreen[:-1] 

                # Header list items are formatted with surrounding
                # double quotes for JSON compatibility.
                if(i==0):

                    # Header string begins with a curly bracket.
                    print("{\""+str(j)+"\":{"+printToScreen+"}") 
                    fileObject.write("{\""+str(j)+"\":{"+printToScreen+"}")

                # Row lists are formatted for JSON compatibility.
                else:

                    # Row string begins with a comma.
                    print(",\""+str(j)+"\":{"+printToScreen+"}") 

                    # New line is added before each new string is written
                    # to the output file.
                    fileObject.write("\n,\""+str(j)+"\":{"+printToScreen+"}") 

                # After the row has been printed and written, the row is deleted.
                del listOfRows[0] 
                i+=1
                j+=1

            # Curly bracket written to output file on a new line after all data has been written.    
            fileObject.write("\n}")

            # Curly bracket printed on a new line after all data has been printed.
            print("}") 
        
def main():
    userFile=input("Enter the filename:  ")
    
    conversionObject=ConvertToJSON(userFile, "Project7Output.txt")
    formattedHeaderlist=conversionObject.formatHeaderList()
    conversionObject.formatForPrint()
    print("\nOutput written to "+conversionObject.outputFile)         

if __name__=="__main__":
    main()
