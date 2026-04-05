# Copilot Instructions

<!--
  Deploy to: .github/copilot-instructions.md
  Stack: Java / Spring Boot
-->

## Project

[One sentence describing what this service does.]

## Stack

- Language: Java 21
- Framework: Spring Boot 3.x
- Build: Maven / Gradle
- ORM: Spring Data JPA / Hibernate
- Test: JUnit 5, Mockito, Spring Boot Test
- Database: [PostgreSQL / MySQL / H2]

## Conventions

- Use constructor injection, not field injection (`@Autowired` on fields is not allowed).
- Service layer holds business logic. Controllers handle HTTP only — no business logic in controllers.
- Repository layer uses Spring Data JPA interfaces. Write JPQL for complex queries, not native SQL.
- DTOs for request/response objects. Never expose JPA entities directly in API responses.
- Use `Optional` for nullable return values from repositories. Never return `null`.
- Exception handling via `@ControllerAdvice`. Do not catch and swallow exceptions in services.
- Logging via SLF4J (`LoggerFactory.getLogger`). No `System.out.println`.

## Naming

- Classes: `PascalCase`
- Methods and variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Packages: lowercase, e.g. `com.example.project.service`
- Test classes: `[ClassName]Test` for unit tests, `[ClassName]IT` for integration tests

## Testing

- Unit tests mock all dependencies with Mockito.
- Use `@SpringBootTest` only for integration tests — not for unit tests.
- Test method naming: `methodName_condition_expectedBehaviour` (e.g. `findUser_whenNotFound_throwsNotFoundException`).
- Assert with AssertJ (`assertThat`), not JUnit assertions.

## What not to do

- Do not use `@Transactional` on controller methods.
- Do not use `Optional.get()` without checking `isPresent()` first — use `orElseThrow`.
- Do not use Lombok `@Data` on JPA entities — use explicit getters/setters.
- Do not write business logic in `@Repository` classes.
