"""
A collection of tools for dictionary, xlxs, and nddata support.
"""
import matlablike as pys


def xlsxToDict(sheet):#{{{
    """ this returns a dictionary of lists with the keys defined by the first row of values and the values of the dictionary defined by the values in each column.

    """
    paramDict = {}
    headerCol = sheet.columns[0]
    totalLen = len(headerCol) 
    for count,column in enumerate(sheet.columns):
        currentIndex = column[0].value
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

def makeNddata(paramDict, dataDim = 'kSigma', indepDim = 'site', errorDim = 'kSigma Error'):#{{{
    """ returns an nddata object and filters out values in list that are None. This should follow xlsxToDict.
    paramDict - dictionary - dict returned from xlsxToDict of a given data set.
    dataDim - string - name of column header in data file.
    indepDim - string - name of column header for the independent dimension. 
    errorDim - string - name of the column header for the error dimension of the data set.
    """
    data = paramDict.get(dataDim)
    indep = paramDict.get(indepDim)
    error = paramDict.get(errorDim)
    trueData = []
    trueIndep = []
    trueError = []
    for count,value in enumerate(data):
        if value != None:
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

