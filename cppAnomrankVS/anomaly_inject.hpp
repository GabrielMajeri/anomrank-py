#pragma once

#include <vector>
struct outEdge;

void inject(outEdge* A, int u, int v, int num);
double inject_anomaly(int scenario, outEdge* A, size_t n, size_t edgeNum);
void inject_snapshot(int injectNum, int initSS, int testNum, std::vector<int>& snapshots, std::vector<int>& injectSS);
