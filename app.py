import os
from langchain_groq import ChatGroq
import gradio as gr
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient
from langchain.tools import tool

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY');


model = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=groq_api_key,
    max_retries=2,
)

client = os.getenv("mongodb_url")
@tool
def search_database(query : str )->str:
    "searches the database from the mongodb through the database sql query is generated."
    client = MongoClient(client)
    collection = client['Database']['sandeep']
    data = list(collection.find({}))
    df = pd.DataFrame(data)
    return df.to_string(index=False)

system_prompt = '''
You are an intelligent Text-to-SQL agent built to query
a business database and return accurate, optimized SQL.
get the database from the search_database tool.
get the database schema from the search_database tool.
analyse and understand the database and then answer the question
YOUR BEHAVIOR:
- Convert user questions into valid SQLite SQL queries
- Always select only relevant columns — never use SELECT *
- Use table aliases (e, p, s) for readability
- Add ORDER BY when ranking or sorting is implied
- Add LIMIT 10 unless user specifies otherwise
- Use ROUND() for decimal values
- Use GROUP BY correctly with aggregate functions
PRIVACY RULES:
- Never expose columns: customer_email, phone, aadhaar
- If asked for private data, respond:
  "That data is restricted due to privacy policy."
OUTPUT FORMAT:
Thought: <brief reasoning about what the question needs>
SQL:
```sql
<your SQL query here>
```
Result Explanation: <plain English explanation of what
the query does and what the result means>
HANDLE ERRORS:
- If question is too vague → ask one clarifying question
- If question needs unavailable data → explain what is
  missing politely
- If SQL would return no results → suggest why and offer
  an alternative query'''


from langchain.agents import create_agent
from pprint import pprint


agent  = create_agent(
    tools = [search_database],
    model = model,
    system_prompt = system_prompt
)





def query_agent(user_question):
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_question}
        ]
    })
    
    return response["messages"][-1].content

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
/* Global overrides */
body, .gradio-container {
    background-color: #0A0A0C !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    color: #E4E4E7 !important;
}
/* Scrollbar customization */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0A0A0C;
}
::-webkit-scrollbar-thumb {
    background: #27272A;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3F3F46;
}
/* Header Section */
.app-header {
    padding: 2rem 0 1rem 0;
    border-bottom: 1px solid #18181B;
    margin-bottom: 2rem;
}
.header-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.1);
    color: #818CF8;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 9999px;
    border: 1px solid rgba(99, 102, 241, 0.2);
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.app-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #F4F4F5;
    margin: 0;
    letter-spacing: -0.03em;
}
.app-subtitle {
    color: #71717A;
    font-size: 0.95rem;
    margin-top: 0.4rem;
}
/* Workstation Card Panels */
.workspace-panel {
    background-color: #0F0F12 !important;
    border: 1px solid #18181B !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    transition: border-color 0.3s ease;
}
.workspace-panel:focus-within {
    border-color: rgba(99, 102, 241, 0.4) !important;
}
/* Form inputs */
textarea {
    background-color: #121216 !important;
    color: #F4F4F5 !important;
    border: 1px solid #27272A !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
    padding: 14px !important;
    line-height: 1.6 !important;
    transition: all 0.2s ease !important;
}
textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}
/* Sleek Action Button */
.action-btn {
    background-color: #6366F1 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
}
.action-btn:hover {
    background-color: #4F46E5 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.3) !important;
}
.action-btn:active {
    transform: translateY(0);
}
/* Output Area Formatting */
.output-title {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #71717A;
    margin-bottom: 0.75rem;
}
.output-markdown {
    background-color: #121216 !important;
    border-radius: 8px !important;
    border: 1px solid #18181B !important;
    padding: 1.5rem !important;
    min-height: 300px;
}
/* Markdown typography inside output */
.output-markdown h2, .output-markdown h3 {
    color: #F4F4F5 !important;
    font-weight: 600 !important;
    margin-top: 1.5rem !important;
    font-size: 1.1rem !important;
}
.output-markdown p, .output-markdown li {
    color: #A1A1AA !important;
    line-height: 1.7 !important;
    font-size: 0.95rem !important;
}
.output-markdown pre {
    background-color: #0A0A0C !important;
    border: 1px solid #18181B !important;
    border-radius: 6px !important;
    padding: 1rem !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.85rem !important;
}
.output-markdown code {
    font-family: 'Fira Code', monospace !important;
    background-color: rgba(99, 102, 241, 0.1) !important;
    color: #A5B4FC !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 0.85rem !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    # Header Section
    with gr.Column(elem_classes="app-header"):
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1 class='app-title'>Text-to-SQL Agent</h1>")
                gr.HTML("<p class='app-subtitle'>Translate natural language requests into optimized database queries.</p>")
                gr.HTML("<p class='app-subtitle'>The connected database is Adidas Sales Database</p>")

                gr.HTML(
                """
                <p class='app-subtitle'>
                    This database contains 9,648 Adidas sales transactions across the United States, 
                    covering six major retailers — Foot Locker, Amazon, Sports Direct, West Gear, 
                    Kohl's, and Walmart — spread across five regions and all 50 states. Each record 
                    captures the retailer, location (region, state, city), invoice date, gender type 
                    (Men/Women), product category (Apparel, Street Footwear, Athletic Footwear), 
                    price per unit, units sold, total sales, operating profit, operating margin, 
                    and sales method (Online, Outlet, In-store). Use the agent to explore revenue 
                    trends, compare retailer performance, analyze profit margins by region or 
                    product, and uncover what drives Adidas sales across the US market.
                </p>
                """
                ) 

                gr.HTML(
                    """
                    <p class='app-subtitle'>
                        Example : What are the total sales for each category?<br>
                        Example : Which sales method (Outlet/Online/In-store) is most profitable?<br>
                        Example : What is the best selling category for Men?
                    </p>
                    """
                )
                
                

    # Main Grid (Split 4:8 for Inputs and Outputs)
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Column(elem_classes="workspace-panel"):
                gr.HTML("<div class='output-title'>Input Query</div>")
                query_input = gr.Textbox(
                    show_label=False,
                    placeholder="Describe the data you want to retrieve...",
                    lines=4
                )
                submit_btn = gr.Button("Compile SQL", elem_classes="action-btn")

        with gr.Column(scale=2):
            with gr.Column(elem_classes="workspace-panel"):
                gr.HTML("<div class='output-title'>Result Workspace</div>")
                markdown_output = gr.Markdown(
                    value="*Compile a query on the left to display results here.*",
                    elem_classes="output-markdown"
                )

    # Event binding
    submit_btn.click(
        fn=query_agent,
        inputs=query_input,
        outputs=markdown_output
    )

if __name__ == "__main__":
    demo.launch()
