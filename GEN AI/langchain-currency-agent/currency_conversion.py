from langchain_core.tools import tool 
from langchain_core.tools import InjectedToolArg
import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Annotated
import json

llm = ChatOpenAI()


#tool create

@tool
def get_conversion_factor( base_currency : str , target_currency : str ) -> float:
    """ this function fetches the currency convervsion factor betwwen base currency and target currenct"""

    url = f"https://v6.exchangerate-api.com/v6/____API_KEY___/pair/{base_currency}/{target_currency}" 

    response = requests.get(url)

    return response.json()

# result = get_conversion_factor.invoke( { "base_currency" : "USD" , "target_currency" : "INR"})
# print(result)


@tool
def convert( base_currency_value : float , conversion_factor : Annotated[ float , InjectedToolArg] ) -> float:
    """ given a conversion rate this function calculates the target currency value from the given base currency value """
    return ( base_currency_value * conversion_factor )

result_final = convert.invoke( { "base_currency_value" : 10 , "conversion_factor" : 94.1701})


# print(result_final)

# tool binding
llm_binded = llm.bind_tools([ get_conversion_factor , convert])


messages = [ HumanMessage("What is the conversion factor between INR and USD, and based on that can you convert 94.1701 inr to usd")]


# print(messages)

ai_message = llm_binded.invoke(messages)

messages.append(ai_message)




# print(ai_message.tool_calls)




for tool_call in ai_message.tool_calls:
    # execute the first tool to get the conversion rate 

    if tool_call["name"] == "get_conversion_factor":
        tool_message1 = get_conversion_factor.invoke(tool_call)
        # print(tool_message1)
        

        #fetch conversion rate
        converson_rate_of_currency = json.loads(tool_message1.content)["conversion_rate"] # tool_message1.content["conversion_rate"] gives a json and not dictionary thus use json_load
        # print(converson_rate_of_currency)
        

        #append this meesage to the message list 
        messages.append(tool_message1)

    # execute the second tool using the conversion rate from tool 1 
    if tool_call["name"] == "convert":
        # fetch the current argument
        tool_call["args"]["conversion_factor"] = converson_rate_of_currency

        tool_message2 = convert.invoke(tool_call)
        messages.append(tool_message2)



# print(messages)


converted_value = llm_binded.invoke(messages).content

print(converted_value)