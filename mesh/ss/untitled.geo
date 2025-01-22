//+
SetFactory("OpenCASCADE");
Circle(1) = {0, -0, 0, 0.5, 0, 2*Pi};
//+
Recursive Delete {
  Curve{1}; 
}
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0.5, 0, 0, 1.0};
//+
Point(3) = {0.5, 0.25, 0, 1.0};
//+
Point(4) = {0, 0.5, 0, 1.0};
//+
Point(5) = {0.25, 0.5, 0, 1.0};
//+
Point(6) = {0.25, 0.25, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 6};
//+
Line(4) = {6, 5};
//+
Line(5) = {5, 4};
//+
Line(6) = {4, 1};
//+
Curve Loop(1) = {3, 4, 5, 6, 1, 2};
//+
Plane Surface(1) = {1};
//+
Physical Curve("wall", 7) = {5};
//+
Physical Curve("wall", 7) += {5};
//+
Physical Curve("load", 8) = {3};
//+
Physical Surface("fluid", 9) = {1};
//+
Show "*";
