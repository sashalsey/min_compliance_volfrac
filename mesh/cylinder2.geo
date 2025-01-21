//+
SetFactory("OpenCASCADE");
Cylinder(1) = {0, 0, 0, 0, 0, 0.1, 0.12, 2*Pi};
//+
Physical Surface("bottom", 4) = {3};
//+
Physical Surface("top", 5) = {2};
