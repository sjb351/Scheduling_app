from scheduleView.models import order, jobs
from input.models import product, proccessesList, machine, proccess
from datetime import datetime, timedelta
from django.utils import timezone
listOrders = order.objects.filter(completedOrder =False)

def printProduct():
    for orders in listOrders:
        productList = orders.productAdd.get()

def checkOrderComplete():
    orderList = order.objects.filter(completedOrder = False)

    for ord in range(orderList.count()):
        TFList =[]
        jobsInOrder = jobs.objects.filter(order = orderList[ord])
        for j in range(jobsInOrder.count()):
            TFList.append(jobsInOrder[j].completedJob)

        if all(TFList):
            orderList[ord].completedOrder = True
        else:
            orderList[ord].completedOrder = False

# def  updateJobDurations():
#     jobList = jobs.objects.filter(completed = False)
#     for j in range(jobList.count()):
#         jobList[j].

def updateTimesByCreated():
    checkOrderComplete()
    #updateJobDurations()
    #jobList = jobs.objects.filter(completed = False)
    orderList = order.objects.filter(completedOrder = False).order_by('createdTime')
    # startingTime = timezone.now()
    # maybe also set time current order started or next aviable work time
    nextTime = timezone.now()

    minOrder = orderList[0].idNumber
    num = 0
    x=[]
    for ord in range(orderList.count()):
        orderToSort = orderList[ord]
        jobListUse = jobs.objects.filter(order = orderToSort).order_by('-rank')
        
        if orderList[ord].idNumber == minOrder: #then this is the first order in list
            for j in range(jobListUse.count()):
                #jobListUse[j].startTime = nextTime
                pkj = jobListUse[j].pk
                endTimeTime = nextTime +(jobListUse[j].proccess.duration*jobListUse[j].quantity) + jobListUse[j].proccess.setUpTime + jobListUse[j].proccess.stopTime + jobListUse[j].delayTime
                jobs.objects.filter(pk = pkj).update(startTime = nextTime)
                jobs.objects.filter(pk = pkj).update(endTime = endTimeTime)
                nextTime = endTimeTime
        else:
            
            jobProcess = jobListUse[0].proccess
            if jobProcess: 
                jobCheck = jobs.objects.filter(order = oldOrder, proccess = jobProcess)
                if jobCheck:
                    lastJobEnd = jobCheck[0].endTime
                    endTimeTime = lastJobEnd + (jobListUse[0].proccess.duration*jobListUse[0].quantity) + jobListUse[0].proccess.setUpTime + jobListUse[0].proccess.stopTime + jobListUse[0].delayTime
                    pkj = jobCheck[0].pk
                    jobs.objects.filter(pk = pkj).update(startTime = nextTime)
                    jobs.objects.filter(pk = pkj).update(endTime = endTimeTime)
                    nextTime = endTimeTime
                    # print("new for" + str(jobCheck[0].pk))
                    # print(nextTime)
                    # print(jobCheck[0].endTime)

                for j in range(1, jobListUse.count()):
                    jobProcess = jobListUse[j].proccess
                    jobCheckend = jobs.objects.filter(order = oldOrder, proccess = jobProcess)[0].endTime
                    if jobCheckend > nextTime:
                        nextTime = jobCheckend
                        
                    pkj = jobListUse[j].pk
                    endTimeTime = nextTime +(jobListUse[j].proccess.duration*jobListUse[j].quantity) + jobListUse[j].proccess.setUpTime + jobListUse[j].proccess.stopTime + jobListUse[j].delayTime
                    jobs.objects.filter(pk = pkj).update(startTime = nextTime)
                    jobs.objects.filter(pk = pkj).update(endTime = endTimeTime)
                    nextTime = endTimeTime
                    num = num +1
                    # print("new for" + str(pkj))
                    # print(nextTime)
                    # print(jobs.objects.filter(pk = pkj)[0].endTime)

        oldOrder = orderToSort

    return x
            # set job start time after otherjob ends 
            # set job end time after other job ends

            




