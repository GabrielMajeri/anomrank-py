#pragma once

struct outEdge;

double* pagerank(outEdge* A, double* b, int n, int m, int version);
