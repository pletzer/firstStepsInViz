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

Visualization is a little like a theater play; there is a background, there are lights and actors. 

```bash
cd scene
```


## Understanding grids

## Understanding file formats
