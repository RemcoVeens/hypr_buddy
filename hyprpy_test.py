from hyprpy import Hyprland
from hyprpy.utils.shell import run_or_fail

instance = Hyprland()


# Fetch active window and display information:
window = instance.get_active_window()
print(window.wm_class)
print(window.width)
print(window.position_x)


# Print information about the windows on the active workspace
workspace = instance.get_active_workspace()
for window in workspace.windows:
    print(f"{window.address}: {window.title} [{window.wm_class}]")


# Get the resolution of the first monitor
monitor = instance.get_monitor_by_id(0)
if monitor:
    print(f"{monitor.width} x {monitor.height}")


# Get all windows currently on the special workspace
special_workspace = instance.get_workspace_by_name("special")
if special_workspace:
    special_windows = special_workspace.windows
    for window in special_windows:
        print(window.title)


# Show a desktop notification every time we switch to workspace 6
def on_workspace_changed(sender, **kwargs):
    workspace_id = kwargs.get("workspace_id")
    print(f"now on workspace: {workspace_id}")
    if workspace_id == 6:
        run_or_fail(["notify-send", "We are on workspace 6."])


instance.signals.workspacev2.connect(on_workspace_changed)
instance.watch()
