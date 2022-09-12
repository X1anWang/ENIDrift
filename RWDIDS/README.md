# RWDIDS'22
**ENIDrift**
![GitHub](https://img.shields.io/github/license/anonymousgithubrepo/enidrift)
[![Discord Chat][discord-badge]][discord]
==

RWDIDS'22 is the first dataset containing several real world drifts. It is a **R**eal-**W**orld **D**rift dataset for network **I**ntrusion **D**etection **S**ystem. It is made because no dataset is found focusing on the dynamic distribution in reality and including various real-world drifts. RWDIDS contains network packets of 6 days in level-2, where the distribution changes gradually and real-world drift grows heavy. And the data of 4 sub-experiments in level-3 mentioned above is also from RWDIDS. They are intense real-world drift caused by concept drift and well-crafted ML attack. And the ratio of the number of packages is imbalanced and changeable in RWDIDS, posing a threat to the training and updating of NIDSs. We capture network traffic by [WireShark](https://www.wireshark.org/), extract network fields from original .pcap files to form .csv files, and open-source RWDIDS. It can be downloaded [here](https://drive.google.com/drive/folders/11Trsu4zsKJo8CBbv52j_N6BEPjcJkItu?usp=sharing). Detailed information can also be found in this [paper](https://github.com/AnonymousGithubRepo/ENIDrift/blob/main/ENIDrift.pdf).

# Network environment
<img width="332" alt="Topology of our network" src="https://user-images.githubusercontent.com/102900943/179391015-edee86e8-f82b-4bb8-ace9-d31206173b39.png">

The network topology of our dataset RWDIDS and field test is shown in the above figure. It consists of 1) computers, which connect to the router; 2) a router, which is linked to the Internet and nine IoT and Bluetooth devices (e.g., Bluetooth audio, monitors) in our office; 3) a laptop, which makes attacks to the router. IoT devices are common in real networks and are used here to make a multiple-IP and dynamic network environment, and also are a breach for well-crafted ML attacks, like data contamination. All network packets via the router are captured and copied to ENIDrift, and ENIDrift needs to use the computing source of the computer.

# Instructions

For privacy issues, we only extract the key fields used in NIDS and remove other sensitive information. The left key network fields are saved as .csv files, and can support NIDSs including but not limited to methods based on one-hot feature extraction, damped incremental statistics from [Kitsune](https://github.com/ymirsky/Kitsune-py), and iP2V (for individual conponent, see [link](https://github.com/AnonymousGithubRepo/ENIDrift/tree/main/ENIDrift/iP2V)). If you want to use damped incremental statistics from Kitsune, we provide an [adapted program](https://github.com/AnonymousGithubRepo/ENIDrift/tree/main/RWDIDS/DISKitsuneCSV) for your reference. It extracts features based on .csv network packet field.

# Distribution of RWDIDS'22

# Download

* Network fields: [link](https://drive.google.com/drive/folders/11Trsu4zsKJo8CBbv52j_N6BEPjcJkItu?usp=sharing)
* Dataset with light real-world drift: [link](https://drive.google.com/drive/folders/11Trsu4zsKJo8CBbv52j_N6BEPjcJkItu?usp=sharing)
* Fierce real-world drift: [link](https://drive.google.com/drive/folders/11Trsu4zsKJo8CBbv52j_N6BEPjcJkItu?usp=sharing)

# Measure the level of real-world drift: Drift Ratio

Real-world drift is any change of network related to our detection in real world. It covers the change of the number and proportion of different classes, newly added classes and new behavior of existing classes, ML-based well-crafted attacks from hackers, and these can be co-exist in one environment.

To give a rough measure of the level of real world drift, we introduce the *Drift Ratio* (DR) and give an error-based measurement. We have the drift ratio at time $t$
\begin{equation}
D{R^{(t)}} = 1 - \frac{{\sum\limits_{y \in Y} {{{\left\| {h_y^{(t - 1)}(S_y^{(t)})} \right\|}_0}} }}{{\left| {{S^{(t)}}} \right|}},
\end{equation}

where $y$ and $Y$ are the label and the set of labels respectively, $S^{(t)}$ is the dataset collected at time $t$, $S^{(t)}_{y}$ is a subset of $S^{(t)}$ containing the samples with the label $y$, $h^{(t-1)}_y(\cdot)$ is unsupervised classifier trained on the class $y$ previously at time $(t-1)$, and it returns $1$ if the input belongs to the class $y$, otherwise $0$.

The measurement is based on error of classification. Though choosing different types of core classifiers may bring subtle performance variance, this measurement has the advantage to include all types of drifts that may prevent our detection, which is our first priority. The formula is not designed for a specific type of drift and has strong practicability. Nearly all the challenges can be included into its scope.

<img width="400" alt="CICIDS2017-Wed with DR" src="https://user-images.githubusercontent.com/102900943/179403174-32869ebd-dafb-460b-bafd-414db555301b.png">

In the above figure, we draw the number of packets per minute of CICIDS2017-Wednesday and also compare the distribution with its DR. We find that each time new attack happens, DR is relatively high. And some oblivious mutation (e.g. the change of number of incoming packets at noon) can be captured. DR matches its distribution well.

## Community & help
* Got a question? Please get in touch via [Discord][discord] or file an [issue](https://github.com/anonymousgithubrepo/enidrift/issues).
* If you see an error message or run into an issue, please make sure to create a [bug report](https://github.com/anonymousgithubrepo/enidrift/issues).

<!-- refs -->
[license-badge]: https://img.shields.io/github/license/anonymousgithubrepo/enidrift
[discord]: https://discord.gg/BeVM624n
[discord-badge]: https://img.shields.io/badge/chat-on%20Discord-blue
