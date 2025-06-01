import logging  # 로깅을 위한 표준 라이브러리
from server.task_manager import InMemoryTaskManager  # 기본 메모리 기반 TaskManager
from models.request import SendTaskRequest, SendTaskResponse  # 요청 및 응답 모델
from models.task import Message, TextPart, TaskStatus, TaskState  # 작업 관련 모델

# 로깅 설정
logger = logging.getLogger(__name__)

class AgentTaskManager(InMemoryTaskManager):
    """
    RestaurantMenuAgent와 Task 시스템을 연결하는 클래스.
    - InMemoryTaskManager를 상속받아 기본 기능을 확장.
    """

    def __init__(self, agent):
        """
        AgentTaskManager 초기화 메서드.
        - RestaurantMenuAgent를 인스턴스 변수로 저장.

        Args:
            agent: RestaurantMenuAgent 인스턴스.
        """
        super().__init__()  # 부모 클래스의 초기화 메서드 호출
        self.agent = agent  # RestaurantMenuAgent 인스턴스 저장

    def _get_user_query(self, request: SendTaskRequest) -> str:
        """
        사용자의 요청에서 텍스트를 추출.

        Args:
            request (SendTaskRequest): 사용자 요청 객체.

        Returns:
            str: 사용자의 요청 텍스트.
        """
        return request.params.message.parts[0].text  # 요청 메시지에서 텍스트 추출

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        """
        새로운 작업을 처리하고 완료 상태로 업데이트.

        Args:
            request (SendTaskRequest): 사용자 요청 객체.

        Returns:
            SendTaskResponse: 작업 처리 결과.
        """
        logger.info(f"Processing new task: {request.params.id}")  # 작업 ID 로깅

        # 작업을 메모리에 저장하거나 업데이트
        task = await self.upsert_task(request.params)

        # 사용자의 요청 텍스트 추출
        query = self._get_user_query(request)

        # RestaurantMenuAgent를 호출하여 응답 생성
        result_text = self.agent.invoke(query, request.params.sessionId)

        # 에이전트의 응답을 Message 객체로 변환
        agent_message = Message(
            role="agent",  # 역할은 "agent"
            parts=[TextPart(text=result_text)]  # 응답 텍스트를 TextPart로 저장
        )

        # 작업 상태를 완료로 업데이트하고 응답 추가
        async with self.lock:  # 동시성 문제를 방지하기 위해 락 사용
            task.status = TaskStatus(state=TaskState.COMPLETED)  # 작업 상태를 완료로 설정
            task.history.append(agent_message)  # 작업 기록에 에이전트 메시지 추가

        # 작업 결과를 포함한 응답 반환
        return SendTaskResponse(id=request.id, result=task)