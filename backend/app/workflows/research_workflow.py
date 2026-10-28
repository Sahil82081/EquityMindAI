import logging
from langgraph.graph import StateGraph, START, END
from app.schemas.state import ResearchState
from app.agents import (
    data_agent,
    news_agent,
    valuation_agent,
    bull_agent,
    bear_agent,
    judge_agent,
    verification_agent,
)

logger = logging.getLogger("equitymind.workflow")


def data_agent_node(state: ResearchState) -> dict:
    """Data Agent Node: Retrieves verified financial data for the company."""
    company = state["company"]

    logger.info(f"▶ [LangGraph Node: Data Agent] Executing for {company.name} ({company.ticker})")

    try:
        financial_data = data_agent.run(company)
        logger.info(
            f"✓ [LangGraph Node: Data Agent] Success for {company.ticker}: "
            f"Price={financial_data.quote.formatted_price}, Live={financial_data.is_live}"
        )
        return {
            "financial_data": financial_data,
            "agent_status": {"data": "completed"},
        }
    except Exception as e:
        err_msg = f"Data Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: Data Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"data": "failed"},
            "errors": [err_msg],
        }


def news_agent_node(state: ResearchState) -> dict:
    """News Agent Node: Collects authentic news and summarizes market coverage using Gemini."""
    company = state["company"]

    logger.info(f"▶ [LangGraph Node: News Agent] Executing for {company.name} ({company.ticker})")

    try:
        news_result = news_agent.run(company)
        logger.info(
            f"✓ [LangGraph Node: News Agent] Success for {company.ticker}: "
            f"{news_result.total_articles} authentic articles retrieved, tone='{news_result.overall_sentiment}'"
        )
        return {
            "news": news_result,
            "agent_status": {"news": "completed"},
        }
    except Exception as e:
        err_msg = f"News Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: News Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"news": "failed"},
            "errors": [err_msg],
        }


def valuation_agent_node(state: ResearchState) -> dict:
    """Valuation Agent Node: Computes mathematical multiples in code and reasons using Gemini."""
    company = state["company"]
    financial_data = state.get("financial_data")

    logger.info(f"▶ [LangGraph Node: Valuation Agent] Executing for {company.name} ({company.ticker})")

    try:
        if financial_data is None:
            # Fallback to run data agent if not populated
            financial_data = data_agent.run(company)

        valuation_result = valuation_agent.run(company, financial_data)
        logger.info(
            f"✓ [LangGraph Node: Valuation Agent] Success for {company.ticker}: "
            f"P/E={valuation_result.pe_ratio.formatted_value}, Score={valuation_result.valuation_score}/100, "
            f"Classification='{valuation_result.valuation_classification}'"
        )
        return {
            "valuation": valuation_result,
            "agent_status": {"valuation": "completed"},
        }
    except Exception as e:
        err_msg = f"Valuation Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: Valuation Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"valuation": "failed"},
            "errors": [err_msg],
        }


def bull_agent_node(state: ResearchState) -> dict:
    """Bull Agent Node: Builds the strongest evidence-backed bullish case using existing research state."""
    company = state["company"]
    financial_data = state.get("financial_data")
    valuation = state.get("valuation")
    news = state.get("news")

    logger.info(f"▶ [LangGraph Node: Bull Agent] Executing for {company.name} ({company.ticker})")

    try:
        bull_case = bull_agent.run(
            company=company,
            financial_data=financial_data,
            valuation=valuation,
            news=news,
        )
        logger.info(
            f"✓ [LangGraph Node: Bull Agent] Success for {company.ticker}: "
            f"Confidence={bull_case.confidence}%, {len(bull_case.arguments)} arguments"
        )
        return {
            "bull_case": bull_case,
            "agent_status": {"bull": "completed"},
        }
    except Exception as e:
        err_msg = f"Bull Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: Bull Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"bull": "failed"},
            "errors": [err_msg],
        }


def bear_agent_node(state: ResearchState) -> dict:
    """Bear Agent Node: Builds the strongest evidence-backed bearish case actively challenging the Bull thesis."""
    company = state["company"]
    financial_data = state.get("financial_data")
    valuation = state.get("valuation")
    news = state.get("news")
    bull_case = state.get("bull_case")

    logger.info(f"▶ [LangGraph Node: Bear Agent] Executing for {company.name} ({company.ticker})")

    try:
        bear_case = bear_agent.run(
            company=company,
            financial_data=financial_data,
            valuation=valuation,
            news=news,
            bull_case=bull_case,
        )
        logger.info(
            f"✓ [LangGraph Node: Bear Agent] Success for {company.ticker}: "
            f"Confidence={bear_case.confidence}%, {len(bear_case.arguments)} arguments"
        )
        return {
            "bear_case": bear_case,
            "agent_status": {"bear": "completed"},
        }
    except Exception as e:
        err_msg = f"Bear Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: Bear Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"bear": "failed"},
            "errors": [err_msg],
        }


def judge_agent_node(state: ResearchState) -> dict:
    """Judge Agent Node: Objectively compares Bull and Bear arguments and produces a balanced conclusion."""
    company = state["company"]
    financial_data = state.get("financial_data")
    valuation = state.get("valuation")
    news = state.get("news")
    bull_case = state.get("bull_case")
    bear_case = state.get("bear_case")

    logger.info(f"▶ [LangGraph Node: Judge Agent] Executing for {company.name} ({company.ticker})")

    try:
        if not bull_case:
            logger.info("Judge Agent generating Bull case fallback...")
            bull_case = bull_agent.run(
                company=company,
                financial_data=financial_data,
                valuation=valuation,
                news=news,
            )
        if not bear_case:
            logger.info("Judge Agent generating Bear case fallback...")
            bear_case = bear_agent.run(
                company=company,
                financial_data=financial_data,
                valuation=valuation,
                news=news,
                bull_case=bull_case,
            )

        debate_result = judge_agent.run(
            company=company,
            bull=bull_case,
            bear=bear_case,
            financial_data=financial_data,
            valuation=valuation,
        )
        logger.info(
            f"✓ [LangGraph Node: Judge Agent] Success for {company.ticker}: "
            f"Adjudication complete, balanced conclusion synthesized"
        )
        return {
            "debate": debate_result,
            "agent_status": {"judge": "completed"},
        }
    except Exception as e:
        err_msg = f"Judge Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: Judge Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"judge": "failed"},
            "errors": [err_msg],
        }


def verification_agent_node(state: ResearchState) -> dict:
    """Verification Agent Node: Audits important claims against source data and Python calculations."""
    company = state["company"]
    financial_data = state.get("financial_data")
    valuation = state.get("valuation")
    news = state.get("news")
    debate = state.get("debate")

    logger.info(f"▶ [LangGraph Node: Verification Agent] Executing for {company.name} ({company.ticker})")

    try:
        claims = verification_agent.run(
            company=company,
            financial_data=financial_data,
            valuation=valuation,
            news=news,
            debate=debate,
        )
        logger.info(
            f"✓ [LangGraph Node: Verification Agent] Success for {company.ticker}: "
            f"{len(claims)} empirical claims audited against ground truth"
        )
        return {
            "claims": claims,
            "agent_status": {"verification": "completed"},
        }
    except Exception as e:
        err_msg = f"Verification Agent error: {str(e)}"
        logger.error(f"✗ [LangGraph Node: Verification Agent] Failed for {company.ticker}: {err_msg}")
        return {
            "agent_status": {"verification": "failed"},
            "errors": [err_msg],
        }


def build_research_graph():
    """Build and compile the complete LangGraph research, debate, and verification workflow.

    Workflow topology:
    Company -> Data Agent -> News Agent -> Valuation Agent (Research State)
                   ↓
         ┌───────────────────┐
         ↓                   ↓
     Bull Agent          Bear Agent
         ↓                   ↓
         └─────────┬─────────┘
                   ↓
              Judge Agent
                   ↓
           Verification Agent (Claim -> Evidence Verification)
                   ↓
            Final Assessment (END)
    """
    workflow = StateGraph(ResearchState)

    # 1. Add agent nodes with distinct responsibilities
    workflow.add_node("data_agent", data_agent_node)
    workflow.add_node("news_agent", news_agent_node)
    workflow.add_node("valuation_agent", valuation_agent_node)
    workflow.add_node("bull_agent", bull_agent_node)
    workflow.add_node("bear_agent", bear_agent_node)
    workflow.add_node("judge_agent", judge_agent_node)
    workflow.add_node("verification_agent", verification_agent_node)

    # 2. Sequential pipeline up to Research State
    workflow.add_edge(START, "data_agent")
    workflow.add_edge("data_agent", "news_agent")
    workflow.add_edge("news_agent", "valuation_agent")

    # 3. Parallel fan-out from Research State to Bull & Bear Agents
    workflow.add_edge("valuation_agent", "bull_agent")
    workflow.add_edge("valuation_agent", "bear_agent")

    # 4. Fan-in from Bull & Bear Agents to Judge Agent
    workflow.add_edge("bull_agent", "judge_agent")
    workflow.add_edge("bear_agent", "judge_agent")

    # 5. Judge Agent to Verification Agent (Claim -> Evidence Verification)
    workflow.add_edge("judge_agent", "verification_agent")

    # 6. Verification Agent to Final Assessment
    workflow.add_edge("verification_agent", END)

    # 7. Compile the graph
    app = workflow.compile()
    logger.info("LangGraph Bull vs Bear & Verification Workflow compiled successfully.")
    return app


# Singleton compiled graph instance
research_graph = build_research_graph()
