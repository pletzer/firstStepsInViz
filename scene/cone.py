import vtk

# create a  rendering window and renderer
ren = vtk.vtkRenderer()
ren.SetBackground(0.5, 0.5, 0.5)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(900, 600)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
# create cone
cone = vtk.vtkConeSource()
 
# mapper
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())
 
# actor
coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)
 
# assign actor to the renderer
ren.AddActor(coneActor)
 
# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()

