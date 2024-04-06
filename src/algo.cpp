#include <bits/stdc++.h>
#include "string.h"
#include "cpp/json.hpp"
#include <fstream>
#include <cmath>

#define rep(a, b)   for(int a = 0; a < (b); ++a)
#define all(a)      (a).begin(),(a).end()
#define endl        '\n'
#define sq(a)       (a) * (a)

using namespace std;
using json = nlohmann::json;

using Graph = vector<vector<pair<int,double>>>;
using ll = long long;
using ull = unsigned long long;

struct Edge {
    int from, to, flow, cap, cost;
    Edge* rev = nullptr;
};

// vector<vector<Edge*>> adj;
vector<Edge*> pre;
vector<ll> dist;

const int PUMPBUILDINGCOST = 100;
const int HOUSECONSUMPTION = 73;
const int PIPECOST = 1;

void add_edge(vector<vector<Edge*>> &adj, int a, int b, int cap, int cost) {
    auto e1 = new Edge{a, b, 0, cap, cost};
    auto e2 = new Edge{b, a, 0, 0, -cost};
    e1->rev = e2;
    e2->rev = e1;
    adj[a].push_back(e1);
    adj[b].push_back(e2);
}

bool bellmann_ford(vector<vector<Edge*>> &adj, int s, int t) {
    queue<int> Q;
    vector<bool> in_Q (adj.size(), false);
    Q.push(s);
    bool found = false;
    fill(dist.begin(), dist.end(), INT_MAX);
    dist[s] = 0ll;

    while (!Q.empty()) {
        int v = Q.front(); Q.pop();
        if (v == t) found = true;
        in_Q[v] = false;
        for (auto &edge : adj[v]) {
            if (edge->flow == edge->cap) continue;
            int cost = 0;
            if (edge->flow == 0) {
                cost = edge->cost;
            }
            // int cost = 0 ? edge->flow : edge->cost;
            ll new_dist = dist[v] + cost;
            if (new_dist >= dist[edge->to]) continue;
            dist[edge->to] = new_dist;
            pre[edge->to] = edge;
            if (!in_Q[edge->to]) {
                Q.push(edge->to);
                in_Q[edge->to] = true;
            }
        }
    }
    return found;
}

ll max_flow (vector<vector<Edge*>> &adj, int s, int t) {
    ll flow = 0ll;
    dist = vector<ll> (adj.size());
    pre = vector<Edge*> (adj.size(), nullptr);

    while (true) {
        if (!bellmann_ford(adj, s, t)) break;
        // int c_flow = 1;
        int c_flow = INT_MAX;
        for (int v = t; v != s; v = pre[v]->from) {
            c_flow = min(c_flow, pre[v]->cap - pre[v]->flow);
        }
        for (int v = t; v != s; v = pre[v]->from) {
            pre[v]->flow += c_flow;
            pre[v]->rev->flow -= c_flow;
        }
        flow += c_flow;
    }
    return flow;
}

// Function to convert degrees to radians
double degToRad(double deg) {
    return (deg * M_PI / 180.0);
}
// Function to calculate the distance between two points
// given their latitude and longitude in degrees
double haversineDistance(double lat1, double lon1, double lat2, double lon2) {
    // Earth's radius in kilometers
    const double R = 6371.0;
    // Convert latitude and longitude from degrees to radians
    lat1 = degToRad(lat1);
    lon1 = degToRad(lon1);
    lat2 = degToRad(lat2);
    lon2 = degToRad(lon2);
    // Differences in coordinates
    double dLat = lat2 - lat1;
    double dLon = lon2 - lon1;
    // Apply Haversine formula
    double a = pow(sin(dLat / 2), 2) +
               cos(lat1) * cos(lat2) * pow(sin(dLon / 2), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double distance = R * c;
    return distance * 1000;
}

struct Building {
    int id;
    double x;
    double y;
    string type;
    double base_area;
    double area;
    int cluster;
    int oldCluster;
};

struct Roads {
    int id;
    double x;
    double y;
};

struct Areas {
    int id;
    double x;
    double y;
    double area;
    double base_area;
};

struct Cluster {
    double x;
    double y;
    vector<int> nodes;
    double mean;
    double stdev;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.precision(10);

    string dir = "../our_data/50";

    ifstream data_file(dir + "/graph.json", std::ifstream::binary);
    json data;
    data_file >> data;

    json graph = data.at("graph");
    json buildingsJson = data.at("buildings");
    json areasJson = data.at("areas");
    json roadsJson = data.at("roads");

    int numberPoints = graph.size();

    Graph G = Graph(numberPoints);

    for (auto row : graph) {
        auto id = row.at("id");
        for (auto c : row.at("children")) {
            auto id2 = c.at("Node");
            auto dist = c.at("Distance");
            G[id].push_back({id2, dist});
        }
    }

    vector<Building> buildings = vector<Building>(buildingsJson.size());
    for (int i=0; i<buildings.size(); i++) {
        buildings[i].id = buildingsJson[i].at("id");
        auto center = buildingsJson[i].at("center");
        buildings[i].x = center.at("lat");
        buildings[i].y = center.at("lon");
        buildings[i].type = buildingsJson[i].at("type");
        buildings[i].base_area = buildingsJson[i].at("base_area");
        buildings[i].area = buildingsJson[i].at("area");
    }

    vector<Roads> roads = vector<Roads>(roadsJson.size());
    for (int i=0; i<roads.size(); i++) {
        roads[i].id = roadsJson[i].at("id");
        auto point = roadsJson[i].at("point");
        roads[i].x = point.at("lat");
        roads[i].y = point.at("lon");
    }

    vector<Areas> areas = vector<Areas>(areasJson.size());
    for (int i=0; i<areas.size(); i++) {
        areas[i].id = areasJson[i].at("id");
        auto center = areasJson[i].at("center");
        areas[i].x = center.at("lat");
        areas[i].y = center.at("lon");
        areas[i].base_area = areasJson[i].at("base_area");
        areas[i].area = areasJson[i].at("area");
    }

    ifstream cluster_file(dir + "/clusters.json", std::ifstream::binary);
    json cluster_data;
    cluster_file >> cluster_data;

    vector<Cluster> clusters = vector<Cluster>(cluster_data.size());
    int clusterNumber = clusters.size();
    for (int i=0; i<clusterNumber; i++) {
        auto center = cluster_data[i].at("center");
        clusters[i].x = center[0];
        clusters[i].y = center[1];
        for (int nei : cluster_data[i].at("nodes")) {
            clusters[i].nodes.push_back(nei);
            buildings[nei].cluster = i;
            buildings[nei].oldCluster = i;
        }
    }

    // remove outlier
    vector<Cluster> newClusters = vector<Cluster> (clusterNumber+1);
    vector<vector<bool>> inCluster = vector<vector<bool>> (clusterNumber+1, vector<bool> (G.size()));
    for (int i=0; i<clusterNumber; i++) {
        double centerX = clusters[i].x;
        double centerY = clusters[i].y;
        int clusterSize = clusters[i].nodes.size();

        vector<double> distances = vector<double>(clusterSize);

        double stdev = 0;
        double mean = 0;
        for (int j=0; j<clusterSize; j++) {
            int node = clusters[i].nodes[j];
            distances[j] = haversineDistance(centerX, centerY, buildings[node].x, buildings[node].y);
            mean += distances[j] / clusterSize;
            stdev += sq(distances[j]) / clusterSize;
        }
        stdev = sqrt(stdev);

        double maxDist = mean + 2 * stdev;

        newClusters[i].x = clusters[i].x;
        newClusters[i].y = clusters[i].y;
        newClusters[i].mean = mean;
        newClusters[i].stdev = stdev;

        for (int j=0; j<clusterSize; j++) {
            int node = clusters[i].nodes[j];

            if (distances[j] > maxDist) {
                buildings[node].cluster = clusterNumber;
                newClusters[clusterNumber].nodes.push_back(node);
            } else {
                newClusters[i].nodes.push_back(node);
                inCluster[i][node] = true;
            }
        }
    }

    // find cluster graphs
    for (int i=0; i<newClusters.size(); i++) {
        double centerX = newClusters[i].x;
        double centerY = newClusters[i].y;
        for (auto road : roads) {
            double pointX = road.x;
            double pointY = road.y;
            double d = haversineDistance(centerX, centerY, pointX, pointY);

            inCluster[i][road.id] = d <= (newClusters[i].mean + 2 * newClusters[i].stdev);
        }
    }


    // add flow network
    vector<vector<vector<Edge*>>> adjs = vector<vector<vector<Edge*>>> (clusterNumber, vector<vector<Edge*>> (G.size() + 2));
    json output;
    vector<json> clusterJsons = vector<json> (clusterNumber);
    for (int j=0; j<clusterNumber; j++) {
    // for (int j=1; j<2; j++) {
        int clusterSize = newClusters[j].nodes.size();
        for (int i=0; i<buildings.size(); i++) {
            int id = buildings[i].id;
            if (inCluster[j][id]) {
                add_edge(adjs[j], 0, id+2, INT_MAX, PUMPBUILDINGCOST);
                add_edge(adjs[j], id+2, 1, HOUSECONSUMPTION, 0);
            }
        }

        for (int i=0; i<G.size(); i++) {
            if (inCluster[j][i]) {
                for (auto [nei, weight] : G[i]) {
                    if (inCluster[j][nei]) {
                        add_edge(adjs[j], i+2, nei+2, INT_MAX, weight * PIPECOST);
                    }
                }
            }
        }
        auto flow = max_flow(adjs[j], 0, 1);

        vector<pair<double, double>> out_buildings = vector<pair<double, double>> (clusterSize);
        for (int x=0; x<clusterSize; x++) {
            out_buildings[x].first = buildings[newClusters[j].nodes[x]].x;
            out_buildings[x].second = buildings[newClusters[j].nodes[x]].y;
        }
        vector<pair<double, double>> out_pumps = vector<pair<double, double>> ();
        for (auto edge : adjs[j][0]) {
            if (edge->from == 0 && edge->flow > 0) {
                int id = edge->to - 2;
                out_pumps.push_back({buildings[id].x, buildings[id].y});
            }
        }
        vector<vector<pair<double,double>>> connections = vector<vector<pair<double,double>>> ();
        for (int p=2; p<adjs[j].size(); p++) {
            for (auto edge : adjs[j][p]) {
                if (edge->from != 0 && edge->from != 1 && edge->to != 0 && edge->to != 1 && edge->flow > 0) {
                    pair<double,double> first, second;

                    int id1 = edge->from - 2;
                    int id2 = edge->to - 2;

                    if (id1 < buildings.size()) {
                        first = {buildings[id1].x, buildings[id1].y};
                    } else {
                        id1 -= buildings.size() + areas.size();
                        first = {roads[id1].x, roads[id1].y};
                    }

                    if (id2 < buildings.size()) {
                        second = {buildings[id2].x, buildings[id2].y};
                    } else {
                        id2 -= buildings.size() + areas.size();
                        second = {roads[id2].x, roads[id2].y};
                    }

                    if (first.first < 40 || first.first > 60  || first.second < 5 || first.second > 20) {
                        cout << edge->from-2 << " " << edge->to-2 << endl;
                    } else if (second.first < 40 || second.first > 60  || second.second < 5 || second.second > 20) {
                        cout << edge->from-2 << " " << edge->to-2 << endl;
                    }
                    connections.push_back({first, second});
                }
            }
        }

        vector<pair<double, double>> out_outliers = vector<pair<double, double>> ();
        for (auto b : buildings) {
            if (b.oldCluster == j && b.cluster != b.oldCluster) {
                out_outliers.push_back({b.x, b.y});
            }
        }

        clusterJsons[j]["buildings"] = out_buildings;
        clusterJsons[j]["outliers"] = out_outliers;
        clusterJsons[j]["pumps"] = out_pumps;
        clusterJsons[j]["connections"] = connections;

        cout << j+1 << " / " << clusterNumber << endl;
        cout.flush();
    }

    output["clusters"] = clusterJsons;


    // Öffnen Sie eine Datei zum Schreiben
    std::ofstream file("../our_output.json");

    // Überprüfen, ob das Öffnen erfolgreich war
    if (!file.is_open()) {
        std::cerr << "Error opening file for writing!" << endl;
        return 1;
    }

    // Schreiben Sie das JSON-Objekt in die Datei
    file << output.dump(4); // Die dump-Methode konvertiert das JSON-Objekt in einen String mit Einzügen für eine bessere Lesbarkeit
    // Schließen Sie die Datei
    file.close();

    return 0;
}