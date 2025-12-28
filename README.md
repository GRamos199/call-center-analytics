<div align="center">

# 📊 Call Center Analytics Dashboard

[![Tests](https://github.com/GRamos199/call-center-analytics/actions/workflows/test.yml/badge.svg)](https://github.com/GRamos199/call-center-analytics/actions/workflows/test.yml)
[![Terraform](https://github.com/GRamos199/call-center-analytics/actions/workflows/terraform.yml/badge.svg)](https://github.com/GRamos199/call-center-analytics/actions/workflows/terraform.yml)
[![Deploy](https://github.com/GRamos199/call-center-analytics/actions/workflows/deploy.yml/badge.svg)](https://github.com/GRamos199/call-center-analytics/actions/workflows/deploy.yml)
[![Pages](https://github.com/GRamos199/call-center-analytics/actions/workflows/pages.yml/badge.svg)](https://github.com/GRamos199/call-center-analytics/actions/workflows/pages.yml)

**A modern, interactive Streamlit dashboard for call center performance analytics**

[Live Preview](https://gramos199.github.io/call-center-analytics/) • [Documentation](#documentation) • [Getting Started](#getting-started)

<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Streamlit-1.40-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/AWS-ECS_Fargate-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS">
<img src="https://img.shields.io/badge/Terraform-1.6-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform">

</div>

---

## 🎯 Overview

Call Center Analytics is a comprehensive dashboard that provides real-time insights into call center operations. Built with Streamlit and designed with a modern UI, it offers intuitive visualizations for monitoring KPIs, agent performance, and channel metrics.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📊 **Multi-Period Analysis** | Switch between monthly and weekly reports |
| 📈 **Interactive Charts** | Dynamic visualizations with Plotly |
| 👥 **Agent Performance** | Individual agent metrics and rankings |
| 📡 **Channel Analytics** | Phone, Email, Chat, WhatsApp breakdown |
| 🎨 **Modern UI** | Animated gradients and glassmorphism design |
| 🐳 **Docker Ready** | One-command deployment with Docker Compose |
| ☁️ **AWS Infrastructure** | Production-ready Terraform for ECS Fargate |
| 🔄 **CI/CD Pipeline** | Automated testing, building, and deployment |

---

## 🖼️ Screenshots

<div align="center">

| Welcome Page | Monthly Report |
|:------------:|:--------------:|
| ![Welcome](https://via.placeholder.com/400x250/1a1a2e/ffffff?text=Welcome+Page) | ![Monthly](https://via.placeholder.com/400x250/1a1a2e/ffffff?text=Monthly+Report) |

</div>

> 📸 **Live Preview**: Visit the [GitHub Pages](https://gramos199.github.io/call-center-analytics/) for full dashboard screenshots and PDF download.

---

##  Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[👤 User Browser]
    end
    
    subgraph "Application Layer"
        B[🎨 Streamlit Frontend]
        C[📊 Plotly Charts]
        D[🎯 Dashboard Logic]
    end
    
    subgraph "Data Layer"
        E[📁 CSV Data Files]
        F[🔄 Data Loader]
        G[📈 Metric Calculator]
    end
    
    A --> B
    B --> C
    B --> D
    D --> F
    F --> E
    F --> G
    G --> D
    
```

---

## 📁 Project Structure

```
call-center-analytics/
├── 📂 analytics/                 # Main application
│   ├── 📄 app.py                 # Streamlit entry point
│   ├── 📂 classes/               # UI components
│   │   ├── �� content_tabs/      # Tab content renderers
│   │   ├── 📄 base_tab.py        # Base tab class
│   │   ├── 📄 monthly_tab.py     # Monthly view
│   │   ├── 📄 weekly_tab.py      # Weekly view
│   │   └── 📄 style_manager.py   # CSS styling
│   ├── �� reporting/             # Report logic
│   │   ├── 📂 monthly/           # Monthly calculations
│   │   ├── 📂 weekly/            # Weekly calculations
│   │   └── 📄 welcome_page.py    # Welcome animation
│   ├── 📂 utils/                 # Utilities
│   │   ├── 📄 data_loader.py     # Data loading
│   │   ├── 📄 metric_loader.py   # KPI calculations
│   │   └── 📄 data_generator.py  # Synthetic data
│   └── 📂 data/                  # CSV data files
│       ├── 📂 monthly/           # Monthly datasets
│       └── 📂 weekly/            # Weekly datasets
├── 📂 terraform/                 # AWS Infrastructure
│   ├── 📄 main.tf                # Provider config
│   ├── 📄 vpc.tf                 # Network setup
│   ├── 📄 ecs.tf                 # Container service
│   ├── 📄 alb.tf                 # Load balancer
│   └── 📄 ...                    # Other resources
├── 📂 .github/workflows/         # CI/CD Pipelines
│   ├── 📄 test.yml               # Testing workflow
│   ├── 📄 terraform.yml          # Infrastructure
│   ├── 📄 deploy.yml             # Deployment
│   └── 📄 pages.yml              # Documentation
├── 📂 tests/                     # Test suite
├── 📄 Dockerfile                 # Container image
├── 📄 docker-compose.yml         # Local deployment
└── 📄 requirements.txt           # Python dependencies
```

---

## �� Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional)
- AWS CLI (for cloud deployment)

### Local Development

```bash
# Clone the repository
git clone https://github.com/GRamos199/call-center-analytics.git
cd call-center-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
cd analytics
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

---

## ☁️ AWS Deployment

The project includes complete Terraform infrastructure for deploying to AWS ECS Fargate.

```mermaid
graph LR
    subgraph "Internet"
        A[🌐 Users]
    end
    
    subgraph "AWS Cloud"
        subgraph "VPC"
            B[⚖️ ALB]
            subgraph "Private Subnets"
                C[🐳 ECS Fargate]
                D[�� ECS Fargate]
            end
        end
        E[📦 ECR]
        F[📊 CloudWatch]
    end
    
    A --> B
    B --> C
    B --> D
    C --> F
    D --> F
    E -.-> C
    E -.-> D
    
```

### Deploy with Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply infrastructure
terraform apply
```

### AWS Resources Created

| Resource | Description |
|----------|-------------|
| VPC | Isolated network with public/private subnets |
| ECS Cluster | Fargate serverless container platform |
| ECR | Docker image registry |
| ALB | Application Load Balancer with health checks |
| Auto Scaling | CPU/Memory-based scaling policies |
| CloudWatch | Logging and monitoring with alarms |
| IAM Roles | Secure execution and task roles |

---

## 🔄 CI/CD Pipeline

```mermaid
flowchart LR
    subgraph "Trigger"
        A[📝 Push to Main]
    end
    
    subgraph "Test Pipeline"
        B[🔍 Lint]
        C[🧪 Unit Tests]
        D[🔗 Integration]
        E[🔒 Security]
    end
    
    subgraph "Build Pipeline"
        F[🐳 Docker Build]
        G[📦 Push to ECR]
    end
    
    subgraph "Deploy Pipeline"
        H[🏗️ Terraform Plan]
        I[🚀 Deploy to ECS]
    end
    
    subgraph "Docs Pipeline"
        J[📸 Screenshots]
        K[📄 GitHub Pages]
    end
    
    A --> B --> C --> D --> E
    E --> F --> G --> I
    A --> H
    A --> J --> K
    
```

### Workflow Files

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `test.yml` | Push/PR | Linting, testing, security scan |
| `terraform.yml` | Terraform changes | Infrastructure validation and deployment |
| `deploy.yml` | Push to main | Docker build and ECS deployment |
| `pages.yml` | Push to main | Generate screenshots and publish docs |

---

## 📊 Metrics & KPIs

The dashboard tracks the following key performance indicators:

```mermaid
mindmap
  root((📊 KPIs))
    Efficiency
      ⏱️ Average Handle Time
       First Call Resolution
      💰 Cost per Interaction
    Volume
      📈 Total Interactions
       Active Agents
      📊 Interactions per Agent
    Quality
      ⭐ Customer Satisfaction
      ✅ Resolution Rate
      📉 Wait Time
    Channels
      📞 Phone
      📧 Email
      💬 Chat
      📱 WhatsApp
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Frontend** | Streamlit, Plotly, Custom CSS |
| **Backend** | Python 3.12, Pandas, NumPy |
| **Containerization** | Docker, Docker Compose |
| **Infrastructure** | Terraform, AWS ECS Fargate |
| **CI/CD** | GitHub Actions |
| **Testing** | Pytest, Black, isort, Flake8 |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=analytics --cov-report=html

# Code formatting
black analytics/
isort analytics/ --profile black

# Linting
flake8 analytics/
```

---

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Application port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Bind address | `0.0.0.0` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using Streamlit**

[⬆️ Back to Top](#-call-center-analytics-dashboard)

</div>
