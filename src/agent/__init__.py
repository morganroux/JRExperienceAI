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
    HumanMessagePromptTemplate,
)
from .prompts import interviewer_inception_prompt, interviewee_inception_prompt


class CAMELAgent:
    def __init__(
        self,
        system_message: SystemMessage,
        model: ChatOpenAI,
    ) -> None:
        self.system_message = system_message
        self.model = model
        self.init_messages()

    def reset(self) -> None:
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        return self.stored_messages

    def get_messages(self):
        return self.stored_messages

    def set_directives(self, message: str, replace=False) -> None:
        pass

    def get_directives(self) -> str:
        pass

    def step(
        self,
        input_message: HumanMessage,
    ) -> AIMessage:
        messages = []
        if input_message != "":
            messages = self.update_messages(input_message)
        else:
            messages = self.get_messages()
        output_message = self.model(messages)
        self.update_messages(output_message)

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

