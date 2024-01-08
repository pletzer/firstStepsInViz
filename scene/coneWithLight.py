import vtk

# create a rendering window and renderer
ren = vtk.vtkRenderer()
ren.SetBackground(0.5, 0.5, 0.5)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(900, 600)

# create lights
light = vtk.vtkLight()
light.SetPosition(4, 3, 2)
light.SetColor(1, 0.5, 0.3)
light.SetIntensity(0.3)

# create another light
light2 = vtk.vtkLight()
light2.SetPosition(2, 3, 4)
light2.SetColor(1, 0, 1.0)
light2.SetIntensity(0.4)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
# create cone
cone = vtk.vtkConeSource()
cone.SetResolution(60)
 
# mapper
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())
 
# actor
coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)
 
# assign actor to the renderer
ren.AddActor(coneActor)
ren.AddLight(light)
ren.AddLight(light2)
 
# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()

