# firstStepsInViz

First steps in 3D visualizations that are worth a thousand words

## Why 3D visualization?

Visualization is a process for representing objects or information in an intuitive way, typically 
using our innate concepts for perspective, depth of field, colour, shading and lighting. 

## What makes 3D visualization different from plotting?

Both plotting and visualization aim to convey as much information as possible. The two approaches 
are complementary: plotting represents objects and information of a flat sheet of paper whereas 
visualization will show those objects in a 3D scene. As such visualization will typically have the 
viewer interact with the object (through rotation of the camera, adjusting the light, etc.). Plotting
tends to be static, hence it is more suitable for publishing.

## What tool should I use for visualization?

For custom visualizations I recommend VTK, which is free. You can either install precompiled versions
of VTK or build the toolkit from source. It comes with Python bindings, which make it easy to explore
visualization concepts.

Hint: if you're using Python via Anaconda you can install the VTK toolkit and Python bindings with
```bash
conda install -c anaconda vtk
```

Many users may want to consider ViSIt or Paraview as these tools will require no or minimal programming. 
If your file format is support by any of these tools then you will be ablt explore your data more 
quickly. Both these tools are free and binaries exist for nearly for Windows, Linux and Mac OS X. 

## General visualization concepts

### What is a pipeline?

Visualizations are made of elements which are assembled into a pipeline, essentially a workflow. 
Typically, a pipeline will involve reading data, applying filters, creating actors and render the
actors in a scene. Filters extract information from the data; e.g. a contour filter might extract 
the surface for which a field satisfy a constraint. Actors are objects that be rendered; triangles, 
lines, points, etc. At the end of the day every actor is made of collections of triangles, lines and 
points.

### What is a scene?

Visualization is a little like a theater play; there is a background, there are lights and actors. We'll start 
with a cone as an actor:
```bash
cd scene
python cone.py
```

Next we'll refine the cone and add some lights, each with its own colour:
```bash
python coneWithLight.py
```

### Understanding grids

More likely, your visualizations will involve gridded data so we'll need to understand how grids 
are represented in VTK. The main types of grid are __structured__ and __unstructructed__. Structured 
grids have regular topology with arbitrary points. This means that given a set of indices describing 
a point I can always find the neighbours without additional information beyond the size of the grid. 
Unstructured grids built on top of points and cells and the arrangement can be arbitrary, i.e. one 
has to specify the topology. You can mix cells of different types in VTK, for instance hexahedra with
prisms with lines and even single points that are not connected to any other point. See [http://www.vtk.org/data-model/]
for a full list of supported cells. Naturally, unstructured grids are more flexible than structured grids.
The latter are however easier to use (and more efficient), if that's what you need.

We'll start with a polar grid represented as a structured grid:
```bash
cd grid
python polar.py
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

Using a for loop in python can be a little slow for large grids. Here is a little know trick -- it is also possible to create all the data using the python numpy module and then pass the data directly to VTK:
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

### Visualizing data on a grid

In VTK data don't generally exist without a grid but a grid can exist without data. So far we just built a grid 
but neglected to attach data to the grid. There are two types of data __point__ data and __cell__ data. Point data
belong the grid nodes whereas cell data associate to grid cells.

To set the point data use
```python
grid.GetPointData().SetScalars(data)
```

To set cell data use
```python
grid.GetCellData().SetScalars(data)
```

We'll start with point data
```python
python polarWithPointData.py
```

Compare this to cell data
```python
python polarWithCellData.py
```
You'll notice that the cell get a soldi colour in the case of cell data. Point data are interpolated linearly from 
each node to the neighbour node. 

### Adding colour

The default colour map in VTK maps low values to red and high values to blue! We need to fix this by adding a lookup 
table and a color bar actor. 

```python
polarWithPointDataLut.py
```