"""
A collection of tools for dictionary, xlxs, and nddata support.
"""
import matlablike as pys


def xlsxToDict(sheet):#{{{
    """ this returns a dictionary of lists with the keys defined by the first row of values and the values of the dictionary defined by the values in each column.

    """
    paramDict = {}
    #headerCol = sheet.columns[0]
    #totalLen = len(headerCol) 
    for count,column in enumerate(sheet.columns):
        currentIndex = column[0].value
        if count == 0:
            totalLen = len(column)
        if currentIndex != None:
            print currentIndex
            valuesList = []
            for cell in column[1:totalLen]:
                curVal = cell.value
                print curVal
                valuesList.append(curVal)
            paramDict.update({currentIndex:valuesList})
        print 'cycling row'
    return paramDict#}}}

def makeNddata(paramDict, dataDim = 'kSigma', indepDim = 'site', errorDim = 'kSigma Error',selections=False):#{{{
    """ returns an nddata object and filters out values in list that are None. This should follow xlsxToDict.
    paramDict - dictionary - dict returned from xlsxToDict of a given data set.
    dataDim - string - name of column header in data file.
    indepDim - string - name of column header for the independent dimension. 
    errorDim - string - name of the column header for the error dimension of the data set.
    selections - dict - This limits the search to rows of data that match the selection. i.e. setting selections = {'Temperature':23} will return data sets that have a Temperature entry equal to 23. This supports multiple selections in typical dict format.
    """

    if selections:
        selectionDict = {}
        for key in selections.keys():
            selectionDict.update({key:paramDict.get(key)})
    data = paramDict.get(dataDim)
    indep = paramDict.get(indepDim)
    error = paramDict.get(errorDim)
    trueData = []
    trueIndep = []
    trueError = []
    for count,value in enumerate(data):
        if value != None:
            if selections:
                ### Currently this is only going to work for a single selection.
                for key in selectionDict.keys():
                    if selectionDict.get(key)[count] == selections.get(key):
                        appendData = True
                    else:
                        appendData = False
                        break
                if appendData:
                    print "This works"
                    trueData.append(data[count])
                    if indepDim:
                        trueIndep.append(indep[count])
                    if errorDim:
                        trueError.append(error[count])

            else:
                trueData.append(data[count])
                if indepDim:
                    trueIndep.append(indep[count])
                if errorDim:
                    trueError.append(error[count])
        else:
            break
    if indepDim:
        if errorDim:
            data = pys.nddata(pys.array(trueData)).rename('value',indepDim).labels(indepDim,pys.array(trueIndep)).set_error(pys.array(trueError))
        else:
            data = pys.nddata(pys.array(trueData)).rename('value',indepDim).labels(indepDim,pys.array(trueIndep))
    else:
        if errorDim:
            data = pys.nddata(pys.array(trueData)).set_error(pys.array(trueError))
        else:
            data = pys.nddata(pys.array(trueData))
    return data
#}}}
