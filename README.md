# firstStepsInViz

First steps in 3D visualizations that are worth a thousand words, a 30 min introduction to visualization.

The NeSI Team.

What you will learn:
 * The difference between 2D and 3D visualization
 * What makes a 3D visualization truly 3D
    * actors
    * light 
    * background 
 * How to visualize grids
 * How to show data on grids
 * Playing with colours
 * Where to go from here

## Why 3D visualization?

Visualization is a process for representing objects or information in an intuitive way, typically 
using our innate concepts for perspective, depth of field, colour, shading and lighting. 

## What makes 3D visualization different from plotting?

Both plotting and visualization aim to convey as much information as possible. The two approaches 
are complementary: plotting represents objects and information on a flat sheet of paper whereas 
visualization will show those objects in a 3D scene. In a visualization the 
viewer will typically interact with the object (through rotation of the camera, adjusting the light, etc.). Plotting
tends to be static, hence it is more suitable for publishing.

## What tool should I use for visualization?

For custom visualizations we recommend [VTK](http://www.vtk.org/), which is free. You can either install precompiled versions
of VTK or build the toolkit from source. It comes with Python bindings, which makes it easy to explore
visualization concepts.

Hint: if you're using Python via [Anaconda](https://www.continuum.io/downloads) you can install the VTK toolkit and Python bindings with
```bash
conda install -c anaconda vtk
```

Many users may want to consider [ViSIt](https://wci.llnl.gov/simulation/computer-codes/visit/) or [Paraview](https://www.paraview.org/) as these tools will require no or minimal programming. 
If your file format is support by any of these tools then you will be ablt explore your data more 
quickly. Both these tools are free and binaries exist for nearly for Windows, Linux and Mac OS X. 

## Overview
1. [General visualization concepts](#scene)
2. [Understanding grids](#grid)
3. [Going fully 3D](#threed)


## General visualization concepts <a name="scene"></a>

### What is a pipeline?

Visualizations are made of elements which are assembled into a pipeline, essentially a workflow. Typically, a pipeline will involve reading data, applying filters, creating actors and rendering the
actors in a scene. Filters extract information from the data; e.g. a contour filter might extract the surface for which a field satisfy a constraint. Actors are objects that be rendered; triangles, lines, points, etc. At the end of the day every actor is made of collections of triangles, lines and points.

```sequence
vtkConeSource->vtkPolyDataMapper->vtkActor
```

### What is a scene?

Visualization is a little like a theater play; there is a background, there are lights and actors. We'll start 
with a cone playing the role of an actor.

Try:
```bash
python scene/cone.py
```

Next we'll refine the cone and add some lights, each with its own colour. 

Try:
```bash
python scene/coneWithLight.py
```

Questions: 
 * How can I change the colour of the light?
 * How can add another light?

## Understanding grids <a name="grid"></a>

More likely, your visualizations will involve gridded data so we'll need to understand how grids are represented in VTK. The main types of grid are __structured__ and __unstructructed__. Structured grids have regular topology with arbitrary points. This means that given a set of indices describing 
a point we can always find the neighbours without additional information beyond the size of the grid. Unstructured grids build on top of points and cells and the arrangement can be arbitrary, i.e. one 
has to specify the topology. You can mix cells of different types in VTK, for instance hexahedra with prisms, lines and points. See [http://www.vtk.org/data-model/]for a full list of supported cells. Naturally, unstructured grids are more flexible than structured grids. The latter are however easier to use (and more efficient).

We'll start with a polar grid represented as a structured grid.

Try:
```bash
python grid/polar.py
```

Note how the structured grid is constructed. First, the set of coordinates is computed and stored in object `coords`, 
an array of doubles
```python
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
```
Then an object `pts` of type vtkPoints is created with the points set to array `coords`. Finally,
the structured grid object `grid` sets the points (`pts`). 

Using a for loop in python can be a little slow for large grids. Here is a little known trick - it is possible to create all the data using the python numpy module and then pass the data directly to VTK:
```python
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
coords.SetVoidArray(xyz, 3*numPoints, 1)
```

Finally it should be noted that all VTK objects work with 3D grids and coordinates. Because our grid is 2D we must 
set one of the dimensions to one:
```python
grid.SetDimensions(nthe, nrho, 1)
```

Question:
 * How can I change the resolution of the grid?

### Visualizing data on a grid

In VTK data don't generally exist without a grid but a grid can exist without data. So far we just built a grid 
but neglected to attach data to the grid. There are two types of data: __point__ data and __cell__ data. Point data
belong the grid nodes whereas cell data associate to grid cells.

To set the point data use:
```python
grid.GetPointData().SetScalars(data)
```

To set cell data use
```python
grid.GetCellData().SetScalars(data)
```

We'll start with point data. Try:
```bash
python grid/polarWithPointData.py
```

Compare this to cell data. Try:
```bash
python grid/polarWithCellData.py
```
You'll notice that the cell get a solid colour in the case of cell data. Point data are interpolated linearly from 
each node to the neighbour node. 

### Adding colour

The default colour map in VTK maps low values to red and high values to blue! We need to fix this by adding a lookup 
table and a color bar actor. 

A lookup table 
```python
lut = vtk.vtkLookupTable()
```
maps a data value to a colour, encoded as four floats in the range oof 0 to 1 (red, green, blue and opacity). Here 
we'll set the colour range to vary from white to green, to light blue, red, purple and black. 
```python
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
```
You will also need to tell the mapper to use the look up table
```python
dataMapper.SetUseLookupTableScalarRange(1)
dataMapper.SetLookupTable(lut)
```

The color bar is an actor
```python
cbar = vtk.vtkScalarBarActor()
cbar.SetLookupTable(lut)
```
which must be added to the scene
```python
ren.AddActor(cbar)
```

Try:
```bash
python grid/polarWithPointDataLut.py
```

Question:
 * What is the effect of changing the number of colours (ncolors)?

### Adding depth

So far we worked in flat land -- when generating grid points we set the elevation `z` to zero. Let's set the elevation of the value of another function:
```python
rr2 = (xx**2 + yy**2).reshape((numPoints,))
xyz[:, 2] = 0.2*numpy.sin(10.*rr2)/numpy.sqrt(2.*rr2)
```
and run: 
```bash
python grid/polarWithPointDataLutBump.py
```

## Going fully 3D <a name="threed"></a>

The previous example was not really in 3D - it displayed a surface which is a 2D object. 

Try:
```bash
python 3d/cube.py
```
to run a case with 3D data. We're facing a new problem: we only see the exterior of the cube.

### I want to see inside!

One possibility is generate iso-surfaces from the data. Let's say we want to show the surfaces for which the data take values 0.2, 0.4 and 0.7:
```python
contour = vtk.vtkContourFilter()
contour.SetNumberOfValues(3)
contour.SetValue(0, 0.2)
contour.SetValue(1, 0.4)
contour.SetValue(2, 0.7)
contour.SetInputData(grid)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(contour.getOutputPort())
```

Try:
```bash
python 3d/cubeIsoSurface.py
```

### Take a knife and cut through your data

Another possibility is to cut through the data. We'll create a `vtkCutter` object and let VTK know that we will cut the domain with a `vtkPlane`:
```python
plane = vtk.vtkPlane()
plane.SetPosition(0.5, 0.5, 0.5)
plane.SetNormal(1., 0.2, -0.3)
knife = vtk.vtkCutter()
knife.SetCutFunction(plane)
```

Try:
```bash
python 3d/cubeCut.py
```

## Explore your data with ViSIt

In the previous step we cut through our data and needed provide a plane with position and normal vectors to indicate where to cut. In most instance you 
will likely want to vary the cut plane. This can be done by hooking VTK up to 
a graphical user interface (for instance Qt). Another way to achieve this is 
by saving your data in a file
```python
writer = vtk.vtkStructuredGridWriter()
writer.SetFileName('cube.vtk')
writer.SetInputData(grid)
writer.Update()
```
and use VisIt to explore your data. 



Hope you enjoyed the tutorial! Feel free to make suggestions and create pull-request. 