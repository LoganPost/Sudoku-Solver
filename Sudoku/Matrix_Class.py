from math import sin, cos,atan
import math
class Matrix(list):
    def height(self):
        return len(self)
    def length(self):
        if len(self)==0:
            return 0
        else:
            return len(self[0])
    def sps(self):
        for r,row in enumerate(self):
            out="["
            first=True
            for e,el in enumerate(row):
                if not first:
                    out+=" "
                else:
                    first=False
                out+=str(el)
                for i in range(max([len(str(self[i][e])) for i in range(len(self))])-len(str(el))):
                    out+=" "
            out+="]"
            print(out)
    def __mul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            return Matrix([other*el for el in row] for row in self)
        assert self.length()==other.height()
        output=[[0]*other.length() for i in range(self.height())]
        for r, row in enumerate(output):
            for e, el in enumerate(row):
                for p, val in enumerate(self[r]):
                    output[r][e]+=val*other[p][e]
        return Matrix(output)
    def __rmul__(self,other):
        return self*other
    def __add__(self,other):
        assert self.length()==other.length() and self.height()==other.height()
        output=[[0]*other.length() for i in range(self.height())]
        for r, row in enumerate(output):
            for e, el in enumerate(row):
                output[r][e]+=self[r][e]+other[r][e]
        return Matrix(output)
    def __sub__(self,other):
        assert self.length()==other.length() and self.height()==other.height()
        output=[[0]*other.length() for i in range(self.height())]
        for r, row in enumerate(output):
            for e, el in enumerate(row):
                output[r][e]+=self[r][e]-other[r][e]
        return Matrix(output)
    def inverse(self):
        assert self.det()!=0
        if self.length()==1:
            return self*(1/self.det()**2)
        else:
            output=Matrix([[0]*self.length() for i in range(self.height())])
            determinant=self.det()
            for r in range(self.height()):
                for e in range(self.length()):
                    cols=list(range(0,e))+list(range(e+1,self.length()))
                    rows=list(range(0,r))+list(range(r+1,self.height()))
                    recur=Matrix([[self[row][el] for el in cols] for row in rows])
                    output[r][e]=Frac(recur.det()*((-1)**(r+e)))
            return output.trans()*(1/self.det())
    def trans(self):
        output=[[0]*self.height() for i in range(self.length())]
        for r in range(self.height()):
            for c in range(self.length()):
                output[c][r]=self[r][c]
        return Matrix(output)
    def det(self):
        assert self.length()==self.height()
        if self.length()==1:
            return self[0][0]
        else:
            output=0
            for e in range(len(self[0])):
                cols=list(range(0,e))+list(range(e+1,len(self[0])))
                rows=range(1,len(self))
                recur=Matrix([[self[row][el] for el in cols] for row in rows])
                adding=recur.det()*self[0][e]*((-1)**e)
                output+=adding
                #print(self[0][e]," becomes ",adding," from ")
                #recur.sms()
            return output
    def round(self,dec):
        return Matrix([[round(el,dec) for el in row] for row in self])
    def apply(self,vec):
        return V(sum(row[i]*vec[i] for i in range(len(vec))) for row in self)
class V(tuple):
    def __add__(self,other):
        return V(self[i]+other[i] for i in range(len(self)))
    def __sub__(self,other):
        return V(self[i] - other[i] for i in range(len(self)))
    def __mul__(self,other): # Dot product
        if isinstance(other,int) or isinstance(other,float):
            return V(i*other for i in self)
        else:
            return sum(self[i]*other[i] for i in range(len(self)))
    def __rmul__(self,other):
        return self*other
    def __truediv__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            return V(i/other for i in self)
        else:
            return sum(self[i]/other[i] for i in range(len(self)))
    def pmul(self,other):
        return V(self[i]*other[i] for i in range(len(self)))
    def cross(self,other):
        if len(self)!=3:
            return "This vector can't have cross product, it is length "+str(len(self))
        i=self[1]*other[2]-self[2]*other[1]
        j=self[2]*other[0]-self[0]*other[2]
        k=self[0]*other[1]-self[1]*other[0]
        return V(i,j,k)
    def __abs__(self):
        return (sum(i**2 for i in self))**(1/2)
    def __eq__(self,other):
        if len(self)==len(other):
            for i in range(len(self)):
                if self[i]!=other[i]:
                    return False
            return True
        return False
    def angle(self):
        if self==(0,0):
            return 0
        if self[0]==0:
            if self[1]>0:
                return 90
            else:
                return 270
        elif self[0]>0:
            return atan(-self[1] / self[0])  * 180 / math.pi
        else:
            return 180+atan(-self[1] / self[0])  * 180 / math.pi

        # if self!=(0,0) and len(self)==2:
        #     if self[0]==0:
        #         if self[1]>0:
        #             return 90
        #         return 270
        #     elif self[0]>0:
        #         return atan(self[1]/self[0])*180/math.pi
        #     return 180+atan(self[1]/self[0])*180/math.pi
        # elif self==(0,0):
        #     return 0
        # else:
        #     return "no angle for length "+str(len(self))
    def normalize(self):
        if abs(self)==0:
            return self
        else:
            return self/abs(self)
    def __rsub__(self,other):
        return (-1)*(self-other)
    def __radd__(self,other):
        return self+other
    def __iadd__(self,other):
        return self+other
    def lenSquared(self):
        return sum(i**2 for i in self)
    def intify(self):
        return V(int(i) for i in self)
    def rdown(self):
        return V(round(i-0.5) for i in self)
    def rup(self):
        return V(round(i+0.5) for i in self)
    def cmul(self,other):
        return V((self[0]*other[0]-self[1]*other[1],self[1]*other[0]+self[0]*other[1]))
    def conj(self):
        return V((self[0],-self[1]))
    def absify(self):
        return V((abs(i) for i in self))
    def __isub__(self, other):
        return self-other


