# Neuron_Code Repository

A comprehensive collection of neural networks, machine learning models, and programming tutorials focusing on scientific and engineering applications, particularly in material science.

## Repository Overview

This repository contains implementations, tutorials, and examples spanning various domains:

- Machine learning algorithms and data analysis
- Neural network architectures (RNN, CNN)
- Scientific computing applications
- Programming fundamentals in Python
- Database integrations using various technologies
- Docker configurations for database environments

## Directory Structure

### CS229

Stanford's Machine Learning course implementations:

- `01_Linear_Regression.py`: Basic linear regression implementation
- `02_Zomato_Data_Analysis.py`: Data analysis of restaurant data
- `03_Wine_Quality_Prediction.py`: ML model for wine quality prediction
- Supporting datasets: Wine-Quality.csv, Zomato-data-.csv

### MIT_6.S191

MIT's Deep Learning course implementations:

- `01_Learn_Gradient_Descent_Using_Linear_Regression.py`: Custom gradient descent implementation
- `02_Recurrent_Neural_Network.py` & `03_Recurrent_Neural_Network.py`: RNN implementations
- `04_Sin_Wave_Generator_Using_RNN.py`: Generating sine waves using RNNs
- `05_Convolution_Neural_Network.ipynb`: CNN implementation

### MIST_Conference

Material science research for conference:

- `Algae_Biofuel_Data_for_MIST_conf.py`: Analysis of algae biofuel data
- `Algae_Biofuel_Data_for MIST conf.csv`: Dataset for biofuel analysis

### Tutorials

Programming tutorials organized by topic:

- `01_Basics`: Fundamental programming concepts
- `02_Basics_OOP`: Object-oriented programming principles
- `03_Decorators`: Python decorator patterns and usage
- `04_Error_Handling`: Exception management techniques
- `05_Database_Sqlite3`: SQLite database integration
- `06_Handling_APIs`: API interaction examples
- `07_Database_MongoDB`: MongoDB integration

### docker-databases

Docker configurations for database environments:

- `mongodb`: MongoDB container configuration
- `mysql`: MySQL container setup
- `postgresql`: PostgreSQL configuration
- `redis`: Redis server and client setup

## Technologies Used

- **Programming Languages**: Python
- **Machine Learning**: scikit-learn, NumPy, Pandas
- **Deep Learning**: PyTorch, TensorFlow (via implementations)
- **Data Visualization**: Matplotlib, Seaborn
- **Notebooks**: Marimo (Jupyter alternative)
- **Databases**: SQLite, MongoDB, MySQL, PostgreSQL, Redis
- **Containerization**: Docker

## Usage

### Setting Up the Environment

1. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

2. For database examples, use the Docker configurations:
   ```
   cd docker-databases/<database-name>
   docker-compose up
   ```

### Running the Examples

- **Python Scripts**: Execute with Python interpreter

  ```
  python <script_name>.py
  ```

- **Marimo Notebooks**: Run with marimo
  ```
  marimo run <notebook_name>.py
  ```

### Working with Specific Modules

- **CS229 (Machine Learning)**: Explore statistical models and data analysis techniques
- **MIT_6.S191 (Deep Learning)**: Learn neural network architectures and implementations
- **MIST_Conference**: Review material science analyses and research code
- **Tutorials**: Step through various programming concepts from basic to advanced

## License

This repository contains educational materials and implementations for learning purposes.
