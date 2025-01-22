// Gmsh project created on Tue Jan 21 11:55:01 2025
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0.12, 0, 0, 1.0};
//+
Point(3) = {0, 0.12, 0, 1.0};
//+
Point(4) = {0.08, 0, 0, 1.0};
//+
Point(5) = {0, 0.08, 0, 1.0};
//+
Circle(1) = {3, 1, 2};
//+
Circle(2) = {5, 1, 4};
//+
Line(3) = {3, 5};
//+
Line(4) = {2, 4};
//+
Curve Loop(1) = {1, 4, -2, -3};
//+
Plane Surface(1) = {1};
//+
Transfinite Curve {4, 3} = 5 Using Progression 1;
//+
Transfinite Curve {2, 1} = 20 Using Progression 1;
//+
Transfinite Surface {1};
//+
Extrude {0, 0, 0.1} {
  Surface{1}; Layers {10}; Recombine;
}
//+
Physical Surface("top", 27) = {26};
//+
Physical Surface("bottom", 28) = {13, 1};
