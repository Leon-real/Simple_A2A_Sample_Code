from autogen_agentchat.agents import AssistantAgent  # Autogen의 AssistantAgent 임포트
from autogen_ext.models.openai import OpenAIChatCompletionClient  # OpenAI 클라이언트 임포트
from autogen_agentchat.messages import TextMessage  # 텍스트 메시지 객체 임포트
from autogen_core import CancellationToken  # 취소 토큰 임포트
from dotenv import load_dotenv  # 환경 변수 로드를 위한 dotenv
import os  # 운영체제 관련 기능
import asyncio  # 비동기 처리


# .env 파일에서 환경 변수 로드
load_dotenv()


class RestaurantMenuAgent:
    # 지원하는 콘텐츠 타입 정의
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        """
        RestaurantMenuAgent 초기화 함수
        - 환경 변수 검증
        - OpenAI 클라이언트 설정
        - 메뉴 데이터 초기화
        - Autogen AssistantAgent 설정
        """
        # OPENAI_API_KEY 환경 변수 확인
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        
        # OpenAI 채팅 완성 클라이언트 초기화
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o",  # 사용할 모델 지정
            api_key=os.getenv("OPENAI_API_KEY")  # API 키 주입
        )
        
        # 하드코딩된 메뉴 데이터
        self.menu = {
            "burger": "치즈버거, 치킨버거, 베지버거",
            "pizza": "마르게리타, 페퍼로니, 바비큐 치킨",
            "drinks": "콜라, 레모네이드, 아이스티",
        }

        # Autogen AssistantAgent 초기화
        self.agent = AssistantAgent(
            name="RestaurantMenuAgent",  # 에이전트 이름
            system_message=(
                "당신은 레스토랑 도우미입니다. "
                "메뉴 정보를 제공해주세요. "
                "메뉴 카테고리: 'burger', 'pizza', 'drinks'."
            ),  # 시스템 역할 정의
            model_client=self.model_client  # 모델 클라이언트 연결
        )

    def invoke(self, query: str, session_id: str) -> str:
        """
        사용자 쿼리 처리 메인 메서드
        - 비동기 처리 루프 관리
        - Autogen 에이전트 호출

        Args:
            query (str): 사용자 질문
            session_id (str): 세션 ID

        Returns:
            str: 에이전트 응답
        """
        # 프롬프트 구성: 사용자 질문 + 메뉴 데이터
        prompt = f"사용자 질문: '{query}'. 메뉴: {self.menu}"

        async def ask():
            """비동기 응답 생성 함수"""
            # Autogen 에이전트에 메시지 전송
            response = await self.agent.on_messages(
                messages=[TextMessage(content=prompt, source="user")],  # 텍스트 메시지 객체 생성
                cancellation_token=CancellationToken()  # 취소 토큰 필수
            )
            return response.chat_message.content  # 응답 텍스트 추출

        try:
            # 현재 실행 중인 이벤트 루프 확인
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # 루프가 없는 경우 새로 실행
            return asyncio.run(ask())
        else:
            # 기존 루프 사용 시(nest_asyncio 적용 필요)
            import nest_asyncio
            nest_asyncio.apply()  # 중첩 이벤트 루프 허용
            return loop.run_until_complete(ask())

    async def stream(self, query: str, session_id: str):
        """
        스트리밍 미지원 처리 메서드
        (현재 Autogen에서 스트리밍 기능을 공식 지원하지 않음)
        """
        raise NotImplementedError("AutoGen은 현재 스트리밍을 지원하지 않습니다.")
