# EU Cybersecurity Incidents Dashboard

**Interactive dashboard visualizing major cybersecurity incidents impacting the European Union and their global origins.**

This project provides a **threat-intelligence-style overview** of cyber attacks affecting EU countries, using publicly available data and interactive visualizations.

---

## 🔹 Features

- **EU Cybersecurity Incidents Map**  
  Interactive choropleth of the EU, showing the number of incidents per country and top attack types.
- **Global Attacker Origin Map**  
  Shows source countries of attacks targeting the EU, helping visualize global threat origins.
- **Attack Type Distribution**  
  Interactive bar chart of attack types (DDoS, Malware, Intrusion) with dynamic y-axis scaling and margins.
- **Raw Dataset Preview**  
  Compact view of the dataset with large or unnecessary columns removed for clarity.
- **Dynamic Data Loading**  
  Automatically downloads the latest dataset from Kaggle via `kagglehub` and maps IP addresses to countries using GeoLite2.
- **Responsive and Dark-Themed Layout**  
  Maps and charts use a professional dark theme and are displayed in side-by-side columns for a compact, dashboard-like appearance.

---

## 🔹 Technologies Used

- Python 3.10+
- Streamlit — interactive web dashboard
- Pandas — data loading and manipulation
- Plotly — interactive choropleth maps and bar charts
- GeoIP2 / GeoLite2 — IP-to-country mapping
- KaggleHub — dynamic dataset download

---

## 🔹 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/eu-cyber-incidents-dashboard.git
   cd eu-cyber-incidents-dashboard
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\\Scripts\\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download GeoLite2 Database**  
   Place `GeoLite2-Country.mmdb` in the project root (see [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)).

5. **Run the dashboard**

   ```bash
   streamlit run app.py
   ```

---

## 🔹 Project Structure

```
eu-cyber-incidents/
│
├── app.py                     # Main Streamlit dashboard
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── GeoLite2-Country.mmdb      # IP geolocation database
├── data/                      # Raw and processed datasets
├── utils/                     # Helper modules (data loading, aggregation, plotting)
└── assets/                    # Images, logos, screenshots
```

---

## 🔹 How It Works

1. **Data Loading:** The latest cybersecurity attack dataset is downloaded automatically from Kaggle.
2. **IP-to-Country Mapping:** Source and destination IPs are converted to countries using GeoLite2.
3. **EU Filtering:** Only attacks affecting EU countries are included in the visualizations.
4. **Aggregation & Visualization:**
   - Incidents per EU country
   - Top attack types per country
   - Global origin of attackers
5. **Dashboard Layout:**
   - Top row: EU map + global origin map
   - Bottom row: attack type bar chart + raw dataset preview

---

## 🔹 Future Improvements

- Add top-N countries leaderboards for attackers and targets
- Include time-series analysis of attacks
- Implement interactive filters for attack type, severity, or protocol
- Export visualizations for reports or presentations

---

## 🔹 License

This project is for **portfolio and educational purposes**. Dataset used is from **Kaggle: teamincribo/cyber-security-attacks**.