#include "read_data.hpp"

#include <algorithm>
#include <fstream>
#include <iostream>
#include "edge.hpp"

struct compare_edge
{
    inline bool operator() (const timeEdge& struct1, const timeEdge& struct2)
    {
        return (struct1.t < struct2.t);
    }
};

void read_data(std::string path, std::string delimiter, int stepSize, std::vector<timeEdge>& edges, std::vector<int>& snapshots, int& n, int& m, int& timeNum)
{
    std::vector<int> nodes;
    std::vector<int> times;

    std::ifstream graphFile(path.c_str());
    std::string line;
    while(getline(graphFile, line))
    {
        size_t pos = 0;
        std::vector<int> tokens;
        while ((pos = line.find(delimiter)) != std::string::npos)
        {
            tokens.push_back(std::stoi(line.substr(0, pos)));
            line.erase(0, pos + delimiter.length());
        }
        tokens.push_back(std::stoi(line));

        edges.push_back(timeEdge(tokens));
        times.push_back(tokens[0]);
        nodes.push_back(tokens[1]);
        nodes.push_back(tokens[2]);
    }

    graphFile.close();

    std::sort(edges.begin(), edges.end(), compare_edge());
    std::sort(times.begin(), times.end());
    std::sort(nodes.begin(), nodes.end());

    int initial_time = times[0];
    int initial_node = nodes[0];
    for(size_t i = 0; i < edges.size(); i++)
    {
        edges[i].t -= initial_time;
        edges[i].src -= initial_node;
        edges[i].trg -= initial_node;
    }

    n = nodes[nodes.size()-1] - initial_node + 1;
    m = edges.size();
    timeNum = times[times.size()-1] - initial_time + 1;

    int step = 1;
    for(size_t i = 0; i < edges.size(); i++)
    {
        if(edges[i].t > step*stepSize)
        {
            snapshots.push_back(step);
            step = edges[i].t/stepSize + 1;

        }
    }
    if (!snapshots.empty() && step != *(snapshots.rbegin())) {
        snapshots.push_back(step);
    }
}
