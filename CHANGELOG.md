## 2023-04-19
- \[**ADDED**\] Option to choose if waypoints should have Gimbal Pitch set to -90°. (Defaults to True, set it to False for Photogrammetry/Structure Scan Missions)
- \[**FIXED**\] "Hover and Take Picture" is now changed to "Take Picture at each Waypoint". This makes the drone take pictures at each waypoint, however it's not going to hover, for that you can try the updated [Workaround to Hover and Take Picture](https://github.com/LOLsW/DJIMavic3Mapping#workaround-to-hover-and-take-picture). Also, either in DJI Fly or by manually controlling it, if you use this option for mapping remember to rotate the gimbal pitch to -90. You can set the first waypoint of the mission to do this or do it manually before starting the mission
- \[**FIXED**\] Waypoints that appear to be facing the wrong direction actually work properly, that is just a graphics bug, it finally happened to me in a mission I could actually fly and it flew perfectly

### IMPORTANT (READ ALL OF IT):
While trying to get the "Hover and Take Picture" option to work properly, I changed to code to basically recreate a 1:1 copy of a mission that I had created and flown inside the DJI Fly app.
That mission had every waypoint (including the last one, it's important to keep this in mind for later) set to: 
1. Take Photo 
2. Hover for 2 seconds

Although the generated .kmz file was nearly identical to the one created by DJI Fly (the only change was the time of creation), the mission still failed to run. So I finally tried using only the Take Photo action and I got that to 'work'.
Furthermore: if you use "Take Picture at each Waypoint" no waypoint will have the gimbal pitch set to -90° because that created a weird patterns with actionIds, but you can change it in DJI Fly as the first waypoint setting or manually while flying. (I may find a solution for this later)
At this point I assume there's something wrong with either DJI Fly or the way the drone itself reads the missions, because I really did recreate PERFECTLY a mission that WORKED in DJI Fly.

Because of the fact that I changed the scripts to allow you to choose if waypoints should have Gimbal Pitch set to -90°, there's one small change that also affects the code that only creates waypoints and waypoints with Gimbal Pitch -90, specifically: previously the code would create the first waypoint with an hard-coded action group that was the same regardless of the options you chose when running the script, specifically: it would have one action ("gimbalRotate" and it's "PitchAngle" would be set to -90). Now the first waypoint is identical to the other ones, it now follows the options you define, which can be:
- Nothing (No action, if you set "Gimbal Pitch to -90" and "Take Picture at each Waypoint" both to False)
- **gimbalEvenlyRotate** set to -90; This action differentiates from **gimbalRotate** as it only controls the Pitch axis, while **gimbalRotate** can also control Yaw and Roll
- **takePhoto**
Now, although this is the only change (for this part of the code) from the previous version of the scripts, somehow the last waypoint cannot have any actions. Doesn't matter if I add an action to it via the DJI Fly app or through the scripts, if the last waypoint of the mission has any action, immediately after uploading to the drone the mission would fail.
This only really affects the "Take Picture at each Waypoint" kind of missions as the other ones have no useful action going on on it. I'm pointing this out because if you change a setting in a waypoint in DJI Fly and press "Apply to All", it'll apply to the last waypoint as well and the mission will fail. The solution is simple: just remove any action from the last waypoint before running the mission. Everything else will work perfectly fine.

To end this on a side-note: you really only need the first waypoint to set the Gimbal Pitch because unless you edit the other waypoints' Gimbal Pitch settings they will not move the Gimbal in any way.

## 2023-04-16
- \[**ADDED**\] The scripts now warn the user that the "Hover and Take Picture" option does not work yet

## 2023-04-05
- \[**ADDED**\] Option for waypoint filtering based on distance between **SUCCESSIVE** waypoints. It include several Earth models to calculate the most accurate distance based on geographic region
- \[**ADDED**\] When using "djiMappingConverter.py", once the processing is done, the script will wait for input before it closes (allowing you to view the output path if the script is run by double clicking)
- \[**FIXED**\] Height/Altitude mismatch is now completely fixed. (It works even when Altitude mode in QGroundControl is set to 'Calculated Above Terrain')
- \[**FIXED**\] The code now cleans the path/to/kml_file by removing quotes and the starting '&' (could cause problems on Windows)

I've also tried to clean and improve the 'Hover and take picture' part (to include a part of its workaround), but apparently now is even worse. BUT the workaround still works