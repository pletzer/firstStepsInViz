import vtk
import numpy

nthe, nrho = 128 + 1, 80 + 1
numPoints = nthe * nrho

# construct the points
thes = numpy.linspace(0., 2*numpy.pi, nthe)
rhos = numpy.linspace(0., 1., nrho)
tthes, rrhos = numpy.meshgrid(thes, rhos)
xx = rrhos*numpy.cos(tthes)
yy = rrhos*numpy.sin(tthes)
ff = numpy.cos(2*xx*numpy.pi)*numpy.sin(3*yy*numpy.pi)
fMin, fMax = ff.min(), ff.max()
print('min/max data values: {}/{}'.format(fMin, fMax))
xyz = numpy.zeros((numPoints, 3), numpy.float64)
xyz[:, 0] = xx.flat
xyz[:, 1] = yy.flat


# create the pipeline
data = vtk.vtkDoubleArray()
coords = vtk.vtkDoubleArray()
pts = vtk.vtkPoints()
grid = vtk.vtkStructuredGrid()
dataMapper = vtk.vtkDataSetMapper()
dataActor = vtk.vtkActor()
lut = vtk.vtkLookupTable()
cbar = vtk.vtkScalarBarActor()

# settings
ncolors = 64
lut.SetNumberOfColors(ncolors)
for i in range(ncolors):
    x = 0.5*i*numpy.pi/(ncolors - 1.)
    r = numpy.cos(3*x)**2
    g = numpy.cos(1*x)**2
    b = numpy.cos(5*x)**2
    a = 1.0 # opacity
    lut.SetTableValue(i, r, g, b, a)
lut.SetTableRange(fMin, fMax)
cbar.SetLookupTable(lut)
dataMapper.SetUseLookupTableScalarRange(1)

# construct the grid
grid.SetDimensions(nthe, nrho, 1)

coords.SetNumberOfComponents(3)
coords.SetNumberOfTuples(numPoints)
coords.SetVoidArray(xyz, 3*numPoints, 1)

# set the data
data.SetNumberOfComponents(1) # scalar
data.SetNumberOfTuples(numPoints)
# set the data to some function of the coordinate
save = 1
data.SetVoidArray(ff, 3*numPoints, save)


# connect
pts.SetNumberOfPoints(numPoints)
pts.SetData(coords)
grid.SetPoints(pts)
grid.GetPointData().SetScalars(data)
dataMapper.SetInputData(grid)
dataActor.SetMapper(dataMapper)
dataMapper.SetLookupTable(lut)

# show
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# add the actors to the renderer, set the background and size
ren.AddActor(dataActor)
ren.AddActor(cbar)
ren.SetBackground(0.5, 0.5, 0.5)
renWin.SetSize(900, 600)
iren.Initialize()
renWin.Render()
iren.Start()