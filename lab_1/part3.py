import re, math, pandas as pd

path="motion_1_all.bvh"
with open(path,"r") as f:
    text=f.read()

# Split header and motion
header, motion = text.split("MOTION")
header_lines=header.splitlines()

joint_stack=[]
channels=[]
joint_channels={}
for line in header_lines:
    if "ROOT" in line or "JOINT" in line:
        name=line.split()[1]
        joint_stack.append(name)
    if "End Site" in line:
        joint_stack.append("End")
    if "}" in line:
        if joint_stack: joint_stack.pop()
    if "CHANNELS" in line:
        parts=line.split()
        n=int(parts[1])
        ch=parts[2:2+n]
        joint=joint_stack[-1]
        joint_channels.setdefault(joint,[]).extend(ch)
        for c in ch:
            channels.append((joint,c))

motion_lines=[l.strip() for l in motion.splitlines() if re.match(r"^[\d\-\.\s]+$",l)]
frames=[list(map(float,l.split())) for l in motion_lines]
df=pd.DataFrame(frames,columns=[f"{j}_{c}" for j,c in channels])

def get_peak(joint):
    cols=[c for c in df.columns if c.startswith(joint) and "rotation" in c.lower()]
    xcol=[c for c in cols if "Xrotation" in c][0]
    series=df[xcol]
    return series.min(), series.max()

results={}
for joint in ["Head","Neck","neck","head"]:
    if any(c.startswith(joint+"_") for c in df.columns):
        results[joint]=get_peak(joint)

print(results)