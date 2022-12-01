class Vertex():
    def __init__(self,posn):
        self.posn=posn
        self.val=0
        self.connections=[]
        self.assigned=False
        self.cages=[]
    def connect(self,other):
        self.connections.append(other)

class Cage():
    def __init__(self,vertices):
        self.vertices=vertices
        self.val=0
    def __iter__(self):
        return iter(self.vertices)
    def __getitem__(self,item):
        return self.vertices[item]
    def __repr__(self):
        return "({}-cage, {} squares)".format(self.val,len(self.vertices))


class Grid():
    def __init__(self,string=""):
        self.vertices = [Vertex((x, y, int(x / 3) + 3 * int(y / 3))) for y in range(9) for x in range(9)]
        for v in self.vertices:
            for u in self.vertices:
                if u != v and True in [x == y for x, y in zip(u.posn, v.posn)]:
                    v.connections.append(u)
        self.cages=[]
        self.point=0
        self.selected=[]
        if string:
            st=decompress(string)
            # print(st)
            # print(st[81:106])
            ass = str(bin(int(st[81:106])))[2:]
            ass="0"*(81-len(ass))+ass
            # print("ass is ",ass)
            for i,v in enumerate(self.vertices):
                v.val=int(st[i])
                v.assigned=bool(int(ass[i]))
            # print(st,len(st))
            # print(len(st[81:106]))
            st=st[106:]
            # print(len(st),st)
            while st:
                newcage=Cage([])
                while st[0]!="_":
                    newcage.vertices.append(int(st[:2]))
                    st=st[2:]
                st=st[1:]
                val=0
                while st[0]!="$":
                    val*=10
                    val+=int(st[0])
                    st=st[1:]
                st=st[1:]
                newcage.val=val
                self.cages.append(newcage)




    def __iter__(self):
        return iter(self.vertices)
    def __getitem__(self,item):
        return self.vertices[item]
    def square(self):
        return self[self.point]
    def __str__(self):
        out=""
        for v in self.vertices:
            out+=str(v.val)
        ass_num=0
        for v in self.vertices:
            ass_num*=2
            ass_num+=int(v.assigned)
        ass_str=str(ass_num)
        out+="0"*(25-len(ass_str))+ass_str
        for cage in self.cages:
            for i in cage:
                if i<10:
                    out+="0"+str(i)
                else:
                    out+=str(i)
            out+="_"+str(cage.val)+"$"
        return compress(out)


def compress(string):
    num_key = "0123456789_$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    inp=0
    string="1"+string
    for s in string:
        inp*=12
        inp+=num_key.index(s)
    out=""
    # print(inp)
    while inp>0:
        out=num_key[inp%64]+out
        inp=inp//64
    # print(out)
    return out
def decompress(string):
    num_key = "0123456789_$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    inp=0
    for s in string:
        inp*=64
        inp+=num_key.index(s)
    out=""
    # print(inp)
    while inp>0:
        out=num_key[inp%12]+out
        inp=inp//12
    # print(out)
    return out[1:]