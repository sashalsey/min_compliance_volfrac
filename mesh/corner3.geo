// Gmsh project created on Tue Jan 21 15:56:14 2025
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {1, 0, 0, 1.0};
//+
Point(3) = {1, 0.4, 0, 1.0};
//+
Point(4) = {0.4, 0.4, 0, 1.0};
//+
Point(5) = {0.4, 1, 0, 1.0};
//+
Point(6) = {0, 1, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 5};
//+
Line(5) = {5, 6};
//+
Line(6) = {6, 1};
//+
Curve Loop(1) = {1, 2, 3, 4, 5, 6};
//+
Plane Surface(1) = {1};
//+
Physical Curve("wall", 7) = {5};
//+
Physical Curve("load", 8) = {3};
//+
Physical Surface("surface", 9) = {1};
//+
Transfinite Curve {5, 2} = 40 Using Progression 1;
//+
Transfinite Curve {4, 3} = 60 Using Progression 1;
//+
Transfinite Curve {6, 1} = 100 Using Progression 1;
//+
Transfinite Curve {6, 1} = 50 Using Progression 1;
//+
Transfinite Curve {4, 3} = 30 Using Progression 1;
//+
Transfinite Curve {5, 2} = 20 Using Progression 1;
