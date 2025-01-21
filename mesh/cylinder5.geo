// Gmsh project created on Tue Jan 21 10:48:57 2025
//+
SetFactory("OpenCASCADE");
Cylinder(1) = {0, 0, 0, 0, 0, 0.1, 0.12, 2*Pi};
//+
Physical Surface("bottom", 4) = {3};
//+
Physical Surface("top", 5) = {2};
