import vtk
import numpy

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
thes = numpy.linspace(0., 2*numpy.pi, nthe)
rhos = numpy.linspace(0., 1., nrho)
tthes, rrhos = numpy.meshgrid(thes, rhos)
xyz = numpy.zeros((numPoints, 3), numpy.float64)
rrhos = numpy.reshape(rrhos, (numPoints,))
tthes = numpy.reshape(tthes, (numPoints,))
xyz[:, 0] = rrhos*numpy.cos(tthes)
xyz[:, 1] = rrhos*numpy.sin(tthes)

coords.SetNumberOfComponents(3)
coords.SetNumberOfTuples(numPoints)
save = 1 # copying so xyz can be destroyed before coords
coords.SetVoidArray(xyz, 3*numPoints, save)

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