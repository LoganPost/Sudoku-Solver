from Graph_Class import Vertex,Cage,Grid,decompress
import pygame as pg
from Matrix_Class import Matrix, V
from Button_Class import Button,TextBox
import pickle

window_size=V((650,650))
reset_grid=False
in_bold=False
memory_size=30
entering_number_id=-1


def show_instructions():
    print("s:               solve")
    print("c:               clean board (+shift removes everything)")
    print("f:               fill board with example solution")
    print("tab:             undo last change ("+str(memory_size)+"x)")
    print("click or arrows: select board spot (+shift selects killer cage)")
    print("number key:      change assigned value (+shift for solving)")
    print("bkspce,del,0:       remove assigned value")
    print("caps lock:       holds shift key down")
    print("b:               makes the numbers bold")
    print("i:               instructions")

def copy_grid(grid):
    cop=Grid()
    for new,v in zip(cop,grid):
        new.val=v.val
        new.assigned=v.assigned
    cop.cages=[Cage([i for i in c]) for c in grid.cages]
    for c1,c2 in zip(cop.cages,grid.cages): c1.val=c2.val
    # for cage in grid.cages:
    #     for i in cage:
    #         grid[i].cages.append(cage)
    cop.point=grid.point
    return cop
def print_grid(grid):
    c = 0
    for v in grid:
        print(str(v.posn) + "   ", end="")
        c += 1
        if c % 3 == 0:
            print("   ", end="")
        if c % 9 == 0:
            print()
        if c % 27 == 0:
            print()

def check_legal_2(v,val,grid):
    # return val not in [i.val for i in v.connections]
    if val in [i.val for i in v.connections]:
        return False
    for cage in grid.cages:
        if grid.vertices.index(v) in cage:
            hypsum=sum(grid[i].val for i in cage)+val-v.val
            nz=len([grid[i] for i in cage if grid[i].val==0])-int(v.val==0)
            # print(val,hypsum,nz,[(v,grid[v].val) for v in cage.vertices])
            # print("pluggin in {} gives {} where the cage value is {} with {} zeros".format(val,hypsum,cage.val,nz))
            if hypsum+nz*(nz+1)/2>cage.val:
                # print("{} Too big, sum of {} for {} with {} zeros: {}".format(val,hypsum,cage.val,nz,[grid[i].val for i in cage]))
                return False
            if hypsum+nz*(19-nz)/2<cage.val:
                # print("{} too small sum of {} for {} with {} zeros: {}".format(val,hypsum,cage.val,nz,[grid[i].val for i in cage]))
                return False
            if val in [grid[i].val for i in cage if grid[i]!=v]:
                return False
    # for cage in v.cages:
    #     hypsum=sum(grid[i].val for i in cage)+val
    #     nz=len([grid[i] for i in cage if grid[i]!=v and grid[i].val==0])
    #     print(val,hypsum,nz,[grid[v].val for v in cage.vertices])
    #     if hypsum+nz*(nz+1)/2>cage.val:
    #         return False
    #     if hypsum+nz*(19-nz)/2<cage.val:
    #         return False
    return True

def same_grid(g1,g2):
    for v1,v2 in zip(g1,g2):
        if v1.val!=v2.val or v1.assigned!=v2.assigned:
            return False
    if len(g1.cages)!=len(g2.cages):
        return False
    for c1,c2 in zip(g1.cages,g2.cages):
        if sorted(c1)!= sorted(c2):
            return False
        if c1.val!=c2.val:
            return False
    return True

def show_numbers(grid):
    all_nums = pg.Surface(window_size, pg.SRCALPHA, 32).convert_alpha()
    #all_nums = all_nums
    for i,v in enumerate(grid):
        if v.val!=0:
            pos = (i % 9 * 50 + 100, int(i / 9) * 50 + 100 )
            if v.assigned:
                col=assigned_color
            else:
                col=unassigned_color
            numbox=TextBox(str(v.val),col,pg.font.SysFont("calibri",50,in_bold))
            numbox.center(pos+V((25,30)))
            numbox.blit(all_nums)
    return all_nums

cage_border=5
def outline_cages(grid):
    surf=pg.Surface(window_size, pg.SRCALPHA, 32).convert_alpha()

    for cage in grid.cages:
        cage=sorted(cage)
        for i in cage:
            for vertcomp in (1,-1):
                if i+vertcomp*9 not in cage:
                    ycomp=int(i / 9) * 50 + 125+vertcomp*(25-cage_border)+1
                    if i-1 in cage:
                        if i+vertcomp*9-1 in cage:
                            left_start=(i % 9 * 50 + 100-cage_border, ycomp)
                        else:
                            left_start = (i % 9 * 50 + 100, ycomp)
                    else:
                        left_start = (i % 9 * 50 + 100 + cage_border, ycomp)
                    if i+1 in cage:
                        if i+vertcomp*9+1 in cage:
                            right_start=(i % 9 * 50 + 150+cage_border,ycomp)
                        else:
                            right_start = (i % 9 * 50 + 150,ycomp)
                    else:
                        right_start = (i % 9 * 50 + 150 - cage_border,ycomp)
                    pg.draw.line(surf, (0, 0, 0), left_start,right_start,1)
            for hcomp in (1,-1):
                if i+hcomp not in cage:
                    xcomp=i % 9 * 50 + 125+hcomp*(25-cage_border)
                    if i-9 in cage:
                        if i-9+hcomp in cage:
                            top_start=(xcomp, int(i / 9) * 50 + 101-cage_border)
                        else:
                            top_start=(xcomp, int(i / 9) * 50 + 101)
                    else:
                        top_start=(xcomp, int(i / 9) * 50 + 101+cage_border)
                    if i + 9 in cage:
                        if i + 9 + hcomp in cage:
                            bot_start = (xcomp, int(i / 9) * 50 + 150 + cage_border)
                        else:
                            bot_start = (xcomp, int(i / 9) * 50 + 150)
                    else:
                        bot_start = (xcomp, int(i / 9) * 50 + 150 - cage_border)
                    pg.draw.line(surf, (0, 0, 0), top_start,bot_start,1)
    return surf
def update_cage_nums(grid):
    numsurf=pg.Surface(window_size,pg.SRCALPHA,32).convert_alpha()

    def pos(i):
        return (i % 9 * 50 + 100, int(i / 9) * 50 + 100)
    for i,cage in enumerate(grid.cages):
        cage.vertices=sorted(cage.vertices)
        if entering_number_id==i:
            box = Button(V((1, 1)) * cage_border * 3, white-(30,30,30), str(cage.val), (0, 0, 0), pg.font.SysFont('calibri', cage_border * 3), 0)
        else:
            box = Button(V((1, 1)) * cage_border * 3, white, str(cage.val), (0, 0, 0), pg.font.SysFont('calibri', cage_border * 3), 0)
        box.topleft(pos(cage[0]) + V((1, 1)) * cage_border)
        box.rad = 2
        box.blit(numsurf)
    return numsurf

def clean_grid(grid):
    for v in grid:
        if not v.assigned:
            v.val=0
def clear_grid(grib):
    global grid
    grid=Grid()
    global outlines, cage_nums
    outlines = outline_cages(grid)
    cage_nums = update_cage_nums(grid)
    for v in grib:
        v.assigned=False
        v.val=0
def fill_grid(grid):
    for i,v in enumerate(grid):
        shift=(3*int(i/9)+int(i/27))%9
        v.val=(i+shift)%9+1
        v.assigned=True
def is_solved(grid):
    return False not in [v.val!=0 and check_legal_2(v,v.val,grid) for v in grid]
def is_sus(grid):
    return False in [check_legal_2(v,v.val,grid) for v in grid if v.val!=0]
def solve_grid(grid): #Assumes a unique solution!!
    choice=-1
    options=10
    for i,v in enumerate(grid):
        if v.val==0:
            n=len([i for i in range(1,10) if check_legal_2(v,i,grid) ])
            if n<options:
                options=n
                choice=i
            if n==0:
                # print("{} has no possiblities".format(i))
                options=0
            if n==1:
                v.val=[i for i in range(1,10) if check_legal_2(v,i,grid) ][0]
                options=1
                break
    # print("{} has {} options".format(choice,options))
    if options==1:
        # print("only one choice")
        # cp(grid)
        return solve_grid(grid)
    elif options==0:
        # print("help")
        # cp(grid)
        return (False,grid)
    elif options==10:
        return (True,grid)
    else:
        for n in [i for i in range(1,10) if check_legal_2(grid[choice],i,grid)]:
            # print("SOMETHING")
            temp_grid=copy_grid(grid)
            temp_grid[choice].val=n
            out=solve_grid(temp_grid)
            if out[0]:
                return out
        # print("help")
        return (False,grid)
def check_uniqueness(grid):
    solution=copy_grid(grid)
    to_solve=copy_grid(grid)
    clean_grid(to_solve)
    def helper(grid,solution):
        choice = -1
        options = 10
        for i, v in enumerate(grid):
            if v.val == 0:
                n = len([i for i in range(1, 10) if check_legal_2(v, i,grid)])
                if n < options:
                    options = n
                    choice = i
                if n == 0:
                    options = 12
                if n == 1:
                    v.val = [i for i in range(1, 10) if check_legal_2(v, i,grid)][0]
                    options = 11
                    break
        if options == 11:
            # print("only one choice")
            # cp(grid)
            return helper(grid,solution)
        elif options == 12 or same_grid(grid,solution):
            return (False, grid)
        elif options == 10:
            return (True, grid)
        else:
            for n in [i for i in range(1, 10) if check_legal_2(grid[choice], i,grid)]:
                temp_grid = copy_grid(grid)
                temp_grid[choice].val = n
                out = helper(temp_grid,solution)
                if out[0]:
                    return out
            return (False, grid)
    return helper(to_solve,solution)

def square_to_highlight(n):
    return (n % 9 * 50 + 100 + 2, int(n / 9) * 50 + 100 + 2)

def cp(grid):
    c=0
    for v in grid:
        print(str(v.val)+"  ",end="")
        c+=1
        if c%3==0:
            print("  ",end="")
        if c%9==0:
            print()
        if c%27==0:
            print()

def update_memory(grid):
    global memory
    if not same_grid(memory[-1],grid):
        memory.append(copy_grid(grid))
        memory=memory[1:]
        # print([i[0].val for i in memory])
def undo(grid):
    global memory
    if not same_grid(memory[-2],grid):
        memory=[memory[0]]+memory
        memory.pop()
        new_grid=(memory[-1])
        global outlines, cage_nums
        outlines = outline_cages(new_grid)
        cage_nums = update_cage_nums(new_grid)
        return copy_grid(new_grid)
    return grid

def make_new_cage(val):
    global entering_number_id
    if True not in [True in [i in cage for cage in grid.cages] for i in grid.selected]:
        grid.cages.append(Cage(grid.selected))
        grid.cages[-1].val=val
        entering_number_id = len(grid.cages) - 1
    else:
        for cage in grid.cages:
            if sorted(grid.selected) == sorted(cage):
                grid.cages.remove(cage)
                grid.cages.append(Cage(grid.selected))
                grid.cages[-1].val = val
                entering_number_id = len(grid.cages) - 1
    grid.selected = []
    global outlines, cage_nums
    outlines = outline_cages(grid)
    cage_nums = update_cage_nums(grid)

###########################################################################
###########################################################################


if reset_grid:
    grid=Grid()
    memory=[copy_grid(grid) for i in range(30)]
    pickle.dump(grid, open("save_grid.dat", 'wb'))
else:
    grid= pickle.load(open("save_grid.dat", 'rb'))
    memory=[copy_grid(grid) for i in range(30)]

key_numbers={
    113:"q", 119:"w",101:"e",114:"r",
    116:"t",121:"y",117:"u",105:"i",111:"o",112:"p",
    97:"a",    115:"s",    100:"d",102:"f",    103:"g",104:"h",    106:"j",
    107:"k",    108:"l",122:"z",    120:"x",99:"c",    118:"v",
    98:"b",    110:"n",109:"m",    32:" ",
}

# grid=construct_grid()

screen=pg.display.set_mode(window_size) # This makes the display
pg.init()

background = pg.Surface(window_size)  # background surface
bg_col=V((210,210,210))
highlight_col=V((140,150,195))
high_3_col=V((160,165,175))
assigned_color=(0,0,0)
unassigned_color=(40,60,140)

bg_col=V((210,210,210))
highlight_col=V((195,140,150))
high_3_col=V((175,160,160))
assigned_color=(0,0,0)
unassigned_color=(140,40,50)

white=V((255,255,255))
bg_col=V((220,220,220))
highlight_col=V((155,195,130)) #Pointing number
high_3_col=V((170,180,170)) # Other numbers
high_sel_col=V((175,170,190))
selecting_col=V((155,150,170))
assigned_color=(0,0,0)
unassigned_color=(50,100,20)

background.fill(white)
highlight=pg.Surface((48,48))
less_highlight=pg.Surface((48,48))
high_3=pg.Surface((48,48))
high_sel=pg.Surface((48,48))
high_selecting=pg.Surface((48,48))
high_erasing=pg.Surface((48,48))

highlight.fill(highlight_col)
less_highlight.fill((bg_col*2+highlight_col)/3)
high_3.fill(high_3_col)
high_sel.fill(high_sel_col)
high_selecting.fill(selecting_col)
high_erasing.fill(bg_col)

lines=pg.Surface(window_size, pg.SRCALPHA, 32).convert_alpha()
for x in range(100,551,50):
    pg.draw.line(lines,(0,0,0),(x,100),(x,550),2)
for y in range(100,551,50):
    pg.draw.line(lines,(0,0,0),(100,y),(550,y),2)
for x in range(101,552,150):
    pg.draw.line(lines,(0,0,0),(x,100),(x,552),2)
for y in range(101,552,150):
    pg.draw.line(lines,(0,0,0),(100,y),(550,y),2)

clock=pg.time.Clock()   # pygame thing
num_surface=show_numbers(grid)
outlines=outline_cages(grid)
cage_nums=update_cage_nums(grid)
shift_down=False
selting=False
erasing=False
show_instructions()
###########################################################################
###########################################################################
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Leftclick down
                if entering_number_id>=0:
                    entering_number_id=-1
                    cage_nums=update_cage_nums(grid)
                mpos=V(pg.mouse.get_pos())
                x,y=mpos
                xcoord=int((x-100)/50)
                ycoord=int((y-100)/50)
                clicked=int((x-100)/50)+9*int((y-100)/50)
                if 0<=xcoord<=8 and 0<=ycoord<=8:
                    if grid.point!=clicked:
                        grid.point=clicked
                    elif not shift_down:
                        grid.point=-1
                if shift_down:
                    if clicked not in grid.selected:
                        grid.selected.append(clicked)
                    else:
                        grid.selected.remove(clicked)
                else:
                    grid.selected=[]
        if event.type == pg.KEYDOWN:
            # print(event.key)
            if event.key==116: # T to input text for save graph
                print("This is the grid code:",grid)
                print("uncompressed:",decompress(str(grid)))
                inp=input("Input new Grid:")
                # print("This was the input:",inp)
                if inp:
                    grid=Grid(inp)
                outlines = outline_cages(grid)
                cage_nums = update_cage_nums(grid)
            if event.key==13: # enter to save cage
                if entering_number_id>=0:
                    entering_number_id=-1
                    cage_nums=update_cage_nums(grid)
                elif grid.selected:
                    make_new_cage(sum(grid[i].val for i in grid.selected))
                    selting=False
                    erasing=False
            if event.key==1073741881: #Caps lock
                shift_down=not shift_down
            if event.key==1073742049: #shift
                shift_down=not shift_down
            elif event.key in (1073741906,1073741905,1073741904,1073741903):
                if entering_number_id>=0:
                    entering_number_id=-1
                    cage_nums=update_cage_nums(grid)
                if shift_down and grid.point not in grid.selected:
                    grid.selected.append(grid.point)
                if event.key==1073741906: #up arrow
                    grid.point-=9
                    grid.point=grid.point%81
                elif event.key==1073741905: #down arrow
                    grid.point += 9
                    grid.point = grid.point % 81
                elif event.key==1073741904: #left arrow
                    grid.point -= 1
                    if grid.point%9==8:
                        grid.point += 9
                elif event.key==1073741903: #right arrow
                    grid.point += 1
                    if grid.point % 9==0:
                        grid.point -= 9
                if shift_down :
                    if grid.point not in grid.selected:
                        grid.selected.append(grid.point)
                else:
                    grid.selected=[]
            elif event.key==99: #clean/clear
                if shift_down:
                    clear_grid(grid)
                else:
                    clean_grid(grid)
            elif 48<=event.key<=57: #number key
                if entering_number_id>=0:
                    cage=grid.cages[entering_number_id]
                    cage.val=10*cage.val+event.key-48
                    cage_nums=update_cage_nums(grid)
                elif grid.selected:
                    make_new_cage(event.key-48)
                elif grid.point!=-1:
                    erasing=False
                    selting=False
                    num=event.key-48
                    v=grid.square()
                    if v.val!=num or v.assigned==shift_down:
                        v.val=num
                        v.assigned=not shift_down
                    else:
                        v.val = 0
                    if v.val==0:
                        v.assigned=False
            elif event.key in (8,127) and grid.point!=-1: #delete or backspace
                if entering_number_id>=0:
                    cage = grid.cages[entering_number_id]
                    cage.val = int( cage.val/10)
                    cage_nums=update_cage_nums(grid)
                elif grid.selected:
                    for cage in grid.cages:
                        if False not in [i in grid.selected for i in cage]:
                            grid.cages.remove(cage)
                    outlines = outline_cages(grid)
                    cage_nums = update_cage_nums(grid)
                else:
                    grid.square().val = 0
                    grid.square().assigned = False
            elif event.key==102: #fill grid
                fill_grid(grid)
            elif event.key==115: #solve grid
                if is_sus(grid):
                    print("This grid is sus")
                else:
                    temp=solve_grid(grid)
                    if temp[0]:
                        grid=temp[1]
                    else:
                        print("This is not solvable, sorry")
            elif event.key==117: #check unique
                if is_solved(grid):
                    temp=check_uniqueness(grid)
                    if not temp[0]:
                        print("This is a unique solution")
                    else:
                        print("This is not a unique solution, here is another")
                        grid=temp[1]
                else:
                    print("This is not solved!")
            elif event.key==98: #bold
                in_bold=not in_bold
                print(grid)
                # for cage in grid.cages:
                #   print([(i,grid[i].val) for i in cage], False not in [cage in grid[i].cages])
                # for i,v in enumerate(grid[:10]):
                #     print(i,v.cages)
            elif event.key==9: #undo
                # print("Trying to undo")
                grid=undo(grid)
            elif event.key==105: #information
                show_instructions()
            pickle.dump(grid, open("save_grid.dat", 'wb'))
            update_memory(grid)
            num_surface=show_numbers(grid)
        if event.type == pg.KEYUP:
            if event.key == 1073742049:
                shift_down = not shift_down
    screen.blit(background, (0, 0))

    for i,v in enumerate(grid):
        if grid.point!=-1:
            if v in grid.square().connections:
                screen.blit(less_highlight,square_to_highlight(i))
            if v.val!=0 and v.val==grid.square().val:
                screen.blit(high_3,square_to_highlight(i))
        if i in grid.selected:
            screen.blit(high_sel, square_to_highlight(i))
    if grid.point!=-1:
        if grid.point in grid.selected:
            screen.blit(high_selecting,square_to_highlight(grid.point))
        else:
            screen.blit(highlight,square_to_highlight(grid.point))

    screen.blit(lines,(0,0))
    screen.blit(outlines, (0, 0))
    screen.blit(cage_nums, (0, 0))
    screen.blit(num_surface,(0,0))
    pg.display.update()

    clock.tick(60) # Limits to 60 fps
print_grid(grid)
