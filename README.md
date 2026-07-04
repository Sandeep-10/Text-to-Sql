# Text-to-SQL Agent

An intelligent **Text-to-SQL** agent built with **LangChain**, **ChatGroq (Qwen-3 32B)**, and **MongoDB**, featuring a sleek **Gradio** web interface.

This application translates natural language requests into optimized SQLite/SQL queries, queries a MongoDB-hosted business dataset (the **Adidas Sales Database**), and returns explanations in plain English.

## 🚀 Features

- **Natural Language to SQL**: Converts complex user questions into valid SQLite SQL queries.
- **RAG/Database-Aware Reasoning**: Uses a `search_database` tool to inspect and retrieve schema and database rows from a MongoDB collection.
- **Strict Privacy Rules**: Automatically masks and restricts access to sensitive columns (`customer_email`, `phone`, `aadhaar`).
- **Robust Error Handling**: Handles vague questions, missing data, and suggests alternative queries when results are empty.
- **Modern Dark-Mode Gradio UI**: Customized CSS theme featuring high-contrast layout, tailored typography (Plus Jakarta Sans & Fira Code), and responsive layout.

## 📊 Connected Dataset: Adidas Sales Database
The agent is configured to query a dataset containing **9,648 Adidas sales transactions** across the US, containing information on:
- Retailers (Foot Locker, Amazon, Sports Direct, West Gear, Kohl's, Walmart)
- Location (Region, State, City)
- Products (Apparel, Street Footwear, Athletic Footwear) and units sold, unit prices, total sales, operating profit, and margin.
- Sales method (Online, Outlet, In-store)

## 🛠️ Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sandeep-10/Text-to-Sql.git
   cd Text-to-Sql
   ```

2. **Install Dependencies**:
   ```bash
   pip install gradio langchain langchain-groq pymongo pandas python-dotenv dnspython
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key
   mongodb_url=your_mongodb_connection_string
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
