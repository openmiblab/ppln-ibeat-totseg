import napari
print("Napari imported successfully!")

# This checks if the windowing engine can initialize without opening a viewer
from qtpy.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])
print("Qt Application initialized successfully!")

# This is the line that drops dead
viewer = napari.Viewer()
print("If you see this, it worked!")