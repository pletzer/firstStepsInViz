import vtk
import numpy

nthe, nrho = 32 + 1, 20 + 1
numPoints = nthe * nrho
numCells = (nthe - 1) * (nrho - 1)

# construct the points
thes = numpy.linspace(0., 2*numpy.pi, nthe)
rhos = numpy.linspace(0., 1., nrho)
tthes, rrhos = numpy.meshgrid(thes, rhos)
xx = rrhos*numpy.cos(tthes)
yy = rrhos*numpy.sin(tthes)
xyz = numpy.zeros((numPoints, 3), numpy.float64)
xyz[:, 0] = xx.flat
xyz[:, 1] = yy.flat
# create cell centred versions of the above by averaging the 4 corner values
xxCell = 0.25*(xx[:-1, :-1] + xx[1:, :-1] + xx[1:, 1:] + xx[:-1, 1:])
yyCell = 0.25*(yy[:-1, :-1] + yy[1:, :-1] + yy[1:, 1:] + yy[:-1, 1:])
# set the data to some function
ffCell = numpy.cos(2*xxCell*numpy.pi)*numpy.sin(3*yyCell*numpy.pi)

# create the pipeline
data = vtk.vtkDoubleArray()
coords = vtk.vtkDoubleArray()
pts = vtk.vtkPoints()
grid = vtk.vtkStructuredGrid()
edges = vtk.vtkExtractEdges()
tubes = vtk.vtkTubeFilter()
edgeMapper = vtk.vtkPolyDataMapper()
edgeActor = vtk.vtkActor()
dataMapper = vtk.vtkDataSetMapper()
dataActor = vtk.vtkActor()

# settings
tubes.SetRadius(0.005)
grid.SetDimensions(nthe, nrho, 1)
coords.SetNumberOfComponents(3)
coords.SetNumberOfTuples(numPoints)
save = 1
coords.SetVoidArray(xyz, 3*numPoints, 1)
data.SetNumberOfComponents(1) # scalar
data.SetNumberOfTuples(numCells)
save = 1
data.SetVoidArray(ffCell, 3*numCells, save)

# connect
pts.SetNumberOfPoints(numPoints)
pts.SetData(coords)
grid.SetPoints(pts)
grid.GetCellData().SetScalars(data)
edges.SetInputData(grid)
tubes.SetInputConnection(edges.GetOutputPort())
edgeMapper.SetInputConnection(tubes.GetOutputPort())
edgeActor.SetMapper(edgeMapper)
dataMapper.SetInputData(grid)
dataActor.SetMapper(dataMapper)

# show
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# add the actors to the renderer, set the background and size
ren.AddActor(edgeActor)
ren.AddActor(dataActor)
ren.SetBackground(0.5, 0.5, 0.5)
renWin.SetSize(900, 600)
iren.Initialize()
renWin.Render()
iren.Start()