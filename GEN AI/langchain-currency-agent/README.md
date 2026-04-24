# LangChain Multi-Step Currency Agent

An intelligent AI agent built with **LangChain** and **OpenAI** that performs multi-step reasoning to fetch real-time exchange rates and perform accurate currency conversions. 

This project demonstrates **Agentic Orchestration**—where the LLM decides which tools to use based on user intent—and **Advanced Parameter Injection** to ensure mathematical accuracy.

## 🚀 Key Features

* **Sequential Reasoning**: The agent understands dependencies (it knows it must fetch a rate before it can calculate a conversion).
* **Secure Tool Injection**: Uses `InjectedToolArg` to prevent the LLM from hallucinating exchange rates. The system injects the "truth" (API data) into the math function.
* **Real-Time Data**: Integrated with the [ExchangeRate-API](https://www.exchangerate-api.com/) for live forex data.
* **Stateful Memory**: Manages a complex flow of `HumanMessage`, `AIMessage`, and `ToolMessage` to maintain context.

## 🛠️ Tech Stack

* **Framework**: LangChain Core
* **LLM**: OpenAI GPT models
* **Networking**: Requests (Python)
* **Validation**: Pydantic & Type Annotations

### 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/langchain-currency-agent.git](https://github.com/your-username/langchain-currency-agent.git)
   cd langchain-currency-agent
2. Install dependencies:
   pip install langchain-core langchain-openai requests

3. Set up Environment Variables:
Ensure you have your OpenAI API key set in your environment:
   export OPENAI_API_KEY='your-key-here'


### How It Works
1. This agent follows a Request -> Tool -> Observation -> Reasoning loop:

2. User Input: "Convert 10 USD to INR."

3. Reasoning: AI identifies it needs the get_conversion_factor tool first.

Observation: The script executes the API call and returns the JSON payload.

4. Injection: The script extracts the rate and injects it into the convert tool, hidden from the LLM's direct input to prevent errors.

5. Final Response: The AI presents the calculated result in natural language.

### Project Structure
 1. currency_conversion.py: The main application logic containing the agent and tools.

 2. README.md: Documentation for the project.

### Example Output
    Human: Whats the conversion rate between USD and INR and convert 10 USD to INR?

AI Thought: Calling get_conversion_factor(base_currency='USD', target_currency='INR')
Tool Result: 94.1701
AI Thought: Calling convert(base_currency_value=10, conversion_factor=94.1701)

Final Answer: The current conversion rate is 94.1701. Therefore, 10 USD is 941.701 INR.
