import taichi as ti
import meshtaichi_patcher as Patcher

ti.init()

#读入表面网格
def init_surf_mesh(model_name):
    #这是用来排列indices的taichi kernel函数
    @ti.kernel
    def init_surf_indices(mesh: ti.template(), indices: ti.template()):
        for f in mesh.faces:
            for j in ti.static(range(3)):
                indices[f.id * 3 + j] = f.verts[j].id

    #1. 先加载模型 
    #relation的意思: F是Face, V是Verts FV表示通过一个面可以找到它的三个顶点，
    #要在加载mesh的时候就把这个关系建立好
    theMesh = Patcher.load_mesh(model_name, relations=["FV"])
    #2. 定义x场，每个verts位置挂载位置x, 它是一个vec3
    theMesh.verts.place({'x' : ti.math.vec3})
    #3. 把numpy的数据传给x（一开始我们读的坐标是numpy的）
    theMesh.verts.x.from_numpy(theMesh.get_position_as_numpy())
    #4. 定义一个indices场，这是为了后面渲染用的(scene.mesh), 它是一维数组，长度是面的数量*3
    display_indices = ti.field(ti.i32, shape = len(theMesh.faces) * 3)
    #5. 按照每三个一组的顺序，把每个面的三个顶点的id传给indices
    init_surf_indices(theMesh, display_indices)
    return theMesh, display_indices

# 这里我们读入了bunny.obj
bunny, bunny_indices = init_surf_mesh("models/bunny.obj")

# 读入四面体网格
def init_tet_mesh(model_name):
    #这是用来排列indices的taichi kernel函数
    @ti.kernel
    def init_tet_indices(mesh: ti.template(), indices: ti.template()):
        for c in mesh.cells:
            ind = [[0, 2, 1], [0, 3, 2], [0, 1, 3], [1, 2, 3]]
            for i in ti.static(range(4)):
                for j in ti.static(range(3)):
                    indices[(c.id * 4 + i) * 3 + j] = c.verts[ind[i][j]].id

    #基本与上面一样，只是多了一个CV关系，表示通过一个cell可以找到它的四个顶点
    theMesh = Patcher.load_mesh(model_name, relations=["CV"])
    theMesh.verts.place({'x' : ti.math.vec3})
    theMesh.verts.x.from_numpy(theMesh.get_position_as_numpy())
    #这里是四面体，所以每个cell有四个面，每个面有三个顶点，所以indices的长度是len(theMesh.cells) * 4 * 3
    display_indices = ti.field(ti.u32, shape = len(theMesh.cells) * 4 * 3)
    init_tet_indices(theMesh, display_indices)
    return theMesh, display_indices

#这里我们读入了armadillo的四面体模型。这个模型是通过tetgen生成的，我们只需要给出node文件就可以了，它会自动找到ele和face文件。tetgen可以转化ply为node格式，可以在这里下载：http://wias-berlin.de/software/index.jsp?id=TetGen&lang=1
armadillo, armadillo_indices = init_tet_mesh("models/armadillo0/armadillo0.1.node")


window = ti.ui.Window("taichimesh", (1024, 1024))
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera.up(0, 1, 0)
camera.fov(75)
camera.position(4.5,4.5,0.6)
camera.lookat(3.8, 3.8, 0.5)
camera.fov(75)

frame = 0
paused = ti.field(int, shape=())
paused[None] = 1
while window.running:
    # 用下面这段代码，通过提前设置一个paused变量，我们就可以在运行的时候按空格暂停和继续了！
    for e in window.get_events(ti.ui.PRESS):
        if e.key == ti.ui.SPACE:
            paused[None] = not paused[None]
            print("paused:", paused[None])
    if not paused[None]:
        # substep()
        print(f"frame: {frame}")
        frame += 1
    # 我们可以通过下面的代码来查看相机的位置和lookat，这样我们就能知道怎么调整相机的位置了
    # print("camera.curr_position",camera.curr_position)
    # print("camera.curr_lookat",camera.curr_lookat)

    # movement_speed=0.05表示移动速度，hold_key=ti.ui.RMB表示按住右键可以移动视角
    # wasdqe可以移动相机
    camera.track_user_inputs(window, movement_speed=0.05, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    
    # 渲染bunny和armadillo!!
    scene.mesh(bunny.verts.x, bunny_indices, color = (0.5,0.5,0.5))
    scene.mesh(armadillo.verts.x, armadillo_indices, color = (0.5,0.5,0.5))

    scene.particles(bunny.verts.x, radius=1e-2, color = (1,0.5,0.5))# 我们也可以把点渲染出来

    scene.point_light(pos=(0.5, 1.5, 0.5), color=(1, 1, 1))
    scene.ambient_light((0.5,0.5,0.5))

    canvas.scene(scene)

    window.show()
