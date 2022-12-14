from scheduleView.models import order, job
from input.models import product, proccessesList, machine, procces, worker
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg, Max, Min
from itertools import permutations
import math, json
import numpy as np
from scheduleView.serilizer import DateTimeEncoder

listOrders = order.objects.filter(completedOrder =False)

def printProduct():
    for orders in listOrders:
        productList = orders.productAdd.get()

def checkOrderComplete():
    orderList = order.objects.filter(completedOrder = False)

    for ord in range(orderList.count()):
        TFList =[]
        jobsInOrder = job.objects.filter(order = orderList[ord])
        for j in range(jobsInOrder.count()):
            TFList.append(jobsInOrder[j].completedJob)

        if all(TFList):
            orderList[ord].completedOrder = True
        else:
            orderList[ord].completedOrder = False

def resetMachineWorker():
    # rest all machine and worker alocation to null to update listing 
    jobList = job.objects.filter(completedJob = False, startedJob = False)
    for i in range(jobList.count()):
        jobList[i].worker.clear()
        jobList[i].machine.clear()

def in_range(start, end, newStart, newEnd):
    #"""Returns whether current is in the range [start, end]"""
    return start <= newStart <= end or start <= newEnd <= end 

def suround_range(start, end, newStart, newEnd):
    #"""Returns whether current is in the range [start, end]"""
    return newStart <= start and end <= newEnd

def job_clash(start, end, newStart, newEnd):
    return in_range(start, end, newStart, newEnd) or suround_range(start, end, newStart, newEnd)


def findWorkers(procc, startTime):
    timeArray =[]
    PPT = procc.WorkerpostProcessTime
    SUT = procc.WorkerSetUpTime
    workerList = worker.objects.filter(proccessTrainedFor=procc) #all workers who can do job
    if procc.automated == False:
        for workers in workerList:
            jobWork = job.objects.filter(completedJob = False, startedJob = False, worker = workers).order_by('-endTime')
            # find the last job end time because worker will be needed for all operation time
            if jobWork.count() > 0:
                latestJob = jobWork.latest('endTime')
                newData = json.loads(latestJob.workData)
                for new in newData:
                    if workers.name in new:
                        workFreeTime = datetime.fromisoformat(new[workers.name]["end"])
                        timeAviable = workFreeTime
            else:
                timeAviable = startTime 
            timeArray.append(timeAviable)
    else: # Job can be automated worker only needed at end and start
        preTime = procc.WorkerSetUpTime
        postTime = procc.WorkerpostProcessTime
        leng = procc.duration
        for workers in workerList:
            jobWork = job.objects.filter(completedJob = False, startedJob = False, worker = workers).order_by('-endTime')
            data =[]
            if jobWork.count() > 0: # if list of jobs is more than 0
                for jobs in jobWork:
                    # find first job first
                    newData = json.loads(jobs.workData)
                    for new in newData:
                        if workers.name in new:
                            busyStart1 = datetime.fromisoformat(new[workers.name]["start"])
                            busyend1 = datetime.fromisoformat(new[workers.name]["endSetUp"])
                            busyStart2 = datetime.fromisoformat(new[workers.name]["startPost"])
                            busyend2 = datetime.fromisoformat(new[workers.name]["end"])
                            # set new set up time
                            if (busyStart2 - busyend1) > leng:
                                data.append([busyStart1, busyend1])
                                data.append([busyStart2, busyend2])
                            else:
                                data.append([busyStart1, busyend2])

                start1 = data[0][1]
                end1 = data[0][1] + preTime
                start2 = data[0][1] + preTime + leng
                end2 =  data[0][1] + preTime + leng +postTime
                timeAviable = start1 = data[0][1]
                for d in data:
                    check1 = job_clash(d[0], d[1], start1, end1)
                    check2 = job_clash(d[0], d[1], start2, end2)
                    if not check1 and not check2:
                        # no clash with times
                        timeAviable = d[1]
                    else: 
                        start1 = d[1]
                        end1 = d[1] + preTime
                        start2 = d[1] + preTime + leng
                        end2 =  d[1] + preTime + leng +postTime
            else:
                timeAviable = startTime 
            timeArray.append(timeAviable)
    return list(workerList),  list(timeArray)


def findMachines(procc, startTime):
    timeArray =[]
    machineList = machine.objects.filter(proccessFor=procc)
    for mach in machineList:
        jobWork = job.objects.filter(completedJob = False, startedJob = False, machine = mach) #.order_by('startTime')
        if jobWork.count() > 0:
            latestJob = jobWork.latest('endTime')
            newData = json.loads(latestJob.machData)
            for new in newData:
                if mach.name in new:
                    machFreeTime = datetime.fromisoformat(new[mach.name]["end"])
            timeAviable = machFreeTime 
        #addTo = [mach, avaible, timeAviable]
        else:
            timeAviable = startTime 
        timeArray.append(timeAviable)
        #machineChoice.append(addTo)
    return list(machineList),  list(timeArray)


def minPossibleMachines(procc):
    machineNum = machine.objects.filter(proccessFor=procc).count()
    workerNum = worker.objects.filter(proccessFor=procc).count()
    if procc.automated == False:
        return min(machineNum,workerNum)
    else:
        return machineNum

def combinationSum(jobTarget, machNum):
    if machNum > 6:
        print("Too many machines the process will be very slow")
    elif jobTarget > 20:
        print("Too manu jobs to calcuate optimum")
    else:
        ans = []
        temp = [0]*machNum
        findNumbers(ans, jobTarget, 0, temp, 0, machNum, 0)
        new =[]
        for li in ans:
             ne = list(li)
             new.append(ne)
        return new
 
def findNumbers(ans, target, start, temp, summ, machNum, index):
    summ = sum(temp)
    if(summ == target):
        l = list(permutations(temp))
        for j in l:
            ans.append(j)
        return
       
    for i in range(start, target):
        if(summ - i) <= target and index <= machNum-1:
 
            temp[index] = i
            newStart = i 
            findNumbers(ans, target, newStart, temp, summ-i, machNum, index + 1)
 
            temp[index] = 0

def findOptimumCombination(mach, timeAviable, quant, jobLeng):
    machNum = len(mach)
    if machNum == 1:
        combin = [quant]
        bestC = combin[0]
    elif machNum == 0:
        print("No machines aviable for this process")
        return
    else:
        jobTarget = quant
        combin = combinationSum(jobTarget, machNum)
        #print("str for combine " + str(combin[0]))
    
        bestC = combin[0]
        bestFinish = np.array(timeAviable) + np.array(bestC)*jobLeng
        for c in combin:
            finishTime = np.array(timeAviable) + np.array(c)*jobLeng
            prevMax = max(bestFinish)
            newMax =  max(finishTime) 
            if newMax < prevMax:
                bestFinish = finishTime
                bestC = c
    
    return bestC
    

def checkLength(value):
    if type(value)==list or isinstance(value, np.ndarray):
        l = len(value)
    elif value == None:
        l = 0
    else:
        l = 1
    return l

def updateTimesByCreated():
    checkOrderComplete()
    orderList = order.objects.filter(completedOrder = False).order_by('createdTime')
    firstOrderPk = orderList[0].pk
    resetMachineWorker()
    # startingTime = timezone.now()
    # maybe also set time current order started or next aviable work time
    if orderList.count()> 0:
        lastJobEnd = timezone.now()
        startTime = timezone.now()
        x=[]
        for ord in range(orderList.count()):
            orderToSort = orderList[ord]
            jobListUse = job.objects.filter(order = orderToSort).order_by('rank')
            for j in range(jobListUse.count()):
                # cylce through each job on the schedule 
                pkj = jobListUse[j].pk
                proc = jobListUse[j].proccess
                auto = jobListUse[j].proccess.automated
                if j==0:  # first job in list 
                    lastJobEnd = startTime
                #quant = math.ceil(jobListUse[j].quantity/minPossibleMachines(proc))
                jobLength = proc.duration + proc.WorkerpostProcessTime + proc.WorkerSetUpTime
                mach, timeAviable = findMachines(proc, lastJobEnd)
                workLis, timeAviableWork = findWorkers(proc, lastJobEnd)
                timeFinal = []
                #print(timeAviable)
                #print(timeAviableWork)

                numMach = len(mach)
                workNum = len(workLis)
                
                workZip = sorted(zip(timeAviableWork, workLis), key=lambda x: x[0])
                machZip = sorted(zip(timeAviable, mach), key=lambda x: x[0])
                workList = []
                machList = []
                fullList = [] # worker name, machine name, best time (latest time avibale)
                if not proc.automated:
                    numberProcc = min(workNum, numMach)
                    for i in range(numberProcc):
                        z = workZip[i][1]
                        y = machZip[i][1]
                        t = max(workZip[i][0], machZip[i][0])
                        fullList.append([z, y, t])

                    machList = machZip[0:numberProcc - 1]
                elif proc.automated and workNum >= numMach:
                    numberProcc = numMach
                    for i in range(numberProcc):
                        z = workZip[i][1]
                        y = machZip[i][1]
                        t = max(workZip[i][0], machZip[i][0])
                        fullList.append([z, y, t])
                    
                else:  # automated process and more machines than worker
                    # cycle through to assign times for each mach
                    numextras = math.ceil(numMach/workNum)
                    timeAdd = proc.WorkerSetUpTime
                    lengEnd = numMach
                    workList = []
                    machList = []
                    #workList = setTimearray(workZip, timeAdd , numextras, lengEnd)
                    #machList = setTimearray(machZip, timeAdd , numextras, lengEnd)
                    for i in range(numextras):
                        arrAddW = [[item[0] + timeAdd*i, item[1]] for item in workZip]
                        workList = workList + arrAddW
                    workList = workList[0:lengEnd]
                    machList = machZip

                    for i in range(lengEnd):
                        z = workList[i][1]
                        y = machList[i][1]
                        t = max(workList[i][0], machList[i][0])
                        fullList.append([z, y, t])
                
                if j == 0 and orderToSort.pk == firstOrderPk:  # if first order to be made 
                    diff = startTime - fullList[0][2] 
                    for data in fullList:
                        data[2] = data[2] + diff
                
                elif j > 0:  # all other jobs in list 
                    diff = lastJobEnd - fullList[0][2] 
                    for data in fullList:
                        data[2] = data[2] + diff
                else:
                    print("no change")

                timeFinal = [item[2] for item in fullList]
                machList = [item[1] for item in fullList]
                workList = [item[0] for item in fullList]

                numParall = 0
                for m in machList:
                    if m.numberParral > 1:
                        numParall = numParall + m.numberParral
                if numParall == 0: numParall = 1

                inQuant =  math.ceil(jobListUse[j].quantity/numParall)
                quant =  findOptimumCombination(machList, timeFinal, inQuant, jobLength)
                finishTime = np.array(timeFinal) + np.array(quant)*jobLength

                statingTimeAuto =[]
                timeSetUpend = []
                timeStartPost = []
                endTimeAuto = []
                longMachList =[]
                longWorkList =[]
                infoList =[]
                l = checkLength(quant)

                if proc.automated == True:
                    for ind in range(l):
                        if l == 1:
                            q = quant
                        else:
                            q = quant[ind]
                        for i in range(q):
                            #copyDict = data2.copy() 
                            #data.append(copyDict)                 
                            longMachList.append(machList[ind])
                            longWorkList.append(workList[ind])
                            infoList.append(str(machList[ind].name) + " "+ str(l) + " and job number" +str(i))
                            statingTimeAuto.append(timeFinal[ind] + i*jobLength)
                            timeSetUpend.append(timeFinal[ind] + i*jobLength + proc.WorkerSetUpTime)
                            timeStartPost.append(timeFinal[ind] + i*jobLength + jobLength - proc.WorkerpostProcessTime)
                            endTimeAuto.append(timeFinal[ind] + i*jobLength + jobLength)

                else:        # not automated no need for time set up and post processing these are set to end and start times
                    for ind in range(l):
                        if l == 1:
                            q = quant
                        else:
                            q = quant[ind]
                        for i in range(q):
                            longMachList.append(machList[ind])
                            longWorkList.append(workList[ind])
                            infoList.append(str(machList[ind].name) +" "+ str(l) + " and job number" +str(i))
                            statingTimeAuto.append(timeFinal[ind] + i*jobLength)
                            timeSetUpend.append(timeFinal[ind] + i*jobLength + jobLength)
                            timeStartPost.append(timeFinal[ind] + i*jobLength)
                            endTimeAuto.append(timeFinal[ind] + i*jobLength + jobLength)

                if len(list(timeFinal)) > 1:
                    jobstart = min(statingTimeAuto)
                    jobend = max(endTimeAuto)
                else:
                    jobstart = statingTimeAuto
                    jobend = endTimeAuto
                
                if type(jobstart) == list or isinstance(jobstart, np.ndarray):
                    jobstart = jobstart[0]
                if type(jobend) == list or isinstance(jobend, np.ndarray):
                    jobend = jobend[0]
                # write all info for job and machine in json file 
                machFile = []
                workFile = []
                newJob = job.objects.filter(pk = pkj)

                for index, machin in enumerate(longMachList):
                    x = (jobstart - statingTimeAuto[index]).total_seconds()
                    yy ={}
                    yy[machin.name] = {}
                    dictAdd = {'seconds': x, 'start': statingTimeAuto[index], 'end': endTimeAuto[index], 'order': orderToSort.pk, 'info': infoList[index], 'worker': longWorkList[index].name}
                    yy[machin.name].update(dictAdd)
                    copyDict2 = yy.copy()
                    machFile.append(copyDict2)
                    newJob[0].machine.add(machin)

                for index, work in enumerate(longWorkList):
                    x = (jobstart - statingTimeAuto[index]).total_seconds()
                    y = {}
                    y[work.name] ={}
                    dictAdd = {'seconds': x, 'start': statingTimeAuto[index], 'end': endTimeAuto[index], 'automated': auto, 'endSetUp': timeSetUpend[index], 'startPost': timeStartPost[index], 'order': orderToSort.pk, 'info': infoList[index], 'mach': longMachList[index].name}
                    y[work.name].update(dictAdd)
                    copyDict = y.copy()
                    workFile.append(copyDict)
                    newJob[0].worker.add(work)
                jD = json.dumps(machFile, cls=DateTimeEncoder)
                wD = json.dumps(workFile, cls=DateTimeEncoder)
                newJob.update(startTime = jobstart, endTime = jobend, machData = jD, workData = wD)

                lastJobEnd = jobend
                if j == 0:
                    startTime = jobend
            oldOrder = orderToSort

        return x
            # set job start time after otherjob ends 
            # set job end time after other job ends

            
def updateOrderTime():
    orderList = order.objects.filter(completedOrder = False)
    for ord in range(orderList.count()):
        orderToSort = orderList[ord]
        jobList = job.objects.filter(order = orderToSort)
        minTime = jobList.aggregate(Min('startTime'))
        maxTime = jobList.aggregate(Max('endTime'))
        orderToSort.startedTime = minTime['startTime__min']
        orderToSort.endTime = maxTime['endTime__max']
        orderToSort.save()
    return


