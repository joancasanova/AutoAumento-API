Documentation: Patterns Used in the Application
1. Dependency Injection

Pattern: Dependency Injection (DI)

Description: The application uses Dependency Injection to provide necessary services and ports to the use cases. This makes the code more modular and easier to test. For example, GenerateTextUseCase requires an LLMPort to interact with the language model.

Example:

class GenerateTextUseCase:
    def __init__(self, llm: LLMPort):
        self.llm = llm

2. Ports and Adapters

Pattern: Hexagonal Architecture (Ports and Adapters)

Description: The application separates concerns by defining ports (interfaces) that the domain layer depends on and adapters that implement these ports. This allows the core logic to remain independent of external systems.

Example:

    Port Definition:

class LLMPort:
    def generate(self, system_prompt: str, user_prompt: str, num_responses: int = 1, max_new_tokens: int = 100) -> List[str]:
        raise NotImplementedError

Adapter Implementation:

    class InstructModel(LLMPort):
        def generate(self, system_prompt: str, user_prompt: str, num_responses: int = 1, max_new_tokens: int = 100) -> List[str]:
            # Implementation details...
            pass

3. Use Case Driven Design

Pattern: Use Case Driven Design

Description: The application organizes its functionality around use cases. Each use case is responsible for a specific business operation, encapsulating the logic and interactions required to perform that operation.

Example:

    Generate Text Use Case:

class GenerateTextUseCase:
    def execute(self, system_prompt: str, user_prompt: str, num_return_sequences: int, max_new_tokens: int, num_executions: int, reference_data: List[Dict[str, str]]) -> List[GeneratedResult]:
        # Logic to generate text...
        pass

Manage Setups Use Case:

    class ManageSetupsUseCase:
        def load_setup(self, name: str) -> Optional[Dict[str, Any]]:
            # Logic to load a setup...
            pass

4. Entity-Relationship Model

Pattern: Entity-Relationship Model

Description: The application defines entities that represent the core concepts and data structures within the domain. These entities are used throughout the application to maintain consistency and clarity.

Example:

    Entities:

    class GeneratedResult:
        def __init__(self, response: str):
            self.response = response

    class ParseEntry:
        def __init__(self, data: Dict[str, Any]):
            self.data = data

5. Data Transfer Objects (DTOs)

Pattern: Data Transfer Objects

Description: The application uses DTOs to transfer data between different layers of the application, such as between the API and the use cases. This helps in decoupling the layers and ensuring that only the necessary data is transferred.

Example:

    DTOs for API Requests:

    class GenerationRequest(BaseModel):
        model: str
        system_prompt: str
        user_prompt: str
        num_return_sequences: int
        max_new_tokens: int
        num_executions: int
        reference_data: List[Dict[str, str]]

6. Error Handling

Pattern: Error Handling

Description: The application includes robust error handling mechanisms to manage exceptions and provide meaningful error messages. This ensures that the application can gracefully handle errors and provide useful feedback to the user.

Example:

    Error Handling in Use Cases:

    def execute(self, system_prompt: str, user_prompt: str, num_return_sequences: int, max_new_tokens: int, num_executions: int, reference_data: List[Dict[str, str]]) -> List[GeneratedResult]:
        if num_return_sequences <= 0 or max_new_tokens <= 0 or num_executions <= 0:
            raise ValueError("num_return_sequences, max_new_tokens and num_executions must be greater than 0")
        # Additional logic...

7. Configuration and Validation

Pattern: Configuration and Validation

Description: The application includes mechanisms for validating input data and configurations. This ensures that the application receives valid and expected data, reducing the risk of errors and inconsistencies.

Example:

    Validation in Use Cases:

    def validate_and_replace_placeholders(prompt: str, data: Dict[str, str]) -> str:
        placeholders = extract_placeholders(prompt)
        for ph in placeholders:
            if ph not in data:
                raise ValueError(f"Missing placeholder '{ph}' in reference data")
        # Additional logic...

8. Service Layer

Pattern: Service Layer

Description: The application includes a service layer that encapsulates complex business logic. This layer provides a higher-level abstraction over the domain entities and ports, making it easier to manage and test the business logic.

Example:

    Parse Service:

class ParseService:
    def parse_text(self, text: str, config: ParseConfiguration) -> List[Dict[str, str]]:
        # Logic to parse text based on configuration...
        pass

Verifier Service:

    class VerifierService:
        def verify_embedding_method(self, method: VerificationMethod, get_similarity, response: str) -> bool:
            # Logic to verify a response using embedding method...
            pass

9. Enum Types

Pattern: Enum Types

Description: The application uses enumeration types to define fixed sets of values for certain attributes. This ensures that only valid values are used, improving data integrity and reducing the risk of errors.

Example:

    Enums for Verification Method Types:

    class VerificationMethodType(Enum):
        EMBEDDING = "embedding"
        CONSENSUS = "consensus"

10. Regular Expressions

Pattern: Regular Expressions

Description: The application uses regular expressions to perform pattern matching and extraction operations on text. This is particularly useful for parsing and validating text data.

Example:

    Extracting Placeholders:

def extract_placeholders(text: str) -> List[str]:
    return re.findall(r"{([^{}]+)}", text)

Parsing Text:

    def _apply_rule_on_text_all(self, text: str, rule: ParseRule) -> List[str]:
        if rule.mode == ParseMode.REGEX:
            matches = re.findall(rule.pattern, text)
            return matches if isinstance(matches, list) else [matches]
        # Additional logic...

11. FastAPI for RESTful API

Pattern: FastAPI

Description: The application uses FastAPI to create a RESTful API. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

Example:

    API Router for Generation:

    router = APIRouter()

    @router.post("/", summary="Generar texto", description="Genera texto utilizando el modelo LLM especificado. Permite placeholders y datos de referencia para sustituir en los prompts.")
    def generate_text(req: GenerationRequest) -> Any:
        llm = get_llm(req.model)
        use_case = GenerateTextUseCase(llm)
        results = use_case.execute(
            system_prompt=req.system_prompt,
            user_prompt=req.user_prompt,
            num_return_sequences=req.num_return_sequences,
            max_new_tokens=req.max_new_tokens,
            num_executions=req.num_executions,
            reference_data=req.reference_data
        )
        return {"results": [{"response": r.response} for r in results]}

12. Modular Design

Pattern: Modular Design

Description: The application is organized into modules and packages, each responsible for a specific aspect of the application. This modularity improves maintainability, readability, and scalability.

Example:

    Modules:
        application/use_cases: Contains use cases.
        domain/entities: Defines domain entities.
        domain/ports: Defines ports (interfaces).
        domain/services: Contains domain services.
        infrastructure/adapters: Contains adapters for ports.
        infrastructure/repositories: Contains repository implementations.
        interfaces/api/routes: Contains API routes.

13. Configuration Management

Pattern: Configuration Management

Description: The application manages configurations through various means, such as default values and external configuration files. This allows for flexibility and ease of deployment.

Example:

    Default Values in DTOs:

class GenerationRequest(BaseModel):
    model: str = Field(default="EleutherAI/gpt-neo-125M", description="Nombre del modelo a utilizar, publicado en HuggingFace.")
    # Additional fields...

Configuration in Adapters:

    def get_llm(model_name: str = "EleutherAI/gpt-neo-125M") -> LLMPort:
        return InstructModel(model_name)

14. Logging and Monitoring

Pattern: Logging and Monitoring

Description: Although not explicitly shown in the provided code, the application likely includes logging and monitoring mechanisms to track its behavior and performance. This is crucial for maintaining and debugging the application.

Example:

    Logging in Use Cases:

    import logging

    logger = logging.getLogger(__name__)

    def execute(self, system_prompt: str, user_prompt: str, num_return_sequences: int, max_new_tokens: int, num_executions: int, reference_data: List[Dict[str, str]]) -> List[GeneratedResult]:
        try:
            # Logic to generate text...
            pass
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise RuntimeError(f"Error generating text: {str(e)}")

Conclusion

The application effectively uses a variety of design patterns to achieve a modular, maintainable, and scalable architecture. By leveraging patterns such as Dependency Injection, Ports and Adapters, Use Case Driven Design, and others, the application is well-structured and easy to understand. This approach also enhances the testability and flexibility of the code, making it easier to adapt to changing requirements.