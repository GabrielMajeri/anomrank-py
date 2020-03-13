#include "anomaly_inject.hpp"
#include "edge.hpp"
#include <algorithm>

void inject(outEdge* A, int u, int v, int num)
{
    bool inserted = false;
    for(size_t nb = 0; nb < A[u].out.size(); nb++)
    {
        if(A[u].out[nb] != v)
            continue;
        A[u].weight[nb] += num;
        A[u].total_w += num;
        inserted = true;
        break;
    }

    if(inserted == false)
    {
        A[u].out.push_back(v);
        A[u].weight.push_back(num);
        A[u].total_w += num;
    }
}

double inject_anomaly(int scenario, outEdge* A, size_t n, size_t edgeNum)
{
    switch(scenario){
        case 1: // add whole weights to one edge
        {
            int u;
            do{
                u = std::rand()%n;
            }while(A[u].out.size() == 0);

            int v_n = std::rand()%(A[u].out.size());
            int v = A[u].out[v_n];
            inject(A, u, v, edgeNum);
            return edgeNum;
        }
        case 2: // distribute whole weights to out-edges
        {
            int u;
            do{
                u = std::rand()%n;
            }while(A[u].out.size()==0);

            if(edgeNum < A[u].out.size())
            {
                for(size_t i = 0; i < edgeNum; i++)
                    inject(A, u, A[u].out[i], 1);
            }
            else
            {
                size_t edgeOne = edgeNum/A[u].out.size();
                for(size_t i = 0; i < A[u].out.size(); i++)
                    inject(A, u, A[u].out[i], edgeOne);
                size_t edgeRest = edgeNum - edgeOne*A[u].out.size();
                inject(A, u, A[u].out[0], edgeRest);
            }
            return edgeNum;
        }
        case 3: // distribute whole edges to unseen edges from one source
        {
            int u = std::rand()%n;
            std::vector<int> v(edgeNum);
            size_t added = 0;
            size_t tried = 0;
            while(added < edgeNum && tried < n)
            {
                int v_n = std::rand()%n;
                if(find(A[u].out.begin(), A[u].out.end(), v_n) == A[u].out.end())
                {
                    v[added] = v_n;
                    added++;
                }
                tried++;
            }

            for(size_t i = 0; i < added; i++)
                inject(A, u, v[i], 1);

            return added;
        }
        case 4:
        {
            std::vector<int> v(edgeNum);
            int v_n = std::rand()%n;
            v[0] = v_n;
            size_t added = 1;
            size_t tried = 0;
            while(added < edgeNum && tried < n)
            {
                bool unseen = true;
                v_n = std::rand()%n;
                for(size_t i = 0; i < added; i++)
                {
                    if(v_n == v[i])
                    {
                        unseen = false;
                        break;
                    }
                    if(find(A[v[i]].out.begin(), A[v[i]].out.end(), v_n) != A[v[i]].out.end())
                    {
                        unseen = false;
                        break;
                    }
                }

                if(unseen)
                {
                    v[added] = v_n;
                    added++;
                }
                tried++;
            }

            for(size_t i = 0; i < added; i++)
            {
                for(size_t j = i+1; j < added; j++)
                    inject(A, v[i], v[j], 1);
            }

            return added*(added-1);
        }
    }
    return 0;
}

void inject_snapshot(int injectNum, int initSS, int testNum, std::vector<int>& snapshots, std::vector<int>& injectSS)
{
    int injected = 300;
    for(int i = 0; i < injectNum; i++)
    {
        do{
            injected = initSS + rand()%testNum;
        }while(find(injectSS.begin(), injectSS.end(), injected) != injectSS.end());

        injectSS.push_back(injected);
        if(find(snapshots.begin(), snapshots.end(), injected) == snapshots.end())
            snapshots.push_back(injected);
    }
    std::sort(snapshots.begin(), snapshots.end());
    std::sort(injectSS.begin(), injectSS.end());
}
