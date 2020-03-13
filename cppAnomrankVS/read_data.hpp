#pragma once

#include <string>
#include <vector>

struct timeEdge;

void read_data(std::string path, std::string delimiter, int stepSize, std::vector<timeEdge>& edges, std::vector<int>& snapshots, int& n, int& m, int& timeNum);
