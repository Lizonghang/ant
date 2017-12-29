# -*- coding: UTF-8 -*-
'''
程序主体：
类BACA的实例化->类BACA的初始化->执行BACA.ReadCityInfo()方法->执行BACA.Search()方法->执行BACA.PutAnts()方法
->类ANT的初始化->类ANT的实例化->执行ANT.MoveToNextCity()方法->执行ANT.SelectNextCity()方法->执行ANT.AddCity()方法
->执行ANT.UpdatePathLen()方法->执行BACA.UpdatePheromoneTrail()方法

蚁群算法中关键两个问题，一个是选择下一个城市的算法，主要在ANT.SelectNextCity(self, alpha, beta)方法中，其中alpha为表征
信息素重要程度的参数，beta为表征启发式因子重要程度的参数；而更新信息素主要在BACA.UpdatePheromoneTrail(self)方法中。
'''

import os, sys, random#调入基本的python模块
from math import *
BestTour = []#用于放置最佳路径选择城市的顺序
CitySet = set()#sets数据类型是个无序的、没有重复元素的集合，两个sets之间可以做差集，即在第一个集合中移出第二个集合中也存在的元素
CityList = []#城市列表即存放代表城市的序号
PheromoneTrailList = []#信息素列表（矩阵）
PheromoneDeltaTrailList = []#释放信息素列表（矩阵）
CityDistanceList = []#两两城市距离列表(矩阵)
AntList = []#蚂蚁列表
class BACA:#定义类BACA，执行蚁群基本算法
    def __init__(self, cityCount=51, antCount=51, q=80, alpha=1, beta=3, rou=0.4, nMax=100):
        #self, cityCount=51, antCount=50, q=80, alpha=2, beta=5, rou=0.3, nMax=40
        #初始化方法，antCount为蚂蚁数，nMax为迭代次数
        self.CityCount = cityCount#城市数量，本例中为手工输入，也可以根据城市数据列表编写程序获得
        self.AntCount = antCount#蚂蚁数量
        self.Q = q#信息素增加强度系数
        self.Alpha = alpha#表征信息素重要程度的参数
        self.Beta = beta#表征启发因子重要程度的参数
        self.Rou = rou#信息素蒸发系数
        self.Nmax = nMax#最大迭代次数
        self.Shortest = 10e6#初始最短距离应该尽可能大，至少大于估算的最大城市旅行距离
        random.seed()#设置随机种子
        #初始化全局数据结构及值
        for nCity in range(self.CityCount):#循环城市总数的次数（即循环range(0,51),为0-50，不包括51）
            BestTour.append(0)#设置最佳路径初始值均为0
        for row in range(self.CityCount):#再次循环城市总数的次数
            pheromoneList = []#定义空的信息素列表
            pheromoneDeltaList = []#定义空的释放信息素列表
            for col in range(self.CityCount):#循环城市总数的次数
                pheromoneList.append(100)#定义一个城市到所有城市路径信息素的初始值
                pheromoneDeltaList.append(0)#定义一个城市到所有城市路径释放信息素的初始值
            PheromoneTrailList.append(pheromoneList)#建立每个城市到所有城市路径信息素的初始值列表矩阵
            PheromoneDeltaTrailList.append(pheromoneDeltaList)#建立每个城市到所有城市路径释放信息素的初始值列表矩阵

    def ReadCityInfo(self, fileName):#定义读取城市文件的方法
        file = open(fileName)#打开城市文件
        for line in file.readlines():#逐行读取文件
            cityN, cityX, cityY = line.split()#分别提取城市序号、X坐标和Y坐标，使用空格切分
            CitySet.add(int(cityN))#在城市集合中逐步追加所有的城市序号
            CityList.append((int(cityN), float(cityX), float(cityY)))#在城市列表中逐步追加每个城市序号、X坐标和Y坐标建立的元组
        for row in range(self.CityCount):#循环总城市数的次数
            distanceList = []#建立临时储存距离的空列表
            for col in range(self.CityCount):
                distance = sqrt(pow(CityList[row][1]-CityList[col][1], 2) + pow(CityList[row][2]-CityList[col][2], 2))#逐一计算每个城市到所有城市的距离值
                distance = round(distance)
                distanceList.append(distance)#追加一个城市到所有城市的距离值
            CityDistanceList.append(distanceList)#追加么个城市到所有城市的距离值，为矩阵，即包含子列表
        file.close()#关闭城市文件

    def PutAnts(self):#定义蚂蚁所选择城市以及将城市作为参数定义蚂蚁的方法和属性
        AntList.clear() # 先清空列表
        for antNum in range(self.AntCount):#循环蚂蚁总数的次数
            city = random.randint(1, self.CityCount)#随机选择一个城市
            ant = ANT(city)#蚂蚁类ANT的实例化，即将每只蚂蚁随机选择的城市作为传入的参数，使之具有ANT蚂蚁类的方法和属性
            AntList.append(ant)#将定义的每只蚂蚁追加到列表中

    def Search(self):#定义搜索最佳旅行路径方法的主程序
        for iter in range(self.Nmax):#循环指定的迭代次数
            self.PutAnts()#执行self.PutAnts()方法，定义蚂蚁选择的初始城市和蚂蚁具有的方法和属性
            for ant in AntList:#循环遍历蚂蚁列表，由self.PutAnts()方法定义获取
                for ttt in range(len(CityList)):#循环遍历城市总数次数
                    ant.MoveToNextCity(self.Alpha, self.Beta)#执行蚂蚁的ant.MoveToNextCity()方法，获取蚂蚁每次旅行时的旅行路径长度CurrLen，禁忌城市城市列表TabuCityList等属性值
                ant.two_opt_search()#使用邻域优化算法    $$$
                ant.UpdatePathLen()#使用ant.UpdatePathLen更新蚂蚁旅行路径长度
            tmpLen = AntList[0].CurrLen#将蚂蚁列表中第一只蚂蚁的旅行路径长度赋值给新的变量tmplen
            tmpTour = AntList[0].TabuCityList#将获取的蚂蚁列表的第一只蚂蚁的禁忌城市列表赋值给新的变量tmpTour
            for ant in AntList[1:]:#循环遍历蚂蚁列表，从索引值1开始，除第一只外
                if ant.CurrLen < tmpLen:#如果循环到的蚂蚁旅行路径长度小于tmpLen即前次循环蚂蚁旅行路径长度，开始值为蚂蚁列表中第一只蚂蚁的旅行路径长度
                    tmpLen = ant.CurrLen#更新变量tmpLen的值
                    tmpTour = ant.TabuCityList#更新变量tmpTour的值，即更新禁忌城市列表
            if tmpLen < self.Shortest:#如果从蚂蚁列表中获取的最短路径小于初始化时定义的长度
                self.Shortest = tmpLen#更新旅行路径最短长度
                BestTour = tmpTour #更新初始化时定义的最佳旅行城市次序列表
            print(iter,":",self.Shortest,":",BestTour)#打印当前迭代次数、最短旅行路径长度和最佳旅行城市次序列表
            self.UpdatePheromoneTrail()#完成每次迭代需要使用self，UpdatePheromoneTrail()方法更新信息素

    def UpdatePheromoneTrail(self):#定义更新信息素的方法，需要参考前文对于蚁群算法的阐述
        for ant in AntList:#循环遍历蚂蚁列表
            for city in ant.TabuCityList[0:-1]:#循环遍历蚂蚁的禁忌城市列表
                idx = ant.TabuCityList.index(city)#获取当前循环 禁忌城市的索引值
                nextCity = ant.TabuCityList[idx+1]#获取当前循环禁忌城市紧邻的下一个禁忌城市
                PheromoneDeltaTrailList[city-1][nextCity-1] += self.Q / ant.CurrLen
                #逐次更新释放信息素列表，注意矩阵行列所代表的意义，[city-1]为选取的子列表即当前城市与所有城市间路径的
                #释放信息素值，初始值均为0，[nextCity-1]为在子列表中对应紧邻的下一个城市，释放信息素为Q，信息素增加强度
                #系数与蚂蚁当前旅行路径长度CurrLen的比值，路径长度越小释放信息素越大，反之则越小。
                PheromoneDeltaTrailList[nextCity-1][city-1] += self.Q / ant.CurrLen
                #在二维矩阵中，每个城市路径均出现两次，分别为[city-1]对应的[nextCity-1]和[nextCity-1]对应的[city-1]，因此都需要更新，
                #注意城市序列因为从1开始，而列表索引值均从0开始，所以需要减1
            lastCity = ant.TabuCityList[-1]#获取禁忌城市列表的最后一个城市
            firstCity = ant.TabuCityList[0]#获取禁忌城市列表的第一个城市
            PheromoneDeltaTrailList[lastCity-1][firstCity-1] += self.Q / ant.CurrLen
            #因为蚂蚁旅行需要返回开始的城市，因此需要更新禁忌城市列表最后一个城市到第一个城市旅行路径的释放信息素值，即最后一个城市对应第一个城市的释放信息素值
            PheromoneDeltaTrailList[firstCity-1][lastCity-1] += self.Q / ant.CurrLen
            #同理更新第一个城市对应最后一个城市的释放信息素值
        for (city1, city1X, city1Y) in CityList:#循环遍历城市列表，主要是提取city1即城市的序号
            for (city2, city2X, city2Y) in CityList:#再次循环遍历城市列表，主要是提取city2即城市序号，循环两次的目的仍然是对应列表矩阵的数据结构
                PheromoneTrailList[city1-1][city2-1] = ( (1-self.Rou)*PheromoneTrailList[city1-1][city2-1] + PheromoneDeltaTrailList[city1-1][city2-1] )
                PheromoneDeltaTrailList[city1-1][city2-1] = 0#将释放信息素列表值再次初始化为0，用于下次循环
####    print(PheromoneTrailList)

class ANT:#定义蚂蚁类，使得蚂蚁具有相应的方法和属性
    def __init__(self, currCity = 0):#蚂蚁类的初始化方法，默认传入当前城市序号为0
        self.TabuCitySet = set()
        #定义禁忌城市集合，定义集合的目的是集合本身要素不重复并且之间可以做差集运算，例如AddCity()方法中
        #self.AllowedCitySet = CitySet - self.TabuCitySet，可以方便地从城市集合中去除禁忌城市列表的城市，获取允许的城市列表
        self.TabuCityList = []#定义禁忌城市空列表
        self.AllowedCitySet = set()#定义允许城市集合
        self.TransferProbabilityList = []#定义城市选择可能性列表
        self.CurrCity = 0 #定义当前城市初始值为0
        self.CurrLen = 0.0#定义当前旅行路径长度
        self.AddCity(currCity)#执行AddCity()方法，获取每次迭代的当前城市CurrCity、禁忌城市列表TabuCityList和允许城市列表AllowedCitySet的值
        pass#空语句，此行为空，不运行任何操作

    def SelectNextCity(self, alpha, beta):#定义蚂蚁选择下一个城市的方法，需要参考前文描述的蚁群算法
        if len(self.AllowedCitySet) == 0:#如果允许城市集合为0，则返回0
            return (0)
        sumProbability = 0.0#定义概率，可能性初始值为0
        self.TransferProbabilityList = []#建立选择下一个城市可能性空列表
        for city in self.AllowedCitySet:#循环遍历允许城市集合
            sumProbability = sumProbability + (
                pow(PheromoneTrailList[self.CurrCity-1][city-1], alpha) *
                pow(1.0/CityDistanceList[self.CurrCity-1][city-1], beta)
            )
            #蚂蚁选择下一个城市的可能性由信息素与城市间距离之间关系等综合因素确定，其中alpha为表征信息素重要程度的参数，beta为表征启发式因子重要程度的参数，
            #该语句为前文蚁群算法阐述的选择下一个转移城市的概率公式的分母部分
            transferProbability = sumProbability#根据信息素选择公式和轮盘选择得出概率列表，非0-1
            self.TransferProbabilityList.append((city, transferProbability))#将城市序号和对应的转移城市概率追加到转移概率列表中
        threshold = sumProbability * random.random()#将概率值乘以一个0~1的随机数，获取轮盘指针值
        for (cityNum, cityProb) in self.TransferProbabilityList:#再次循环遍历概率列表
            if threshold <= cityProb:#如果轮盘指针值大于概率值，则返回对应的城市序号
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! key step!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                return (cityNum)
        return (0)#否则返回0

    def MoveToNextCity(self, alpha, beta):#定义转移城市方法
        nextCity = self.SelectNextCity(alpha, beta)#执行SelectNextCity(),选择下一个城市的方法，获取选择城市的序号，并赋值给新的变量nextCity
        if nextCity > 0 : #如果选择的城市序号大于0，则执行self.AddCity()方法，获取每次迭代的当前城市Currcity、禁忌城市列表TabuCityList和允许城市列表AllowedCitySet的值
            self.AddCity(nextCity)#执行self.AddCity()方法

    def ClearTabu(self):#定义清楚禁忌城市方法，以用于下一次循环
        self.TabuCityList = []#初始化禁忌城市列表为空
        self.TabuCitySet.clear()#初始化城市禁忌列表为空
        self.AllowedCitySet = CitySet - self.TabuCitySet#初始化允许城市集合

    def UpdatePathLen(self):#定义更新旅行路径长度方法
        for city in self.TabuCityList[0:-1]:#循环遍历禁忌城市列表
            nextCity = self.TabuCityList[self.TabuCityList.index(city)+1]#获取禁忌城市列表中的下一个城市序号
            self.CurrLen = self.CurrLen + CityDistanceList[city-1][nextCity-1]#从城市间距离之中提取当前循环城市与下一个城市之间的距离，并逐次求和
        lastCity = self.TabuCityList[-1]#提取禁忌列表中的最后一个城市
        firstCity = self.TabuCityList[0]#提取禁忌列表中的第一个城市
        self.CurrLen = self.CurrLen + CityDistanceList[lastCity-1][firstCity-1]#将最后一个城市与第一个城市的距离值加到当前旅行路径长度，获取循环全部城市的路径长度

    def AddCity(self, city):#定义增加城市到禁忌城市列表中的方法
        if city <= 0:#如果城市序号小于等于0，则返回
            return
        self.CurrCity = city#更新当前城市序号
        self.TabuCityList.append(city)#将当前城市追加到禁忌城市列表中，因为已经旅行过的城市不应该再进入
        self.TabuCitySet.add(city)#将当前城市追加到禁忌城市集合中，用于差集运算
        self.AllowedCitySet = CitySet - self.TabuCitySet#使用集合差集的方法获取允许的城市列表

    def two_opt_search(self): # 领域搜索
        cityNum = len(CityList)
        for i in range(cityNum):
            for j in range(cityNum-1, i, -1):
                #for j in range(i+1, cityNum):
                #for j in range((i+10) if (i+10)<cityNum else cityNum-1, i, -1):
                curCity1 = self.TabuCityList[i] -1#此处风格不统一!
                preCity1 = self.TabuCityList[(i-1) % cityNum] -1
                nextCity1 = self.TabuCityList[(i+1) % cityNum] -1
                curCity2 = self.TabuCityList[j] -1#此处风格不统一!
                preCity2 = self.TabuCityList[(j-1) % cityNum] -1
                nextCity2 = self.TabuCityList[(j+1) % cityNum] -1
                CurrLen = CityDistanceList[preCity1][curCity1] + CityDistanceList[curCity2][nextCity2]
                NextLen = CityDistanceList[preCity1][curCity2] + CityDistanceList[curCity1][nextCity2]
                if NextLen < CurrLen:
                    tempList = self.TabuCityList[i:j+1]
                    self.TabuCityList[i:j+1] = tempList[::-1]
                    # for i in range(cityNum):
                    #     curCity = self.TabuCityList[i] -1#此处风格不统一!
                    #     preCity = self.TabuCityList[(i-1) % cityNum] -1
                    #     nextCity = self.TabuCityList[(i+1) % cityNum] -1
                    #     forwardCity = self.TabuCityList[(i+2) % cityNum] -1
                    #     CurrLen = CityDistanceList[preCity][curCity] + CityDistanceList[nextCity][forwardCity]
                    #     NextLen = CityDistanceList[preCity][nextCity] + CityDistanceList[curCity][forwardCity]
                    #     if NextLen < CurrLen :
                    #         #print i
                    #         self.TabuCityList[i], self.TabuCityList[(i+1) % cityNum] = self.TabuCityList[(i+1) % cityNum], self.TabuCityList[i]

if __name__ == '__main__':#该语句说明之后的语句在该.py文件作为模块被调用时，语句之后的代码不执行；打开.py文件直接使用时，语句之后的代码则执行。通常该语句在模块测试中
    theBaca = BACA()#BACA类的实例化
    theBaca.ReadCityInfo('C:\\Users\\luole\\Desktop\\ant\\tsp\\eil51.tsp')#读取城市数据
    theBaca.Search()#执行Search()方法
