import vtk
import numpy

nx, ny, nz = 100 + 1, 101 + 1, 102 + 1
numPoints = nx * ny * nz

# construct the points
xs = numpy.linspace(0., 1.0, nx)
ys = numpy.linspace(0., 1.1, ny)
zs = numpy.linspace(0., 1.2, nz)
zz, yy, xx = numpy.meshgrid(zs, ys, xs, indexing='ij')
ff = numpy.cos(2*xx*numpy.pi)*numpy.sin(3*yy*numpy.pi)*numpy.exp(-(zz-0.5)**2/0.5**2)
fMin, fMax = ff.min(), ff.max()
print('min/max data values: {}/{}'.format(fMin, fMax))
xyz = numpy.zeros((numPoints, 3), numpy.float64)
xyz[:, 0] = xx.flat
xyz[:, 1] = yy.flat
xyz[:, 2] = zz.flat

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
lut.SetHueRange(0.666,0.)
lut.SetTableRange(fMin, fMax)
cbar.SetLookupTable(lut)
dataMapper.SetUseLookupTableScalarRange(1)

# construct the grid
grid.SetDimensions(nx, ny, nz)

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

writer = vtk.vtkStructuredGridWriter()
writer.SetFileName('cube.vtk')
writer.SetInputData(grid)
writer.Update()

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
renWin.SetSize(400, 300)
iren.Initialize()
renWin.Render()
iren.Start()