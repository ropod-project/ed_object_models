#!/usr/bin/python
import sys

if len(sys.argv) <= 1:
    print "Please provide room file"
    sys.exit(1)

room_filename = sys.argv[1]

data = {}

with open(room_filename) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        args = [arg.strip() for arg in line.split(";")]
        room = args[0]

        if not room in data:
            data[room] = {}

        data[room][args[1]] = (float(args[2].replace(",",".")), float(args[3].replace(",",".")))

for (room, info) in data.iteritems():

    center = info["center"]

    print """    - type: "door"
      id: "%s"
      pose: { x: %.2f, y: %.2f, z: 0, rz: 0 }
      shape:
          compound:
            - polygon:
                  points:""" % (room, center[0], center[1])
    
    n = 1
    if "point" in info:
        pname = info["point".format(n)]
        print "        - { x: %.2f, y: %.2f }" % (pname[0], pname[1])
        
        while True:
            if not "min{}".format(n) in info:
                break

            min = info["min{}".format(n)]
            max = info["max{}".format(n)]

            rel_min = (min[0] - center[0], min[1] - center[1])
            rel_max = (max[0] - center[0], max[1] - center[1])


            print """    - box:
        min: { x: %.2f, y: %.2f, z: 0 }
        max: { x: %.2f, y: %.2f, z: 0.01 }""" % (min[0], min[1], max[0], max[1])

            n += 1
    else:
        n = 1
        points = []
        while True:
            pname = "point{}".format(n)
            if not pname in info:
                break
            points.append(info[pname])
            n += 1

        if points:
            print """    - polygon:
        points:"""

            for p in points:
                print "                        - { x: %.2f, y: %.2f }" % (p[0], p[1])
            
            print("                  height: 2.0")

