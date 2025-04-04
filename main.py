from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent , AgentExecutor
from tools import search_tool, wiki_tool, save_tool


# Load environment variables
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize ChatOpenAI without manually fetching the key
llm = ChatOpenAI(model="gpt-4o-mini")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Wrap the output in thi format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),   
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
#important for context
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("How can I help you Today? \n\n")
raw_response = agent_executor.invoke({"query": query})
print(raw_response,"\n")

# structured_response = parser.parse(raw_response["output"])
# print(structured_response)
