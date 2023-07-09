from typing import List
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
)
from .prompts import interviewer_inception_prompt, interviewee_inception_prompt


class CAMELAgent:
    def __init__(
        self,
        system_message: SystemMessage,
        model: ChatOpenAI,
    ) -> None:
        self._init_system_message = system_message
        self._system_messages = [self._init_system_message]
        self._chat_messages = []
        self._model = model
        self.init_messages()

    def reset(self) -> None:
        self.init_messages()
        return self.build_complete_message_list()

    def init_messages(self) -> None:
        self._system_messages = [self._init_system_message]
        self._chat_messages = []

    def add_chat_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self._chat_messages.append(message)
        return self._chat_messages

    def build_complete_message_list(self):
        return self._system_messages + self._chat_messages

    def add_directives(self, message: str, replace=False) -> None:
        director_msg = SystemMessage(content=message)
        self.add_chat_messages(director_msg)

    def get_directives(self) -> str:
        pass

    def step(
        self,
        input_message: HumanMessage,
    ) -> AIMessage:
        messages = []
        if input_message != "":
            self.add_chat_messages(input_message)
        messages = self.build_complete_message_list()
        output_message = self._model(messages)
        self.add_chat_messages(output_message)

        return output_message


def get_sys_msgs(interviewer_role_name: str, interviewee_role_name: str):
    interviewer_sys_template = SystemMessagePromptTemplate.from_template(
        template=interviewer_inception_prompt
    )
    interviewer_sys_msg = interviewer_sys_template.format_messages(
        interviewer_role_name=interviewer_role_name,
        interviewee_role_name=interviewee_role_name,
    )[0]

    interviewee_sys_template = SystemMessagePromptTemplate.from_template(
        template=interviewee_inception_prompt
    )
    interviewee_sys_msg = interviewee_sys_template.format_messages(
        interviewer_role_name=interviewer_role_name,
        interviewee_role_name=interviewee_role_name,
    )[0]

    return interviewer_sys_msg, interviewee_sys_msg

