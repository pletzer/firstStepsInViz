import vtk
from math import cos, sin, pi

nthe, nrho = 16 + 1, 10 + 1
numPoints = nthe * nrho

# create the pipeline
coords = vtk.vtkDoubleArray()
pts = vtk.vtkPoints()
grid = vtk.vtkStructuredGrid()
edges = vtk.vtkExtractEdges()
tubes = vtk.vtkTubeFilter()
edgeMapper = vtk.vtkPolyDataMapper()
edgeActor = vtk.vtkActor()

# settings
tubes.SetRadius(0.01)

# construct the grid
grid.SetDimensions(nthe, nrho, 1)

# construct the points
dthe, drho = 2*pi/float(nthe - 1), 1.0/float(nrho - 1)
coords.SetNumberOfComponents(3)
coords.SetNumberOfTuples(numPoints)
k = 0
for j in range(nrho):
    rho = j * drho
    for i in range(nthe):
        the = i * dthe
        x = rho * cos(the)
        y = rho * sin(the)
        z = 0.0
        coords.SetTuple(k, (x, y, z))
        k += 1

# connect
pts.SetNumberOfPoints(numPoints)
pts.SetData(coords)
grid.SetPoints(pts)
edges.SetInputData(grid)
tubes.SetInputConnection(edges.GetOutputPort())
edgeMapper.SetInputConnection(tubes.GetOutputPort())
edgeActor.SetMapper(edgeMapper)

# show
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# add the actors to the renderer, set the background and size
ren.AddActor(edgeActor)
ren.SetBackground(0.5, 0.5, 0.5)
renWin.SetSize(400, 300)
iren.Initialize()
renWin.Render()
iren.Start()