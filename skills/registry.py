import logging
from skills.base import BaseSkill

logger = logging.getLogger(__name__)

class SkillRegistry:

    def __init__(self):
        self._skills: list[BaseSkill] = []

    def register(self, skill: BaseSkill) -> None:
        self._skills.append(skill)
        logger.info("Skill registered: %s", skill.name)

    def find(self, text: str) -> BaseSkill | None:
        for skill in self._skills:
            if skill.can_handle(text):
                logger.info("Skill matched: %s", skill.name)
                return skill
        return None

    def list_skills(self) -> list[str]:
        return [skill.name for skill in self._skills]