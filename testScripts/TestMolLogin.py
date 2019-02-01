from action.PageAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
import time
import traceback
from util.Log import *


excelObj = ParseExcel()
excelObj.loadWorkBook(dataFilePath)


# 用例或用例步骤执行结束后，向Excel中写入执行结果信息
def writeTestResult(sheetObj, rowNo, colsNo, testResult, errorInfo=None, picPath=None):
    colorDict = {"pass": 'green', "fail": "red"}
    colsDict = {"testCase": [testCase_runTime, testCase_testResult],
                "caseStep": [testStep_runTime, testStep_testResult]
                }
    try:
        excelObj.writeCellCurrentTime(sheetObj, rowNo=rowNo, colsNo=colsDict[colsNo][0])
        excelObj.writeOfCell\
            (sheetObj, content=testResult, rowNo=rowNo, colsNo=colsDict[colsNo][1], style=colorDict[testResult])
        if errorInfo and picPath:
            excelObj.writeOfCell(sheetObj, content=errorInfo, rowNo=rowNo, colsNo=testStep_errorInfo)
            excelObj.writeOfCell(sheetObj, content=picPath, rowNo=rowNo, colsNo=testStep_errorPic)
        else:
            excelObj.writeOfCell(sheetObj, content="", rowNo=rowNo, colsNo=testStep_errorInfo)
            excelObj.writeOfCell(sheetObj, content="", rowNo=rowNo, colsNo=testStep_errorPic)
    except Exception as e:
        logging.debug("写excel出错，", traceback.print_exc())


def TestLoginMol():
    try:
        # 根据excelsheet名获取excel对象
        caseSheet = excelObj.getSheetByName("测试用例")
        isExecuteClumn = excelObj.getColumn(caseSheet, testCase_isExecute)
        # 记录执行成功的测试用例个数
        successfulCase = 0
        # 记录需要执行的用例个数
        requiredCase = 0
        for idx, i in enumerate(isExecuteClumn[1:]):
            # print(i.value)
            if i.value.lower() == "y":
                requiredCase += 1
                # 获取测试用例中第idx+2行数据
                caseRow = excelObj.getRow(caseSheet, idx+2)
                # 获取测试用例中第idx+2行的"步骤sheet名"
                caseStepSheetName = caseRow[testCase_testStepSheetName-1].value
                # print(caseStepSheetName)
                # 根据测试用例中的步骤sheet名获取测试步骤sheet对象
                stepSheet = excelObj.getSheetByName(caseStepSheetName)
                # 获取步骤sheet中步骤数
                stepNum = excelObj.getRowNumber(stepSheet)
                # print(stepNum)
                successfulSteps = 0
                logging.info("开始执行用例%s" % caseRow[testCase_testCaseName-1].value)
                for step in range(2, stepNum+1):
                    stepRow = excelObj.getRow(stepSheet, step)
                    # 获取关键字作为调用的函数名
                    keyWord = stepRow[testStep_keyWords-1].value
                    # 获取操作元素的定位方式作为调用的函数的参数
                    locationType = stepRow[testStep_locationType-1].value
                    # 获取操作元素的定位表达式作为调用的函数的参数
                    locationExpression = stepRow[testStep_locationExpression-1].value
                    # 获取操作值作为调用函数的参数
                    operateValue = stepRow[testStep_operateValue-1].value

                    # 将操作值为数字类型的数据转换成字符串类型，方便字符串连接
                    if isinstance(operateValue, int):
                        operateValue = str(operateValue)
                    print(keyWord, locationType, locationExpression, operateValue)
                    expressionStr = ""
                    # 构造需要执行的python语句
                    if keyWord and operateValue and locationType is None and locationExpression is None:
                        expressionStr = keyWord.strip()+"('"+operateValue+"')"

                    elif keyWord and operateValue is None and locationType is None and locationExpression is None:
                        expressionStr = keyWord.strip()+"()"

                    elif keyWord and locationType and locationExpression and operateValue:
                        expressionStr = keyWord.strip()+"('"+locationType.strip()+"','"+locationExpression.strip() + \
                        "','"+operateValue+"')"

                    elif keyWord and locationType and locationExpression and operateValue is None:
                        expressionStr = keyWord.strip()+"('"+locationType.strip()+"','"+locationExpression.strip()+"')"

                    try:
                        eval(expressionStr)
                        excelObj.writeCellCurrentTime(stepSheet, rowNo=step, colsNo=testStep_runTime)
                    except Exception as e:
                        capturePic = capture_screen()
                        errorInfo = traceback.format_exc()
                        writeTestResult(stepSheet, step, "caseStep", "fail", errorInfo, capturePic)
                        logging.info("步骤%s执行失败！" % stepRow[testStep_testStepDescribe-1].value)
                        raise e
                    else:
                        # 在测试步骤sheet中写入成功信息
                        writeTestResult(stepSheet, step, "caseStep", "pass")
                        successfulSteps += 1
                        logging.info("步骤%s执行通过！"% stepRow[testStep_testStepDescribe-1].value)
                if successfulSteps == stepNum-1:
                    writeTestResult(caseSheet, idx+2, "testCase", "pass")
                    successfulCase += 1
                else:
                    writeTestResult(caseSheet, idx+2, "testCase", "fail")
        logging.info("共%d条用例，%d条需要被执行，本次执行通过%d条"%(len(isExecuteClumn)-1, requiredCase, successfulCase))
    except Exception as e:
        print(traceback.print_exc())


if __name__ == '__main__':
    TestLoginMol()








