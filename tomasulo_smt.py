"""
Created on Sun Nov  17 19:56:37 2019

@author: shaomingtian
"""


#   指令类
#   name为指令名称，opr1~opr3为操作数
class instruction:
    def __init__(self,name,opr1='None',opr2='None',opr3='None'):
        self.name=name
        self.opr1=opr1
        self.opr2=opr2
        self.opr3=opr3
        self.started=False
        self.executed=False
        self.exeed=False
        self.written=False
    

#       指令状态类
#       started是否流出，executed是否进入执行阶段，written是否写回
#       number指令序号，op该指令操作类型，start_time流出时钟，execute_time执行时钟
class ins_condition:
    def __init__(self,number,op,execute_time,start_time=0):
        self.number=number
        self.op=op
        self.start_time=start_time
        self.execute_time=execute_time
        self.started=False
        self.executed=False
        self.exeed=False
        self.ex_Rb_number='None'
        self.written=False
    
#   保留站类
#   Op指示该保留站可执行何种类型的操作，cur_Op指示当前该保留站正在执行的操作类型
#   QjQk将产生操作数的保留站号，VjVk操作数的值
#   Busy为yes表示该保留站“忙”
#   A仅load和store指令有该项，表示立即数或计算后的地址，number为该保留站序号
class reservation_station:
    def __init__(self,Op,number,cur_Op='None',Qj='None',Qk='None',Vj='None',Vk='None',Busy=False,A='None'):
        self.Op=Op
        self.cur_Op=cur_Op
        self.number=number
        self.Qj=Qj
        self.Qk=Qk
        self.Vj=Vj
        self.Vk=Vk
        self.Busy=Busy
        self.A=A
        self.started_time='None'
        self.result='None'
    #清空保留站的方法
    def finis(self):
        self.Busy=False
        self.cur_Op='None'
        self.Qj='None'
        self.Qk='None'
        self.Vj='None'
        self.Vk='None'
        self.A='None'
        self.started_time='None'
        self.result='None'
class register:
    def __init__(self,name,val=0):
        self.name=name
        self.val=val

#顺序检查对应操作是否有保留站可用，可用则返回相应保留站号，否则返回-1
def available_reservation_station(op):
    if op=='L.D':
        for i in range(1,3):
            if not Reservation_station_state[i].Busy:
                return i
    elif op=='ADD.D' or op=='SUB.D':
        for i in range(3,6):
            if not Reservation_station_state[i].Busy:
                return i
    elif op=='DIV.D' or op=='MUL.D':
        for i in range(6,8):
            if not Reservation_station_state[i].Busy:
                return i
    else:
        return -1




#不同指令对应的exe时间即为PPT中的延迟时间＋1
Delay_time={'L.D':2,'ADD.D':3,'SUB.D':3,'DIV.D':41,'MUL.D':11,}

ins='1	L.D 	F6,34(R2)\n2	L.D 	F2,45(R3)\n3	MUL.D	F0,F2,F4\n4	SUB.D	F8,F2,F6\n5	DIV.D	F0,F0,F6\n6	ADD.D	F6,F8,F2'
ins=ins.split('\n')

#总指令数量
instruction_quantity=len(ins)
#print(instruction_quantity)
#指令表
instructions=[]
print('执行的指令序列为:')
for x in ins:
    x=x.replace('\t','')
    x=x.replace('\n','')
    x=x.replace(' ','')
    print(x)
    i=0
    while not(x[i-1]=='.'and x[i]=='D'):
        i+=1
    i+=1
    #这里限制了只能在个位数条指令时简化为op=str(x[1:i])
    #当指令数为两位数时要修改这里
    op=str(x[1:i])
    j=i+1
    while x[j]!=',':
        j+=1
    #这时候x[j]为","
    op1=str(x[i:j])
    j+=1
    #如果op1之后是立即数，那么是load即L.D指令
    if x[j]<='9' and x[j]>='0':
        #load指令
        #op3存立即数
        i=j
        j=i+1
        while x[j]!='(':
            j+=1
        #这时候x[j]是"(",得到的op3在使用时可能要转化为int
        op3=str(x[i:j])
        i=j+1
        j=i+1
        while x[j]!=')':
            j+=1
        op2=str(x[i:j])
        temp=op2
        op2=op3
        op3=temp
    else:
        #ALU指令
        i=j
        j=i+1
        while x[j]!=',':
            j+=1
        op2=str(x[i:j])
        j+=1
        i=j
        #while x[j]!='\n':
        #    j+=1
        op3=str(x[i:len(x)])
        #print(op1,op2,op3)
    instructions.append(instruction(op,op1,op2,op3))

#用到的寄存器对应的编号
Regs={'F0':0,'F2':2,'F4':4,'F6':6,'F8':8,'F10':10,'R2':11,'R3':12,}

#寄存器及其存储值的映射表
registers={'F0':'F0','F2':'F2','F4':'F4','F6':'F6','F8':'F8','F10':'F10','R2':'R2','R3':'R3',}

#Qi为寄存器状态指示表，可指明各寄存器的值是可以直接使用还是需要等待保留站的写入，初始为0表示所有寄存器都可用
Qi={'F0':0,'F2':0,'F4':0,'F6':0,'F8':0,'F10':0,'R2':0,'R3':0,}

#Instruction_state为指令状态表
Instruction_state=[ins_condition(i,instructions[i].name,Delay_time[instructions[i].name]) for i in range(instruction_quantity)]


#Reservation_station_state为保留站状态表
#1~2为load，3~5为加减法保留站，6~7为乘除法保留站，鉴于本题目代码中无store指令，不建立store保留站

Reservation_station_state=['']
for i in range(1,3):
    Reservation_station_state.append(reservation_station('L.D',i))
for i in range(3,6):
    Reservation_station_state.append(reservation_station('ADD.D',i))
for i in range(6,8):
    Reservation_station_state.append(reservation_station('DIV.D',i))

basic_time=0
cur_started_instructions=0  #已经ISSUE的指令数


def single_step():
    
    global basic_time
    global cur_started_instructions
    global Reservation_station_state
    global Instruction_state
    global instructions
    global Qi
    
    #时钟跳1
    basic_time+=1

    ##########ISSUE：下一条指令能否流出          ###########
    if cur_started_instructions<len(Instruction_state):
        op=Instruction_state[cur_started_instructions].op
        res=available_reservation_station(op)#判断是否还有保留站可以使用
        if res>0: #有空闲保留站，则ISSUE
            #当前指令            
            cur_instuction=instructions[cur_started_instructions]
            #更新保留站状态表信息
            Reservation_station_state[res].Busy=True
            Reservation_station_state[res].cur_Op=op
            Reservation_station_state[res].started_time=basic_time
            '''
            if op=='L.D':


            else:
            '''
            #定义一个序号来表示功能单元哪个
            if(res>0 and res<3):
                seq=res
            elif (res>2 and res<6):
                seq=res-2
            elif (res>5):
                seq=res-5
            #op1目的操作数,也就是目标寄存器
            if Qi[cur_instuction.opr1]==0:#当前目标寄存器没有冲突，也就是没有功能部件的目标寄存器是它
                Qi[cur_instuction.opr1]=cur_instuction.name+str(seq)

            #op2第一源操作数
            if op=='L.D':
                Reservation_station_state[res].A=str(cur_instuction.opr2)+'+'+str(cur_instuction.opr3)
            else:    
                if Qi[cur_instuction.opr2]==0:#当前目标寄存器没有冲突，也就是没有功能部件的目标寄存器是它
                    Reservation_station_state[res].Vj=registers[cur_instuction.opr2]
                    Reservation_station_state[res].Qj='None'                
                else:
                    Reservation_station_state[res].Vj='None'
                    Reservation_station_state[res].Qj=Qi[cur_instuction.opr2]
                
            #op3第二源操作数：load指令和运算指令分情况讨论
            if op!='L.D':
                if Qi[cur_instuction.opr3]==0:
                    Reservation_station_state[res].Vk=registers[cur_instuction.opr3]
                    Reservation_station_state[res].Qk='None'
                else:
                    Reservation_station_state[res].Vk='None'
                    Reservation_station_state[res].Qk=Qi[cur_instuction.opr3]
        #更新指令状态表中该条指令的状态为已流出
        Instruction_state[cur_started_instructions].start_time=basic_time
        Instruction_state[cur_started_instructions].started=basic_time
        Instruction_state[cur_started_instructions].ex_Rb_number=res
        #已流出指令数加一
        cur_started_instructions+=1
        


    ##############                执行                ###################
    #检查全部保留站，能执行的全部开始执行，执行时间到了的写结果
    for i in range(1,8):
        if Reservation_station_state[i].Busy==True:#仅仅判断被占用的保留站是否可以执行
            for j in range(instruction_quantity):
                if Instruction_state[j].ex_Rb_number==i:
                    break
            
            #流出->执行
            #特殊处理LOAD的执行和写回
            if Reservation_station_state[i].Op=='L.D':
                if Reservation_station_state[i].started_time==basic_time-1:
                    Instruction_state[j].executed=basic_time
                if Reservation_station_state[i].started_time==basic_time-Delay_time[Reservation_station_state[i].cur_Op]:
                    Instruction_state[j].exeed=basic_time
                    Reservation_station_state[i].result='Mem'+'['+Reservation_station_state[i].A+']'
                elif Reservation_station_state[i].started_time==basic_time-1-Delay_time[Reservation_station_state[i].cur_Op]:
                    Instruction_state[j].written=basic_time
                    Reservation_station_state[i].Busy=False
                    Reservation_station_state[i].A='None'
                    #for y in range(3,8):
                    #if Reservation_station_state[y].Qj=='L.D'+str(i):
                    for y in range(3,8):
                        if Reservation_station_state[y].Qj=='L.D'+str(i) and Reservation_station_state[y].Vj=='None':
                            Reservation_station_state[y].Vj=Reservation_station_state[i].result
                            Reservation_station_state[y].Qj='None' 
                        if Reservation_station_state[y].Qk=='L.D'+str(i) and Reservation_station_state[y].Vk=='None':
                            Reservation_station_state[y].Vk=Reservation_station_state[i].result
                            Reservation_station_state[y].Qk='None'
                    for x in Qi:#寄存器写回
                        if Qi[x]=='L.D'+str(i):
                            Qi[x]=0
                    
            else:
                
                if(Reservation_station_state[i].Vj != 'None' and Reservation_station_state[i].Vk != 'None'):
                    #两个操作数就绪
                    if Instruction_state[j].executed==False:
                        Instruction_state[j].executed=basic_time
                    elif Instruction_state[j].executed==basic_time+1-Delay_time[Reservation_station_state[i].cur_Op]:
                        Instruction_state[j].exeed=basic_time
                        if Reservation_station_state[i].cur_Op=='ADD.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'+'+str(Reservation_station_state[i].Vk)
                        if Reservation_station_state[i].cur_Op=='SUB.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'-'+str(Reservation_station_state[i].Vk)
                        if Reservation_station_state[i].cur_Op=='MUL.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'*'+str(Reservation_station_state[i].Vk)
                        if Reservation_station_state[i].cur_Op=='DIV.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'/'+str(Reservation_station_state[i].Vk)
                    elif Instruction_state[j].executed==basic_time-Delay_time[Reservation_station_state[i].cur_Op]:
                        Instruction_state[j].written=basic_time
                        #若有寄存器在等待当前保留站的结果
                        #print(Qi[x])
                        #print(len(str(Qi[x])))
                        if Reservation_station_state[i].cur_Op=='ADD.D':
                            for x in Qi:
                                if Qi[x]=='ADD.D'+str(i-2):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='ADD.D'+str(i-2) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='ADD.D'+str(i-2) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis()
                        if Reservation_station_state[i].cur_Op=='SUB.D':
                            for x in Qi:
                                if Qi[x]=='SUB.D'+str(i-2):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='SUB.D'+str(i-2) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='SUB.D'+str(i-2) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis()
                        if Reservation_station_state[i].cur_Op=='MUL.D':
                            for x in Qi:
                                if Qi[x]=='MUL.D'+str(i-5):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='MUL.D'+str(i-5) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='MUL.D'+str(i-5) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis() 
                        if Reservation_station_state[i].cur_Op=='DIV.D':
                            for x in Qi:
                                if Qi[x]=='DIV.D'+str(i-5):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='DIV.D'+str(i-5) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='DIV.D'+str(i-5) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis()


####################################
# 输出当前各表信息
def printInfo():
	#周期信息
	print ("Cycle : " + str(basic_time))
	#指令状态表信息
	print('Instruction Status')
	print("\t指令类型\t执行延迟\t流出\t开始执行\t执行完毕\t写回")
	for i in range(instruction_quantity):
	    x=Instruction_state[i]
	    print('指令'+str(x.number)+'\t'+str(x.op)+'\t\t'+str(x.execute_time)+'\t\t'+str(x.start_time)+'\t'+str(x.executed)+'\t\t'+str(x.exeed)+'\t\t'+str(x.written))
	print('\nLoad Buffer')
	print('\tBusy\tAddress')
	for i in range(1,3):
	    x=Reservation_station_state[i]
	    print('L.D'+str(i)+'\t'+str(x.Busy)+'\t'+str(x.A)+'\t')
	print('\nReservation Stations')
	print("\t保留站属性\t当前操作类型\t编号\tVj\tVk\tQj\tQk\tBusy\tA\t开始时钟\t结果")
	for i in range(3,len(Reservation_station_state)):
	    x=Reservation_station_state[i]
	    print('保留站'+str(i-2)+'\t'+str(x.Op)+'\t\t'+str(x.cur_Op)+'\t\t'+str(x.number)+'\t'+str(x.Vj)+'\t'+str(x.Vk)+'\t'+str(x.Qj)+'\t'+str(x.Qk)+'\t'+str(x.Busy)+'\t'+str(x.A)+'\t'+str(x.started_time)+'\t\t'+str(x.result))
	print('\nRegister Result status')
	#寄存器结果状态表信息，只输出PPT中出现的寄存器
	print("F0\tF2\tF4\tF6\tF8\tF10\t")
	print(str(Qi["F0"])+"\t"+str(Qi["F2"])+"\t"+str(Qi["F4"])+"\t"+str(Qi["F6"])+"\t"+str(Qi["F8"])+"\t"+str(Qi["F10"])+"\t")

	'''
	if insTable != None:
		ins = insTable.getList()
		
		print ("Instruction\ttarget\tj\tk\tIssue\tRead operand\tExecution complet\tWrite Result")
		for item in ins:
			print (item["instruction"]+"\t\t"+item["target"]+"\t"+item["j"]+"\t"+item["k"]+"\t"+item["issue"]+"\t"+item["readOperand"]+"\t\t"+item["exeComplet"]+"\t\t\t"+item["writeResult"])
	#功能单元状态表信息
	if funcUTable != None:
		func = funcUTable.getList()
		print ("Functional Unit status")
		print ("Name\tBusy\tOp\tFi\tFj\tFk\tQj\tQk\tRj\tRk")
		for item in func:
			print (item["name"]+"\t"+item["busy"]+"\t"+item["Op"]+"\t"+item["Fi"]+"\t"+item["Fj"]+"\t"+item["Fk"]+"\t"+item["Qj"]+"\t"+item["Qk"]+"\t"+item["Rj"]+"\t"+item["Rk"])
	#寄存器结果状态表信息，只输出F0-F11因为后面的都没有用到
	if registerTable != None:
		reg = registerTable.getDict()
		print ("Register result status")
		print ("F0\tF1\tF2\tF3\tF4\tF5\t")
		print (reg["F0"]+"\t"+reg["F1"]+"\t"+reg["F2"]+"\t"+reg["F3"]+"\t"+reg["F4"]+"\t"+reg["F5"]+"\t")
		print ("F6\tF7\tF8\tF9\tF10\tF11\t")
		print (reg["F6"]+"\t"+reg["F7"]+"\t"+reg["F8"]+"\t"+reg["F9"]+"\t"+reg["F10"]+"\t"+reg["F11"]+"\t")
    '''


####################################

inputst = input("请输入跳转周期，输入‘-1’(负一)结束程序\n")
#print(inputst)

while inputst != '-1':
    inputst = int(inputst)
    
    while(basic_time < inputst):
        single_step()
    printInfo()
    inputst = input("请输入跳转周期，输入‘-1’(负一)结束程序\n")
print('Program done')
