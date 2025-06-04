# SDN-Enabled Serverless Architecture

This project demonstrates a complete end-to-end system that integrates Software Defined Networking (SDN) with serverless computing (AWS Lambda) for intelligent DDoS attack detection. It involves real-time traffic monitoring in Mininet-based SDN topologies, data logging via custom SDN controllers (POX, Ryu, Floodlight), machine learning model training for attack classification, and model deployment via serverless APIs.

---

## 📁 Repository Structure

```
SDN-Enabled-Serverless-Architecture/
├── Topologies/            # Custom Mininet topologies
├── POX/                   # POX controller-based packet logger and feature extractor
├── RYU/                   # Ryu controller setup and DDoS logger
├── Floodlight/            # Floodlight flow collector and REST polling
├── Ddos-ML/               # ML training scripts, evaluation reports
├── AWS-Lambda/            # Lambda handler code and API Gateway instructions
├── requirements.txt       # Python dependencies
└── README.md              # Project overview and setup instructions
```

---

## ⚙️ Prerequisites

* Ubuntu (preferably 20.04 or 22.04) in VirtualBox or native
* Python 3.8+
* Mininet (`sudo apt install mininet`)
* Open vSwitch (`sudo apt install openvswitch-switch`)
* Git, pip, virtualenv
* AWS account with Lambda + API Gateway access

---

## 🌐 1. Mininet Topology Setup

> Navigate to `Topologies/` and use `custom_topo.py`

### ▶ Run Custom Topology

```bash
cd Topologies
sudo python3 custom_topo.py
```

This creates a two-switch, four-host tree topology.

---

## 🎛️ 2. SDN Controllers

### ✅ POX Controller

1. Clone POX:

```bash
git clone https://github.com/noxrepo/pox.git
cd pox
```

2. Place `pox_logger.py` or `ddos_features_logger.py` inside `pox/ext`

3. Run Controller:

```bash
python3 pox.py log.level --DEBUG openflow.discovery ext.pox_logger
```

> Outputs CSV `traffic_data.csv` with 10+ features and dynamic DDoS labels

---

### ✅ Ryu Controller

1. Create a virtual environment:

```bash
python3 -m venv ryuenv
source ryuenv/bin/activate
pip install ryu
```

2. Place `ryu_ddos_logger.py` in project folder

3. Run Ryu app:

```bash
ryu-manager ryu_ddos_logger.py
```

4. Run Mininet topology connected to Ryu:

```python
net = Mininet(topo=topo,
              controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633))
```

---

### ✅ Floodlight Controller

1. Clone Floodlight:

```bash
git clone https://github.com/floodlight/floodlight.git
cd floodlight
sudo apt install ant
ant
```

2. Start Floodlight:

```bash
java -jar target/floodlight.jar
```

3. Use `floodlight_logger.py` to poll REST API:

```bash
python3 floodlight_logger.py
```

> Collects flow statistics via `http://localhost:8080/wm/core/switch/all/flow/json`

---

## 🧠 3. Machine Learning Pipeline (Ddos-ML/)

### 💾 Data Collected

* Features: `pktcount`, `byteperflow`, `totalkbps`, `flows`, `protocol`, `duration`, etc.
* Classes: `normal`, `ddos`

### 🧪 Model Training & Tuning

File: `first.py`

* Algorithms: Random Forest, SVM, KNN, XGBoost, ANN
* Tuning: GridSearch + RandomSearch for 100+ hyperparam combinations

### 📊 Results Summary:

| Model         | Accuracy | F1 Score | Best Params                              |
| ------------- | -------- | -------- | ---------------------------------------- |
| Random Forest | 96.25%   | 0.96     | `n_estimators=100, max_depth=None, log2` |
| SVM           | 92.75%   | 0.93     | `C=100, kernel=poly, gamma=auto`         |
| KNN           | 94.75%   | 0.95     | `n_neighbors=11, weights=distance`       |
| XGBoost       | 96.50%   | 0.97     | `depth=3, learning_rate=0.2, gamma=0.1`  |
| ANN (Keras)   | 93.25%   | 0.94     | Tuned layers, units, dropout, optimizer  |

---

## ☁️ 4. Serverless Deployment (AWS-Lambda/)

### 🔁 API Workflow

```
Client → API Gateway → Lambda → Predict → Return JSON (normal / ddos)
```

### 🪄 Lambda Function

* `lambda_function.py`: Reads feature vector, simulates classification
* Handles POST body: `{ "features": [..8 float values..] }`
* Outputs: `{ "prediction": 0 or 1 }`

### 🧩 Deployment Steps

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda)
2. Create Function → Python 3.8
3. Upload ZIP file with `lambda_function.py`
4. Deploy and copy ARN

### 🌐 Connect API Gateway

1. Go to [API Gateway Console](https://console.aws.amazon.com/apigateway)
2. Create REST API → Resource `/predict`
3. Add POST method → Link to Lambda → Enable Lambda Proxy
4. Deploy to stage: `prod`

Example Endpoint:

```
https://abc123.execute-api.us-east-1.amazonaws.com/prod/predict
```

### 🚀 Test From Client (Colab / Python)

```python
import requests, json
features = [-1.22, -0.99, 3.0, 3.0, 0.0, -0.99, 0.0, -0.83]
res = requests.post(
  url, headers={"Content-Type": "application/json"},
  data=json.dumps({"features": features})
)
print(res.json())
```

---

## 📌 Additional Notes

* ✅ **Concurrency**: Lambda + API Gateway supports 30+ concurrent requests (customizable stage limits)
* ✅ **Flexibility**: Modular controller logic across POX, Ryu, and Floodlight
* ✅ **Lightweight**: Low-latency predictions under 150ms for hardcoded or deployed models

---

## 🧾 requirements.txt (partial)

```txt
scikit-learn
xgboost
pandas
numpy
matplotlib
seaborn
requests
tensorflow
keras
tensorflow-addons
```

---

## 📚 References

* [Mininet Docs](http://mininet.org)
* [POX GitHub](https://github.com/noxrepo/pox)
* [Ryu Docs](https://osrg.github.io/ryu)
* [Floodlight](http://www.projectfloodlight.org/floodlight)
* [AWS Lambda Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)

---

## 📬 Contact

For collaboration or questions, reach out via [LinkedIn](https://www.linkedin.com/) or open an issue in this repository.

---

> 🚀 **Built to demonstrate intelligent SDN systems with scalable cloud-native inference!**
