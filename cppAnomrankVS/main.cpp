#include <array>
#include <cmath>
#include <ctime>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

#include "accuracy.hpp"
#include "anomaly_detect.hpp"
#include "anomaly_inject.hpp"
#include "edge.hpp"
#include "pagerank.hpp"
#include "read_data.hpp"

#define attackLimit 50

int main(int argc, char *argv[])
{
    clock_t start = clock();

    if (argc != 8) {
        std::cerr << "Need 8 parameters:\n";
        std::cerr << argv[0] << " path delimiter timeStep initSS injectScene injectNum injectSize\n";
        return 1;
    }
    std::string path = argv[1];
    std::string delimeter = argv[2];
    int timeStep = atoi(argv[3]);
    int initSS = atoi(argv[4]);

    int injectScene = atoi(argv[5]);
    int injectNum = atoi(argv[6]);
    int injectSize = atoi(argv[7]);
    bool INJECT = (injectScene != 0);

    // READ DATA
    std::vector<timeEdge> edges;
    std::vector<int> snapshots;
    int n, m, timeNum;
    read_data(path, delimeter, timeStep, edges, snapshots, n, m, timeNum);
    int numSS = timeNum/timeStep + 1;

    std::vector<outEdge> A(n);
    std::cout << "#node: " << n << ", #edges: "<< edges.size() << ", #timeStamp: " << timeNum << std::endl;

    // ANOMALY_SCORE
    int testNum = numSS - initSS;
    if (testNum < 0) {
        std::cerr << "Negative snapshot count" << std::endl;
        return -1;
    }
    std::vector<double> anomScore(testNum + 1, 0.0);
    bool* attack = new bool[testNum + 1]{};

    // PAGERANK
    std::array<double*, 3> pagerank1;
    std::array<double*, 3> pagerank2;
    for(size_t i = 0; i < 3; i++)
    {
        pagerank1[i] = new double[n]{};
        pagerank2[i] = new double[n]{};
    }

    // MEAN AND VARIANCE
    std::array<double*, 4> mean;
    std::array<double*, 4> var;
    for(size_t i = 0; i < 4; i++)
    {
        mean[i] = new double[n]{};
        var[i] = new double[n]{};
    }

    // INJECTED SNAPSHOT
    std::vector<int> injectSS;
    if(INJECT)
        inject_snapshot(injectNum, initSS, testNum, snapshots, injectSS);

    std::cout << "Preprocess done: " << (double)(clock() - start) / CLOCKS_PER_SEC << std::endl;

    size_t eg = 0;
    int snapshot = 0;
    int attackNum = 0;
    size_t injected = 0;
    int current_m = 0;
    //double previous_score = 100.0;

    start = clock();
    size_t print_e = 10;
    for(size_t ss = 0; ss < snapshots.size(); ss++)
    {
        while(edges[eg].t < snapshots[ss]*timeStep)
        {
            inject(A.data(), edges[eg].src, edges[eg].trg, 1);
            current_m++;
            if(edges[eg].atk)
                attackNum++;
            eg++;
            if(eg == print_e)
            {
                std::cout << eg << "," << (double)(clock() - start) / CLOCKS_PER_SEC << std::endl;
                print_e *= 10;
            }
            if(eg == edges.size())
                break;
        }

        if(INJECT && injectSS[injected] == snapshots[ss])
        {
            current_m += inject_anomaly(injectScene, A.data(), n, injectSize);
            attackNum += attackLimit;
            injected++;
            if(injected == injectSS.size())
                INJECT = false;
        }

        snapshot = snapshots[ss];
        pagerank(A.data(), pagerank1[snapshot%3], n, current_m, 1);
        pagerank(A.data(), pagerank2[snapshot%3], n, current_m, 2);

        double score = compute_anomaly_score(snapshot, pagerank1.data(), pagerank2.data(), mean.data(), var.data(), n);
        if(snapshot >= initSS)
        {
            int idx = snapshot - initSS;
            anomScore[idx] = score; //min(score, previous_score);
            attack[idx] = attackNum >= attackLimit;
            //previous_score = score;
        }
        attackNum = 0;
    }

    // WRITE ANOMALY SCORE
    std::string filePath = "darpa_anomrank.txt";
    std::ofstream writeFile(filePath.c_str(), std::ofstream::out);
    for(int i = 0; i < testNum; i++)
        writeFile << anomScore[i] << " " << int(attack[i]) << std::endl;
    writeFile.close();

    // COMPUTE ACCURACY
    for(int i = 1; i < 17; i ++)
        compute_accuracy(anomScore.data(), attack, testNum, 50*i);

    // FREE MEMORY
    for(size_t i = 0; i < 4; i++)
    {
        delete[] mean[i];
        delete[] var[i];
    }
    for(size_t i = 0; i < 3; i++)
    {
        delete[] pagerank1[i];
        delete[] pagerank2[i];
    }

    delete[] attack;

    return 0;
}
