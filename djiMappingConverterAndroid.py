import os, sys, time, math, shutil, math
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
            <wpml:actionActuatorFunc>hover</wpml:actionActuatorFunc>
            <wpml:actionActuatorFuncParam>
              <wpml:hoverTime>3</wpml:hoverTime>
            </wpml:actionActuatorFuncParam>
          </wpml:action>
        </wpml:actionGroup>
""")

# These will be used to remove waypoints that are too close to each other
# Vicenty's Formula (could be replaced by 'geopy.distance.distance().m' if you have 'geopy' installed (Remember to 'import geopy'))
ELLIPSOIDS = {
    'WGS-84':        (6378137,     6356752.3142,  1 / 298.257223563), # General
    'GRS-80':        (6378137,     6356752.3141,  1 / 298.257222101), # North America, Australia
    'Airy (1830)':   (6377563.396, 6356256.909,   1 / 299.3249646),   # UK
    'Intl 1924':     (6378388,     6356911.946,   1 / 297.0),         # Europe
    'Clarke (1880)': (6378249.145, 6356514.86955, 1 / 293.465),       # Africa
    'GRS-67':        (6378160.0,   6356774.719,   1 / 298.25)         # South America
}

def vicentyFormula(point_a, point_b, model=ELLIPSOIDS["WGS-84"]):
    a = model[0]
    b = model[1]
    f = model[2]

    lat1 = point_a[1]
    lon1 = point_a[0]

    lat2 = point_b[1]
    lon2 = point_b[0]

    L = math.radians(lon2 - lon1)
    U1 = math.atan2((1 - f) * math.sin(math.radians(lat1)), math.cos(math.radians(lat1)))
    U2 = math.atan2((1 - f) * math.sin(math.radians(lat2)), math.cos(math.radians(lat2)))
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    lambdaa = L
    lambdaaP = 2 * math.pi

    while abs(lambdaa - lambdaaP) > 10e-12:
        sinLambda = math.sin(lambdaa)
        cosLambda = math.cos(lambdaa)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        if sinSigma == 0:
            return 0

        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        alpha = math.asin(cosU1 * cosU2 * sinLambda / sinSigma)
        cosSqAlpha = math.cos(alpha) ** 2
        cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        lambdaaP = lambdaa
        lambdaa = L + (1 - C) * f * math.sin(alpha) * (
                    sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)))

    uSq = cosSqAlpha * (a ** 2 - b ** 2) / b ** 2
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (
                cos2SigmaM + B / 4 *
                (cosSigma *
                 (-1 + 2 *
                  cos2SigmaM ** 2) -
                 B / 6 *
                 cos2SigmaM *
                 (-3 + 4 *
                  sinSigma ** 2) *
                 (-3 + 4 *
                  cos2SigmaM ** 2)))

    s = b * A * (sigma - deltaSigma)

    return s

# Haversine Formula
EARTH_RADIUS = 6372.795
def haversineFormula(a, b):
    dlat = (b[0] - a[0]) * math.pi / 180
    dlon = (b[1] - a[1]) * math.pi / 180
    ab = math.sin(dlat / 2) ** 2 + math.cos(a[0] * math.pi / 180) * math.cos(b[0] * math.pi / 180) * (math.sin(dlon / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(ab), math.sqrt(1 - ab))
    d = EARTH_RADIUS * c

    return d * 1000 # distance in METERS

def sortType(lst, tp):
  new = []
  for el in lst:
    if tp in el:
      new.append(el)

  return new

def sortDate(lst):
  latest_date = 0
  latest_file = None
  for fl in lst:
    if os.stat(fl).st_mtime_ns > latest_date:
      latest_date = os.stat(fl).st_mtime_ns
      latest_file = fl

  return latest_file

if __name__ == "__main__":
    
    hover_and_take = input("Hover and Take Picture? [Y/N] (Defaults to False) ")
    if hover_and_take:
        hover_and_take = True if hover_and_take.lower() == "y" else False
    else:
        hover_and_take = False

    # Choose if we should remove SUCCESSIVE waypoints that are too close to each other (Recommended, defaults to True)
    # Make sure that, in QGroundControl, you use a Turnaround Distance higher or equal than the minimum distance
    waypoint_distance_threshold = 2 # Minimum distance between two SUCCESSIVE waypoints in meters
    filter_waypoints = input("Filter successive waypoints that are too close to each other? [Y/N] (Defaults to True) ")
    if filter_waypoints:
        filter_waypoints = False if filter_waypoints.lower() == "n" else True
    else:
        filter_waypoints = True

    if filter_waypoints:
        # Define minimum distance in meters
        waypoint_distance_threshold = input("Minimum distance in meters between two successive waypoints: (Defaults to 2) ")
        waypoint_distance_threshold = float(waypoint_distance_threshold) if waypoint_distance_threshold else 2

        # Choose Ellipsoid (or Great Circle) model for the most accurate distance measurement (Defaults to WGS-84, but Haversine's formula should work just fine for short distances and it's much faster to compute)
        earth_model = input("Choose Earth model to compute waypoint distances accurately: [0-6] (Defaults to 0, General)\n  0 General Most globally accurate\n  1 North America/Australia\n  2 UK\n  3 Europe\n  4 Africa\n  5 South America\n  6 Haversine's formula (faster, least accurate)\n0 (general) is recommended: ")
        if earth_model:
            earth_model = int(earth_model)
        else:
            earth_model = 0

    # Import .kml file from QGroundControl
    os.chdir("/storage/emulated/0/Download")
    kml_files = sortType(os.listdir(), ".kml")

    shape_file = sortDate(kml_files)

    # Gather Point Data
    shape_coordinates = []
    excess_height = 0 # Used to fix Altitude mismatch
    with open(shape_file, "r") as sf:
        lines = sf.read()
        name_index = lines.index("<name>Flight Path</name>")
        coord_index = lines[name_index:].index("<coordinates>") + 13
        lcoord_index = lines[name_index:].index("</coordinates>")

        raw_coords = lines[name_index + coord_index : name_index + lcoord_index].strip()
        split_vec = raw_coords.split("\n")
        excess_height = float(split_vec[0].split(",")[2])
        shape_coordinates = [[float(c) for c in v.split(",")] for v in split_vec[1:]]

    """
    # Move to DJI Fly waypoint folder
    os.chdir("/storage/emulated/0/Android/data/dji.go.v5/files/waypoint")
    waypoint_folder = sortDate([f for f in os.listdir() if f != "map_preview"])

    if input(f"\nLatest '.kml' file found: {shape_file}\n\nLatest waypoint folder found: {waypoint_folder}\n\nConfirm to continue. [Y] ").lower() != "y":
      sys.exit()

    ### Since Android 10 access to app data folder is forbidden ###
    """

    os.chdir("/storage/emulated/0/Download")
    try:
        os.mkdir("./wpmz")
    except:
        pass

    # Write 'template.kml' file
    template_file = TEMPLATE_FILE_HEAD_TEMPLATE.substitute(creationTime=int(time.time()))
    with open("./wpmz/template.kml", "w") as tf:
        tf.write(template_file)

    # Write 'waylines.wpml' file
    #waylines_file = HEAD_TEMPLATE.substitute(waypoints=[WAYPOINT_TEMPLATE.substitute(lon=w[1], lat=w[0], index=shape_coordinates.index(w), height=altitude) for w in shape_coordinates])
    waylines_file = ""
    action_group_id = 2
    action_id = 2
    skip = False # Used to skip waypoints too close to each other
    skipped = 0  # Keep track of how many waypoints are skipped (to fix waypoint index)
    for w in shape_coordinates:
        indx = shape_coordinates.index(w)
        ag = ""

        if skip:
            print(f"Skipped waypoint {indx}")
            skipped += 1
            skip = False
            continue

        if filter_waypoints:
            if indx != len(shape_coordinates) - 1: # Check if we're writing the last waypoint
                distance = vicentyFormula(w, shape_coordinates[indx + 1], ELLIPSOIDS[list(ELLIPSOIDS.keys())[earth_model]]) if earth_model != 6 else haversineFormula(w, shape_coordinates[indx + 1])
                if distance < waypoint_distance_threshold:
                    skip = True

        if indx == 0:
            ag += FIRST_WAYPOINT_AG + WAYPOINT_AG_TEMPLATE.substitute(index=indx, agId=action_group_id, aId=action_id)
        #elif indx == len(shape_coordinates) - 1:
        #    ag = ""
        else:
            if hover_and_take:
                ag += WAYPOINT_AG_HOVER_TEMPLATE.substitute(index=indx-skipped, agId=action_group_id, aId=action_id)
            else:
              ag += WAYPOINT_AG_TEMPLATE.substitute(index=indx-skipped, agId=action_group_id, aId=action_id)
        action_id += 1
        action_group_id += 1
        waylines_file += WAYPOINT_TEMPLATE.substitute(lon=w[0], lat=w[1], index=indx, height=w[2] - excess_height, action_group=ag)

    waylines = HEAD_TEMPLATE.substitute(waypoints=waylines_file)
    waylines = "\n".join([s.rstrip() for s in waylines.splitlines() if s.strip()])
    with open("./wpmz/waylines.wpml", "w") as wf:
        wf.write(waylines)

    # Compress folder into .kmz file
    shutil.make_archive("temp", "zip", "./", "./wpmz")
    shutil.move("temp.zip", "temp.kmz")
    print("File saved in " + os.path.abspath("temp.kmz"))
    #shutil.move("temp.zip", f"/storage/emulated/0/Android/data/dji.go.v5/files/waypoint/{waypoint_folder}/{waypoint_folder}.kmz")