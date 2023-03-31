import os, time, shutil, math
from string import Template

###########################
#      template.kml       #
###########################

TEMPLATE_FILE_HEAD_TEMPLATE = Template("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:wpml="http://www.dji.com/wpmz/1.0.2">
  <Document>
    <wpml:author>fly</wpml:author>
    <wpml:createTime>$creationTime</wpml:createTime>
    <wpml:updateTime>$creationTime</wpml:updateTime>
    <wpml:missionConfig>
      <wpml:flyToWaylineMode>safely</wpml:flyToWaylineMode>
      <wpml:finishAction>goHome</wpml:finishAction>
      <wpml:exitOnRCLost>goContinue</wpml:exitOnRCLost>
      <wpml:executeRCLostAction>goBack</wpml:executeRCLostAction>
      <wpml:globalTransitionalSpeed>4</wpml:globalTransitionalSpeed>
      <wpml:droneInfo>
        <wpml:droneEnumValue>68</wpml:droneEnumValue>
        <wpml:droneSubEnumValue>0</wpml:droneSubEnumValue>
      </wpml:droneInfo>
    </wpml:missionConfig>
  </Document>
</kml>""")

###########################
#      waylines.wpml      #
###########################

HEAD_TEMPLATE = Template("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:wpml="http://www.dji.com/wpmz/1.0.2">
  <Document>
    <wpml:missionConfig>
      <wpml:flyToWaylineMode>safely</wpml:flyToWaylineMode>
      <wpml:finishAction>goHome</wpml:finishAction>
      <wpml:exitOnRCLost>goContinue</wpml:exitOnRCLost>
      <wpml:executeRCLostAction>goBack</wpml:executeRCLostAction>
      <wpml:globalTransitionalSpeed>4</wpml:globalTransitionalSpeed>
      <wpml:droneInfo>
        <wpml:droneEnumValue>68</wpml:droneEnumValue>
        <wpml:droneSubEnumValue>0</wpml:droneSubEnumValue>
      </wpml:droneInfo>
    </wpml:missionConfig>
    <Folder>
      <wpml:templateId>0</wpml:templateId>
      <wpml:executeHeightMode>relativeToStartPoint</wpml:executeHeightMode>
      <wpml:waylineId>0</wpml:waylineId>
      <wpml:distance>0</wpml:distance>
      <wpml:duration>0</wpml:duration>
      <wpml:autoFlightSpeed>4</wpml:autoFlightSpeed>
        $waypoints
    </Folder>
  </Document>
</kml>""")

GLOBAL_SETTINGS_TEMPLATE = Template("""

""")

WAYPOINT_TEMPLATE = Template("""
      <Placemark>
        <Point>
            <coordinates>
                $lon $lat
            </coordinates>
        </Point>
        <wpml:index>$index</wpml:index>
        <wpml:executeHeight>$height</wpml:executeHeight>
        <wpml:waypointSpeed>4</wpml:waypointSpeed>
        <wpml:waypointHeadingParam>
          <wpml:waypointHeadingMode>followWayline</wpml:waypointHeadingMode>
          <wpml:waypointHeadingAngle>0</wpml:waypointHeadingAngle>
          <wpml:waypointPoiPoint>0.000000,0.000000,0.000000</wpml:waypointPoiPoint>
          <wpml:waypointHeadingAngleEnable>1</wpml:waypointHeadingAngleEnable>
          <wpml:waypointHeadingPathMode>followBadArc</wpml:waypointHeadingPathMode>
        </wpml:waypointHeadingParam>
        <wpml:waypointTurnParam>
          <wpml:waypointTurnMode>toPointAndStopWithDiscontinuityCurvature</wpml:waypointTurnMode>
          <wpml:waypointTurnDampingDist>0</wpml:waypointTurnDampingDist>
        </wpml:waypointTurnParam>
        <wpml:useStraightLine>1</wpml:useStraightLine>$action_group
      </Placemark>
""")

FIRST_WAYPOINT_AG = """
        <wpml:actionGroup>
          <wpml:actionGroupId>1</wpml:actionGroupId>
          <wpml:actionGroupStartIndex>0</wpml:actionGroupStartIndex>
          <wpml:actionGroupEndIndex>0</wpml:actionGroupEndIndex>
          <wpml:actionGroupMode>parallel</wpml:actionGroupMode>
          <wpml:actionTrigger>
            <wpml:actionTriggerType>reachPoint</wpml:actionTriggerType>
          </wpml:actionTrigger>
          <wpml:action>
            <wpml:actionId>1</wpml:actionId>
            <wpml:actionActuatorFunc>gimbalRotate</wpml:actionActuatorFunc>
            <wpml:actionActuatorFuncParam>
              <wpml:gimbalHeadingYawBase>aircraft</wpml:gimbalHeadingYawBase>
              <wpml:gimbalRotateMode>absoluteAngle</wpml:gimbalRotateMode>
              <wpml:gimbalPitchRotateEnable>1</wpml:gimbalPitchRotateEnable>
              <wpml:gimbalPitchRotateAngle>-90</wpml:gimbalPitchRotateAngle>
              <wpml:gimbalRollRotateEnable>0</wpml:gimbalRollRotateEnable>
              <wpml:gimbalRollRotateAngle>0</wpml:gimbalRollRotateAngle>
              <wpml:gimbalYawRotateEnable>0</wpml:gimbalYawRotateEnable>
              <wpml:gimbalYawRotateAngle>0</wpml:gimbalYawRotateAngle>
              <wpml:gimbalRotateTimeEnable>0</wpml:gimbalRotateTimeEnable>
              <wpml:gimbalRotateTime>0</wpml:gimbalRotateTime>
              <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
            </wpml:actionActuatorFuncParam>
          </wpml:action>
        </wpml:actionGroup>
"""

WAYPOINT_AG_TEMPLATE = Template("""
        <wpml:actionGroup>
          <wpml:actionGroupId>$agId</wpml:actionGroupId>
          <wpml:actionGroupStartIndex>$index</wpml:actionGroupStartIndex>
          <wpml:actionGroupEndIndex>$index</wpml:actionGroupEndIndex>
          <wpml:actionGroupMode>parallel</wpml:actionGroupMode>
          <wpml:actionTrigger>
            <wpml:actionTriggerType>reachPoint</wpml:actionTriggerType>
          </wpml:actionTrigger>
          <wpml:action>
            <wpml:actionId>$aId</wpml:actionId>
            <wpml:actionActuatorFunc>gimbalEvenlyRotate</wpml:actionActuatorFunc>
            <wpml:actionActuatorFuncParam>
              <wpml:gimbalPitchRotateAngle>-90</wpml:gimbalPitchRotateAngle>
              <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
            </wpml:actionActuatorFuncParam>
          </wpml:action>
        </wpml:actionGroup>
""")

WAYPOINT_AG_HOVER_TEMPLATE = Template("""
        <wpml:actionGroup>
          <wpml:actionGroupId>$agId</wpml:actionGroupId>
          <wpml:actionGroupStartIndex>$index</wpml:actionGroupStartIndex>
          <wpml:actionGroupEndIndex>$index</wpml:actionGroupEndIndex>
          <wpml:actionGroupMode>sequence</wpml:actionGroupMode>
          <wpml:actionTrigger>
            <wpml:actionTriggerType>reachPoint</wpml:actionTriggerType>
          </wpml:actionTrigger>
          <wpml:action>
            <wpml:actionId>$aId</wpml:actionId>
            <wpml:actionActuatorFunc>gimbalEvenlyRotate</wpml:actionActuatorFunc>
            <wpml:actionActuatorFuncParam>
              <wpml:gimbalPitchRotateAngle>-90</wpml:gimbalPitchRotateAngle>
              <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
            </wpml:actionActuatorFuncParam>
          </wpml:action>
          <wpml:action>
            <wpml:actionId>$aIdP1</wpml:actionId>
            <wpml:actionActuatorFunc>hover</wpml:actionActuatorFunc>
            <wpml:actionActuatorFuncParam>
              <wpml:hoverTime>1.5</wpml:hoverTime>
            </wpml:actionActuatorFuncParam>
          </wpml:action>
          <wpml:action>
            <wpml:actionId>$aIdP2</wpml:actionId>
            <wpml:actionActuatorFunc>takePhoto</wpml:actionActuatorFunc>
            <wpml:actionActuatorFuncParam>
              <wpml:payloadPositionIndex>0</wpml:payloadPositionIndex>
            </wpml:actionActuatorFuncParam>
          </wpml:action>
        </wpml:actionGroup>
""")

# These will be used to remove waypoints that are too close to each other
EARTH_RADIUS = 6378.137

def distanceBetweenPoints(a, b):
    
    #return abs(2 * EARTH_RADIUS * math.sin(math.sqrt(math.sin((b[0] - a[0]) / 2) ** 2 + math.cos(a[0]) * math.cos(b[0]) * math.sin((b[1] - a[1]) / 2) ** 2)) ** -1)

    #dlat = b[0] * math.pi / 180 - a[0] * math.pi / 180
    #dlon = b[1] * math.pi / 180 - a[1] * math.pi / 180
    dlat = (b[0] - a[0]) * math.pi / 180
    dlon = (b[1] - a[1]) * math.pi / 180
    ab = math.sin(dlat / 2) ** 2 + math.cos(a[0] * math.pi / 180) * math.cos(b[0] * math.pi / 180) * (math.sin(dlon / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(ab), math.sqrt(1 - ab))
    d = EARTH_RADIUS * c

    return d * 1000 # distance in METERS

if __name__ == "__main__":
       
    # Import .kml file from QGroundControl
    shape_file = input("Drag and drop shape .kml file: ")

    # Choose Waypoint Mode
    hover_and_take = input("Hover and Take Picture? [Y/N] (Defaults to False) ")
    if hover_and_take:
        hover_and_take = True if hover_and_take.lower() == "y" else False
    else:
        hover_and_take = False

    # Gather Point Data
    shape_coordinates = []
    with open(shape_file, "r") as sf:
        lines = sf.read()
        name_index = lines.index("<name>Flight Path</name>")
        coord_index = lines[name_index:].index("<coordinates>") + 13
        lcoord_index = lines[name_index:].index("</coordinates>")

        raw_coords = lines[name_index + coord_index : name_index + lcoord_index].strip()
        split_vec = raw_coords.split("\n")
        shape_coordinates = [[float(c) for c in v.split(",")] for v in split_vec[1:]]

    print(shape_coordinates)

    # Create new .kmz file
    output_file = input("Enter output path: ")
    if output_file:
        os.chdir(os.path.dirname(output_file))
    else:
        os.chdir(os.path.dirname(__file__))
    
    try:
        os.mkdir("./wpmz")
    except:
        pass  # Assuming folder can't be created because it already exists

    # Write 'template.kml' file
    template_file = TEMPLATE_FILE_HEAD_TEMPLATE.substitute(creationTime=int(time.time()))
    with open("./wpmz/template.kml", "w") as tf:
        tf.write(template_file)

    # Write 'waylines.wpml' file
    #waylines_file = HEAD_TEMPLATE.substitute(waypoints=[WAYPOINT_TEMPLATE.substitute(lon=w[1], lat=w[0], index=shape_coordinates.index(w), height=altitude) for w in shape_coordinates])
    waylines_file = ""
    action_group_id = 2
    action_id = 2
    for w in shape_coordinates:
        indx = shape_coordinates.index(w)
        ag = ""
        # TO DO: Remove waypoints that are too close to each other
        if indx == 0:
            ag += FIRST_WAYPOINT_AG + WAYPOINT_AG_TEMPLATE.substitute(index=indx, agId=action_group_id, aId=action_id)
            action_id += 1
        #elif indx == len(shape_coordinates) - 1:
        #    ag = ""
        else:
            if hover_and_take:
                ag += WAYPOINT_AG_HOVER_TEMPLATE.substitute(index=indx, agId=action_group_id, aId=action_id, aIdP1=action_id+1, aIdP2=action_id+2)
                action_id += 3
            else:
              ag += WAYPOINT_AG_TEMPLATE.substitute(index=indx, agId=action_group_id, aId=action_id)
              action_id += 1
        action_group_id += 1
        waylines_file += WAYPOINT_TEMPLATE.substitute(lon=w[0], lat=w[1], index=indx, height=w[2], action_group=ag)

    waylines = HEAD_TEMPLATE.substitute(waypoints=waylines_file)
    waylines = "\n".join([s.rstrip() for s in waylines.splitlines() if s.strip()])
    with open("./wpmz/waylines.wpml", "w") as wf:
        wf.write(waylines)

    # Compress folder into .kmz file
    shutil.make_archive("temp", "zip", "./", "./wpmz")
    shutil.move("temp.zip", "temp.kmz")
    print("File saved in " + os.path.abspath("temp.kmz"))