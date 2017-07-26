import vtk
import numpy

nthe, nrho = 32 + 1, 20 + 1
numPoints = nthe * nrho
numCells = (nthe - 1) * (nrho - 1)

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

# construct the grid
grid.SetDimensions(nthe, nrho, 1)

# construct the points
thes = numpy.linspace(0., 2*numpy.pi, nthe)
rhos = numpy.linspace(0., 1., nrho)
tthes, rrhos = numpy.meshgrid(thes, rhos)
xyz = numpy.zeros((numPoints, 3), numpy.float64)
rrhos = numpy.reshape(rrhos, (numPoints,))
tthes = numpy.reshape(tthes, (numPoints,))
xyz[:, 0] = rrhos*numpy.cos(tthes)
xyz[:, 1] = rrhos*numpy.sin(tthes)
# create cell centered versions of the above by averaging the 4 corner values
xx = numpy.reshape(xyz[:, 0], (nthe, nrho))
yy = numpy.reshape(xyz[:, 1], (nthe, nrho))
xxCell = 0.25*(xx[:-1, :-1] + xx[1:, :-1] + xx[1:, 1:] + xx[:-1, 1:])
yyCell = 0.25*(yy[:-1, :-1] + yy[1:, :-1] + yy[1:, 1:] + yy[:-1, 1:])

coords.SetNumberOfComponents(3)
coords.SetNumberOfTuples(numCells)
coords.SetVoidArray(xyz, 3*numCells, 1)

# set the data
data.SetNumberOfComponents(1) # scalar
data.SetNumberOfTuples(numPoints)
# set the data to some function of the coordinate
save = 1
ffCell = numpy.cos(2*xxCell*numpy.pi)*numpy.sin(3*yyCell*numpy.pi)
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
renWin.SetSize(400, 300)
iren.Initialize()
renWin.Render()
iren.Start()