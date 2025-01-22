lc = 0.05;
Point(1) = {0, 0, 0, lc};
Point(2) = {0.12, 0, 0, lc};
Point(3) = {0, 0.12, 0, lc};
Point(4) = {-0.12, 0, 0, lc};
Point(5) = {0, -0.12, 0, lc};

Circle(1) = {2, 1, 3};
Circle(2) = {3, 1, 4};
Circle(3) = {4, 1, 5};
Circle(4) = {5, 1, 2};

Curve Loop(5) = {1, 2, 3, 4};
Plane Surface(1) = {5};

height = 0.1;
layers = 10;

Extrude {0,0,height} {
  Surface{1}; Layers{ {layers}, {1} };
}
