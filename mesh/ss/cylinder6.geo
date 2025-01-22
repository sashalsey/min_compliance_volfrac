// Gmsh project created on Tue Jan 21 11:18:51 2025
//+
SetFactory("OpenCASCADE");
Cylinder(1) = {0, 0, 0, 0, 0, 0, 0.12, 2*Pi};
//+
Cylinder(1) = {0, 0, 0, 0, 0, 0, 0.12, 2*Pi};
//+
Cylinder(1) = {0, 0, 0, 0, 0, 0.1, 0.12, 2*Pi};
//+
Curve Loop(4) = {1};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {3};
//+
Plane Surface(5) = {5};
//+
Physical Surface("top", 6) = {2};
//+
Physical Surface("bottom", 7) = {3};
