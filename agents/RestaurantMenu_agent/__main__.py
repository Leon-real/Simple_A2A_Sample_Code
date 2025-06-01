from server.server import A2AServer  # A2A 서버 클래스
from models.agent import AgentCard, AgentCapabilities, AgentSkill  # 에이전트 메타데이터 모델
from agents.RestaurantMenu_agent.task_manager import AgentTaskManager  # TaskManager 클래스
from agents.RestaurantMenu_agent.agent import RestaurantMenuAgent  # RestaurantMenuAgent 클래스
import click  # CLI 옵션 처리를 위한 라이브러리
import logging  # 로깅을 위한 표준 라이브러리

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")  # 호스트 옵션
@click.option("--port", default=10003, help="Port number for the server")  # 포트 옵션
def main(host, port):
    """
    에이전트 서버를 설정하고 시작.
    """
    # 에이전트의 기능 정의 (스트리밍 미지원)
    capabilities = AgentCapabilities(streaming=False)

    # 에이전트의 스킬 정의
    skill = AgentSkill(
        id="store_agent",  # 스킬 ID
        name="Restaurant Menu Assistant",  # 스킬 이름
        description="Provides information about the restaurant menu.",  # 스킬 설명
        tags=["menu", "restaurant"],  # 태그
        examples=["What burgers do you have?", "Tell me about your drinks."]  # 예제
    )

    # 에이전트 메타데이터 정의
    agent_card = AgentCard(
        name="RestaurantMenuAgent",  # 에이전트 이름
        description="This agent provides information about the restaurant menu.",  # 설명
        url=f"http://{host}:{port}/",  # 에이전트 URL
        version="1.0.0",  # 버전
        defaultInputModes=RestaurantMenuAgent.SUPPORTED_CONTENT_TYPES,  # 지원 입력 타입
        defaultOutputModes=RestaurantMenuAgent.SUPPORTED_CONTENT_TYPES,  # 지원 출력 타입
        capabilities=capabilities,  # 에이전트 기능
        skills=[skill]  # 에이전트 스킬
    )

    # A2A 서버 초기화
    server = A2AServer(
        host=host,  # 서버 호스트
        port=port,  # 서버 포트
        agent_card=agent_card,  # 에이전트 메타데이터
        task_manager=AgentTaskManager(agent=RestaurantMenuAgent())  # TaskManager와 RestaurantMenuAgent 연결
    )

    # 서버 시작
    server.start()

# 스크립트가 직접 실행될 때만 main 함수 호출
if __name__ == "__main__":
    main()