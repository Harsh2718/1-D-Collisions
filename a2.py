from math import trunc
import time
class Min_Heap:
    def __init__(self,L):
        self.length = len(L)
        self.size = len(L)
        self.Heap = L
    def parent(self,i):
        if (i==0):
            return i
        return (i-1)//2
    def Left_Child(self,i):
        if (i < (self.size//2)):
            return 2*i+1
        return i
    def Right_Child(self,i):
        if (i < ((self.size-1)//2)):
            return 2*i+2
        return i
    def Heap_Up(self,A,i):
        while self.Heap[self.parent(i)]>self.Heap[i]:
            k = self.Heap[self.parent(i)][1]
            l = self.Heap[i][1]
            A[k]=i
            A[l]=self.parent(i)
            self.Heap[self.parent(i)],self.Heap[i]=self.Heap[i],self.Heap[self.parent(i)]
            i = self.parent(i)
    def Heap_Down(self,A,i):
        while (self.Heap[self.Left_Child(i)]<self.Heap[i] or self.Heap[self.Right_Child(i)]<self.Heap[i]) and i < self.size//2:
            if self.Heap[self.Left_Child(i)]<self.Heap[self.Right_Child(i)]:
                v = self.Left_Child(i)
            else:
                v = self.Right_Child(i)
            k= self.Heap[v][1]
            l =self.Heap[i][1]
            A[k]=i
            A[l]=v
            self.Heap[v],self.Heap[i] = self.Heap[i],self.Heap[v]
            i= v
    def fast_build_heap(self,A):
        for i in range (self.size-1,-1,-1):
           self.Heap_Down(A,i)
    def __str__(self):
        return str(self.Heap)
    def Change_key(self,A,i,x):
        x1=self.Heap[i]
        self.Heap[i] = x
        if x1>x:
            self.Heap_Up(A,i)
        if x1<x:
            self.Heap_Down(A,i)
    def get_root(self):
        return 0
    def get_min(self):
        return self.Heap[self.get_root()]
    def extract_root(self,A):
        root = self.Heap[0]
        k=self.Heap[0][1]
        self.Heap[0]=self.Heap[self.size-1]
        l = self.Heap[self.size-1][1]
        A[l] = 0
        self.Heap.pop()
        A[k] = -1
        self.size-=1
        if self.size>0:
            self.Heap_Down(A,0)
        return root
    def insert_key(self,A,x):
        self.Heap.append(x)
        self.size+=1
        k= self.Heap[self.size-1][1]
        A[k] = self.size -1 
        self.Heap_Up(A,self.size-1)
def listCollisions(M,x,v,m,T):
    n = len(M)
    out_list=[]
    time_list=[]
    index_list=[]
    pos_time=[]
    for i in range(n):
        pos_time.append([x[i],0])
    for i in range(n-1):
        index_list.append(i)
    for i in range(n-1):
        v1=v[i]
        v2=v[i+1]
        x1=x[i]
        x2=x[i+1]
        if checkCollisions(v1,v2):
            t= get_time(x1,x2,v1,v2)
        else:
            t= T+1
        time_list.append([t,i])
    heap=Min_Heap(time_list)
    heap.fast_build_heap(index_list)
    k=0
    while (k<m):
        t_min = heap.get_min()
        t=t_min[0]
        if (t_min[0]>T):
            break
        else:
            print(v[72])
            i = t_min[1]
            m1= M[i]
            m2 = M[i+1]
            v1=v[i]
            v2=v[i+1]
            x1=pos_time[i][0]
            x2=pos_time[i+1][0]
            x1_final = x1+v1*(t-pos_time[i][1])
            x2_final = x2+v2*(t-pos_time[i+1][1])
            pos_time[i] =[x1_final,t]
            pos_time[i+1]=[x2_final,t]
            out_list.append((round(t_min[0],4),i,round(pos_time[i][0],4)))
            v_final1,v_final2 = get_velocities(m1,m2,v1,v2)
            v[i],v[i+1] = v_final1,v_final2
            heap.extract_root(index_list)
            if i==0 and n>2:
                l0= index_list[i+1]
                v11 = v[i+1]
                v22 = v[i+2]
                x11 = pos_time[i+1][0]+ v11*(t-pos_time[i+1][1])
                pos_time[i+1] = [x11,t]
                x22=pos_time[i+2][0]+ v22*(t-pos_time[i+2][1])
                pos_time[i+2]=[x22,t]
                if checkCollisions(v11,v22):
                    t1=t_min[0]+get_time(x11,x22,v11,v22)
                else:
                    t1=T+1
                if l0==-1:
                    heap.insert_key(index_list,[t1,i+1])
                else:
                    heap.Change_key(index_list,l0,[t1,i+1])
            elif i==n-2 and n>2:
                l1= index_list[i-1]
                v11 = v[i-1]
                v22 = v[i]
                x11 = pos_time[i-1][0]+ v11*(t-pos_time[i-1][1])
                pos_time[i-1] = [x11,t]
                x22=pos_time[i][0]+ v22*(t-pos_time[i][1])
                pos_time[i]=[x22,t]
                if checkCollisions(v11,v22):
                    t1=t_min[0]+get_time(x11,x22,v11,v22)
                else:
                    t1=T+1
                if l1==-1:
                    heap.insert_key(index_list,[t1,i-1])
                else:
                    heap.Change_key(index_list,l1,[t1,i-1])
            elif i!=0 and i!=n-2 and n>=4:
                l3=index_list[i+1]
                l5 = index_list[i-1]
                v11=v[i-1]
                v22=v[i]
                v33=v[i+1]
                v44=v[i+2]
                x11 = pos_time[i-1][0]+ v11*(t-pos_time[i-1][1])
                pos_time[i-1] = [x11,t]
                x22=pos_time[i][0]+ v22*(t-pos_time[i][1])
                pos_time[i]=[x22,t]
                x33 = pos_time[i+1][0]+ v33*(t-pos_time[i+1][1])
                pos_time[i+1] = [x33,t]
                x44=pos_time[i+2][0]+ v44*(t-pos_time[i+2][1])
                pos_time[i+2]=[x44,t]
                if checkCollisions(v11,v22):
                    t1=t_min[0]+get_time(x11,x22,v11,v22)
                else:
                    t1=T+1
                if checkCollisions(v33,v44):
                    t2=t_min[0]+get_time(x33,x44,v33,v44)
                else:
                    t2=T+1
                if l5==-1:
                    heap.insert_key(index_list,[t1,i-1])
                else:
                    heap.Change_key(index_list,l5,[t1,i-1])
                if l3==-1:
                    heap.insert_key(index_list,[t2,i+1])
                else:
                    heap.Change_key(index_list,l3,[t2,i+1])
        k+=1
    return out_list 
def checkCollisions(v1,v2):
    if ((v1-v2)<=0):
        return False
    elif (v1-v2)>0:
        return True 
def get_time(x1,x2,v1,v2):
        return (abs(x1-x2))/(abs(v1-v2))
def get_velocities(m1,m2,v1,v2):
    v1_final= ((m1-m2)/(m1+m2))*v1 + (2*m2/(m1+m2))*v2
    v2_final= (2*m1/(m1+m2))*v1 - ((m1-m2)/(m1+m2))*v2
    return (v1_final,v2_final)
def get_pos(x1,x2,v1,v2):
    if checkCollisions(v1,v2):
        t =get_time(x1,x2,v1,v2)
    return (x1+t*v1,x2+t*v2)
#[(1.1299, 27, 2852.6127), (2.4358, 72, 9191.1491), (2.479, 77, 9793.6524), (2.7181, 21, 2515.9839), (3.7015, 59, 8272.9894), (4.2847, 20, 2516.1745), (5.0875, 65, 8922.8235), (5.6514, 66, 8928.2862), (6.3684, 65, 8932.9673), (7.3954, 22, 2549.0136), (7.5053, 67, 8944.7173), (7.5257, 21, 2548.8677), (7.7515, 22, 2550.6437), (7.8906, 66, 8945.3234), (8.1742, 65, 8945.1137), (9.1086, 66, 8952.3939), (9.3327, 39, 4337.7809), (9.9735, 11, 1468.8266), (11.0493, 30, 3202.3247), (11.4311, 19, 2533.2458), (11.6435, 20, 2535.1032), (12.0089, 19, 2535.1828), (12.0906, 64, 8946.389), (12.6004, 73, 9297.9889), (13.5662, 16, 1950.473), (14.5273, 69, 9147.9069), (14.6744, 21, 2572.4095), (16.26, 65, 8988.8897), (17.6073, 70, 9181.495), (18.822, 74, 9358.0283), (19.0641, 28, 2959.146), (19.9688, 66, 9029.3878), (20.2802, 22, 2631.2178), (22.1477, 38, 4315.0695), (23.9851, 26, 2898.4308), (25.0366, 20, 2586.1532), (25.2205, 37, 4291.5183), (25.3415, 71, 9304.3958), (25.809, 49, 5987.5347), (26.1187, 48, 5988.4618), (26.3339, 49, 5991.0175), (26.8445, 75, 9448.5971), (27.2179, 38, 4335.5566), (27.2585, 46, 5853.4979), (27.338, 6, 901.5458), (28.3083, 60, 8602.8475), (28.383, 10, 1499.078)]
lis1=[[12796.506138572438, 77823.70902511006, 21477.793419128564, 19925.29397312417, 92229.18132406162, 26294.312732835766, 5246.111523846542, 81875.20185697752, 91369.75067562603, 7728.105103911976, 95372.76516629085, 86962.42218256224, 99589.5122758794, 77846.33553210879, 75789.46847965897, 14089.887544596746, 27189.973986915782, 7744.659824365729, 36603.669966772446, 62006.53173862802, 43211.88702718338, 23551.37258838074, 35205.22337551467, 89649.67568648129, 10276.378831944023, 40354.31206273846, 60450.7754729102, 27324.21911081595, 82219.24595483446, 44424.53872010889, 36273.186643231726, 55345.678274944454, 45136.059010101504, 63747.891809836285, 53188.63454533289, 56717.70588755674, 15889.243026031607, 43105.630888416716, 5300.02098408947, 16044.199913464086, 52174.86067424396, 82689.42680304316, 91843.81559056487, 7663.404918946848, 30531.691933687456, 33748.897938834976, 93885.9726274754, 23430.609985267227, 90567.60846691189, 16399.345241706655, 19487.411606321315, 93390.16855794353, 90130.18881286941, 13592.80037285614, 60173.481424675934, 98703.56667323032, 79989.30152946494, 94805.47938785651, 15669.11411564419, 59910.435408878446, 9822.181541705533, 88056.0397015103, 62728.96736199326, 76628.6779746058, 67337.94103615484, 60392.463862651566, 45313.86952026199, 94827.88628731393, 86432.24243807221, 97255.94805449259, 27365.74602970929, 3849.994479831531, 64536.870535039, 52829.04089552225, 79158.02896712619, 52839.004496982976, 69380.91183940432, 55642.70797172961, 52542.585276134305, 98691.56875425506], [28.403200423076093, 117.26128783965284, 485.03677726086215, 490.5224527051377, 516.5698276815556, 654.3216043302547, 691.9664424228366, 881.6202446874466, 1096.685174490507, 1177.9354757890048, 1217.5954606633832, 1393.7625471964143, 1448.717877436474, 1493.1242806391588, 1524.9527027017873, 1822.7074073944505, 1888.664013683362, 1925.402035433519, 2369.5467437982875, 2444.2638338323795, 2482.6670338968916, 2493.047878863278, 2511.911724034345, 2538.9224507799436, 2620.757671539912, 2665.8359533812004, 2700.6772820188776, 2843.6728751502114, 2848.1194121424915, 2869.870450740972, 3139.7260879828236, 3193.132341940391, 3445.6538132811565, 3792.4441871416657, 3917.0262273072976, 3954.638831708384, 4033.7398907788315, 4064.063127931683, 4095.083720980348, 4279.520654413362, 4328.421697343782, 4676.637398183113, 5184.98628434169, 5476.069521032661, 5477.280904763831, 5535.086232807413, 5611.072092997885, 5760.582743184497, 5773.264208723264, 5808.192352954477, 5902.181961690098, 6249.098939742338, 6588.5662076799845, 7207.171068553118, 7256.521238037978, 7356.3118046464815, 7675.884288136918, 7965.13545160007, 8149.249521681996, 8238.126312624621, 8258.669395070197, 8382.66440122524, 8442.9383372108, 8496.626764209037, 8829.295610574061, 8874.820909394466, 8883.81984418337, 8886.732191670355, 8935.569560388753, 9028.457049430574, 9097.949243257179, 9106.002611529651, 9166.898784880716, 9180.45895329785, 9219.922954637976, 9331.13173442354, 9338.957908029435, 9772.736213937216, 9792.405027613862, 9929.789266357304], [4.654622151680955, 7.34018008756007, 1.4401118077728792, 3.537600498229275, 7.811157163960468, 6.719308423898353, -5.373025233506576, 1.564340433454956, 0.3917752512892225, 3.1506513797099247, 2.024900568470649, 10.298954934768696, 7.153403936398159, 9.184213486802602, 6.536400293784296, 15.914985182143107, 3.3553928213048936, 6.063441051209894, 5.672780616982653, 0.7777206763200767, 2.0879011462618795, 4.67403583667351, 4.660944927621391, 8.720487980076474, 5.265852902887758, 7.1072199542426, 4.359761576915071, 10.59990876729223, 5.058123113634395, 6.315420757125052, -0.17424632189750144, 4.659202314410497, 7.608292194343726, 1.5822047296940356, 1.1676472070151478, 1.6657542365743006, 7.821027009154773, 9.018646617635973, -7.664251458887665, 4.040682855950224, 3.4674684720250104, 4.126315672102516, 1.9225088871261398, 1.4511961646672078, 3.7155398262080244, 2.9603504333340416, 6.702687861147296, 12.187615936764516, 6.49395465432843, 6.940295880632748, 11.425332504277666, 1.2200174440261602, 1.001039887324514, 0.3651354277498675, 0.3797360809551287, 3.382235869688135, 3.5332979234320083, 9.136142142863376, 7.138548873515001, 7.855184465440734, 3.280297038654661, 8.907402571694382, 7.006881264223327, 9.632638415440901, 0.8345265871946452, 5.829405975927915, 5.736371086481203, 9.566426116328952, 9.216875826243763, 6.121611688033759, 5.8089121374842065, 19.851575597519126, 6.176543763741561, 0.757290705582625, 8.888878906335394, 7.145901990434344, 4.084225084860991, 0.7305444456299331, 8.66462338721243, 5.189288440788481], 47, 556.0612253103493]
M= lis1[0]
x = lis1[1]
v = lis1[2]
m = lis1[3]
T = lis1[4]
print(listCollisions(M,x,v,m,T))
