from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
import os


class TrendingCompany(BaseModel):
    """ 一家在新闻中受到关注的公司 """
    name: str = Field(description="公司名称")
    ticker: str = Field(description="股票代码")
    reason: str = Field(
        description="该公司在新闻中热门的原因")


class TrendingCompanyList(BaseModel):
    """ 新闻中多个热门公司的列表 """
    companies: List[TrendingCompany] = Field(
        description="新闻中热门公司的列表")


class TrendingCompanyResearch(BaseModel):
    """ 对公司的详细研究 """
    name: str = Field(description="公司名称")
    market_position: str = Field(
        description="当前市场地位和竞争分析")
    future_outlook: str = Field(
        description="未来展望和增长前景")
    investment_potential: str = Field(
        description="投资潜力和投资适宜性")


class TrendingCompanyResearchList(BaseModel):
    """ 所有公司详细研究的列表 """
    research_list: List[TrendingCompanyResearch] = Field(
        description="对所有热门公司的全面研究")


@CrewBase
class No3StockPicker():
    """No3StockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()], memory=True)

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], tools=[PushNotificationTool()], memory=True)

    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'], output_pydantic=TrendingCompanyList)

    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'], output_pydantic=TrendingCompanyResearchList)

    @task
    def pick_best_company(self) -> Task:
        return Task(config=self.tasks_config['pick_best_company'])

    @crew
    def crew(self) -> Crew:
        """Creates the No3StockPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'], allow_delegation=True)

        # 创建记忆
        short_term_memory = ShortTermMemory(
            storage=RAGStorage(
                type="short_term",
                path="./memory",
                embedder_config={
                    "provider": "ollama",
                    "config": {
                        "model": "mxbai-embed-large",
                        "url": "http://localhost:11434/api/embeddings"
                    }
                }
            )
        )

        long_term_memory = LongTermMemory(
            storage=LTMSQLiteStorage(
                db_path="./memory/long_term_memory_storage.db"
            )
        )

        entity_memory = EntityMemory(
            storage=RAGStorage(
                type="entity",
                path="./memory",
                embedder_config={
                    "provider": "ollama",
                    "config": {
                        "model": "mxbai-embed-large",
                        "url": "http://localhost:11434/api/embeddings"
                    }
                }
            )
        )
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large",
                    "url": "http://localhost:11434/api/embeddings"
                }
            },
            short_term_memory=short_term_memory,
            long_term_memory=long_term_memory,
            entity_memory=entity_memory,
        )
