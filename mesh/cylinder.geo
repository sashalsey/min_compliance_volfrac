// Gmsh project created on Wed Jan 22 08:02:36 2025
//+
SetFactory("OpenCASCADE");
Cylinder(1) = {0, 0, 0, 0, 0, 0.1, 0.12, 2*Pi};
//+
Physical Surface("top", 4) = {2};
//+
Physical Surface("bottom", 5) = {3};
//+
Physical Curve("tops", 6) = {1};
//+
Physical Curve("bots", 7) = {3};
