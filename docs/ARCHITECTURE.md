\# CHITTI — System Architecture



\## 1. Overview



CHITTI is a personal AI assistant for Windows, developed as a Nexora AI product. It supports text-based interaction through a desktop graphical interface and uses a modular Python backend.



\## 2. Architecture Principles



\- \*\*Modular design:\*\* Each module has a clearly defined responsibility.

\- \*\*Skill-based extensibility:\*\* Features are implemented as independent skills.

\- \*\*Centralized orchestration:\*\* A single orchestrator routes user requests.

\- \*\*Configuration management:\*\* Application settings are managed separately from source code.

\- \*\*Maintainability:\*\* Components are organized to support testing and future improvements.



\## 3. Main Components



| Component | Responsibility |

|---|---|

| `gui/` | Desktop user interface built with PySide6 |

| `core/` | Core application logic and orchestration |

| `skills/` | Individual assistant capabilities |

| `llm/` | Large language model integration |

| `memory/` | Memory-related functionality |

| `database/` | Data persistence |

| `voice/` | Voice-related functionality |

| `automation/` | Automation-related functionality |

| `services/` | Supporting application services |

| `configs/` | Application configuration |

| `scripts/` | Development and utility scripts |

| `tests/` | Automated tests |



\## 4. Request Flow



1\. The user submits a request through the desktop GUI.

2\. The core orchestrator receives the request.

3\. The skill registry helps identify a suitable skill.

4\. If a skill can handle the request, the orchestrator routes it to that skill.

5\. Requests that are not handled by a skill may be processed through the configured LLM integration.

6\. The result is returned to the user interface.



\## 5. Skills



Skills provide independent capabilities through a shared interface. A skill can define its name, supported triggers, request-handling logic, and execution behavior.



The skill registry manages available skills, while the orchestrator coordinates request routing.



\## 6. LLM Integration



CHITTI integrates with the Groq API for language-model responses. API credentials should be stored in environment variables and must never be committed to the public repository.



\## 7. Configuration and Logging



Application settings are managed separately from business logic. Logging supports troubleshooting and should avoid recording secrets or sensitive user information.



\## 8. Desktop Interface



The desktop interface uses PySide6 and separates the main window, navigation sidebar, header, chat area, and input controls into reusable components.



\## 9. Future Development



Potential future improvements include voice interaction, additional skills, enhanced memory, browser automation, computer automation, and improved packaging for Windows installation.



These are planned capabilities and should not be considered implemented unless verified in the codebase.



