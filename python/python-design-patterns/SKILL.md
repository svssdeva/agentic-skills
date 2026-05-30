<!-- Source: https://www.skills.sh/wshobson/agents/python-design-patterns -->
<!-- Install: npx skills add https://github.com/wshobson/agents --skill python-design-patterns -->
---
name: python-design-patterns
description: Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance. Use this skill when designing a new service or component from scratch and choosing how to layer responsibilities, when refactoring a God class or monolithic function that has grown too large, when deciding whether to add a new abstraction or live with duplication, when evaluating a pull request for structural issues like tight coupling or leaking internal types, when choosing between inheritance and composition for a new class hierarchy, or when a codebase is becoming hard to test because of entangled I/O and business logic.
---

# Python Design Patterns

Write maintainable Python code using fundamental design principles. These patterns help you build systems that are easy to understand, test, and modify.

## When to Use This Skill

- Designing new components or services
- Refactoring complex or tangled code
- Deciding whether to create an abstraction
- Choosing between inheritance and composition
- Evaluating code complexity and coupling
- Planning modular architectures

## Core Concepts

1. **KISS** — Choose the simplest solution that works. Complexity must be justified.
2. **Single Responsibility (SRP)** — Each unit should have one reason to change.
3. **Composition Over Inheritance** — Build behavior by combining objects, not extending classes.
4. **Rule of Three** — Wait until you have three instances before abstracting.

## Pattern 1: KISS — Keep It Simple

```python
# Over-engineered: factory with registration
class OutputFormatterFactory:
    _formatters: dict[str, type[Formatter]] = {}
    @classmethod
    def register(cls, name): ...
    @classmethod
    def create(cls, name): ...

# Simple: just use a dictionary
FORMATTERS = {"json": JsonFormatter, "csv": CsvFormatter, "xml": XmlFormatter}

def get_formatter(name: str) -> Formatter:
    if name not in FORMATTERS:
        raise ValueError(f"Unknown format: {name}")
    return FORMATTERS[name]()
```

## Pattern 2: Single Responsibility Principle

```python
# BAD: handler does everything
class UserHandler:
    async def create_user(self, request):
        data = await request.json()          # HTTP parsing
        if not data.get("email"):            # Validation
            return Response({"error": "email required"}, status=400)
        user = await db.execute("INSERT ...", data["email"], data["name"])  # DB
        return Response({"id": user.id}, status=201)  # Formatting

# GOOD: separated concerns
class UserService:
    """Business logic only."""
    async def create_user(self, data: CreateUserInput) -> User:
        return await self._repo.save(User(email=data.email, name=data.name))

class UserHandler:
    """HTTP concerns only."""
    async def create_user(self, request: Request) -> Response:
        data = CreateUserInput(**(await request.json()))
        user = await self._service.create_user(data)
        return Response(user.to_dict(), status=201)
```

## Pattern 3: Separation of Concerns

```
┌──────────────────────────────────┐
│  API Layer (handlers)             │
│  Parse requests, format responses │
└────────────────┬─────────────────┘
                 ▼
┌──────────────────────────────────┐
│  Service Layer (business logic)   │
│  Domain rules, orchestrate ops    │
└────────────────┬─────────────────┘
                 ▼
┌──────────────────────────────────┐
│  Repository Layer (data access)   │
│  SQL, external APIs, cache        │
└──────────────────────────────────┘
```

Each layer depends only on layers below it. Never import upward.

## Pattern 4: Composition Over Inheritance

```python
# Inheritance: rigid, hard to test
class EmailNotificationService(NotificationService):
    def __init__(self):
        super().__init__()
        self._smtp = SmtpClient()  # Hard to mock

# Composition: flexible, testable
class NotificationService:
    def __init__(
        self,
        email_sender: EmailSender,
        sms_sender: SmsSender | None = None,
    ) -> None:
        self._email = email_sender
        self._sms = sms_sender

    async def notify(self, user: User, message: str, channels: set[str] | None = None) -> None:
        channels = channels or {"email"}
        if "email" in channels:
            await self._email.send(user.email, message)
        if "sms" in channels and self._sms and user.phone:
            await self._sms.send(user.phone, message)

# Easy to test with fakes
service = NotificationService(email_sender=FakeEmailSender(), sms_sender=FakeSmsSender())
```

## Pattern 5: Rule of Three

Wait until you have three instances before abstracting. Duplication is often better than the wrong abstraction.

```python
# Two similar functions — don't abstract yet
def process_orders(orders): ...
def process_returns(returns): ...
# They look similar but have different validation, processing, errors...
# Wait for a third. Even then, explicit is often better than abstract.
```

## Pattern 6: Function Size

Keep functions focused. Extract when a function:
- Exceeds ~20-50 lines (varies by complexity)
- Serves multiple distinct purposes
- Has deeply nested logic (3+ levels)

```python
# Too long, multiple concerns
def process_order(order):
    # 50 lines validation, 30 lines inventory, 40 lines payment, 20 lines notification

# Better: composed from focused functions
def process_order(order: Order) -> Result:
    validate_order(order)
    reserve_inventory(order)
    payment_result = charge_payment(order)
    send_confirmation(order, payment_result)
    return Result(success=True, order_id=order.id)
```

## Pattern 7: Dependency Injection

```python
from typing import Protocol

class Cache(Protocol):
    async def get(self, key: str) -> str | None: ...
    async def set(self, key: str, value: str, ttl: int) -> None: ...

class UserService:
    def __init__(self, repository: UserRepository, cache: Cache, logger: Logger) -> None:
        self._repo = repository
        self._cache = cache
        self._logger = logger

# Production
service = UserService(PostgresUserRepository(db), RedisCache(redis), StructlogLogger())

# Testing
service = UserService(InMemoryUserRepository(), FakeCache(), NullLogger())
```

## Pattern 8: Avoiding Anti-Patterns

**Don't expose internal types:**
```python
# BAD: leaking ORM model to API
@app.get("/users/{id}")
def get_user(id: str) -> UserModel:  # SQLAlchemy model — leaks internals
    return db.query(UserModel).get(id)

# GOOD
@app.get("/users/{id}")
def get_user(id: str) -> UserResponse:
    return UserResponse.from_orm(db.query(UserModel).get(id))
```

**Don't mix I/O with business logic:**
```python
# BAD
def calculate_discount(user_id: str) -> float:
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)  # I/O in logic!

# GOOD — pure function, easily testable
def calculate_discount(user: User, order_history: list[Order]) -> float:
    return 0.15 if len(order_history) > 10 else 0.0
```

## Best Practices Summary

1. Keep it simple — choose the simplest solution that works
2. Single responsibility — one reason to change
3. Separate concerns — distinct layers with clear purposes
4. Compose, don't inherit — combine objects for flexibility
5. Rule of three — wait before abstracting
6. Keep functions small — one purpose, ~20-50 lines
7. Inject dependencies — constructor injection for testability
8. Delete before abstracting — remove dead code, then consider patterns
9. Test each layer — isolated tests for each concern
10. Explicit over clever — readable beats elegant

## Troubleshooting

**A class is growing and seems to have multiple responsibilities, but splitting it feels wrong.**
Apply the "reason to change" test: list every change that could require editing this class. If the list has items from different domains (e.g., HTTP parsing AND business rules AND formatting), split it. If all changes stem from the same domain concern, the class may be appropriately sized.

**Injecting all dependencies through the constructor is producing constructors with 7+ parameters.**
This is a sign of too many responsibilities in one class, not a problem with dependency injection. Split the class into smaller units first, then each constructor naturally becomes smaller.

**Composition is producing deeply nested wrapper objects that are hard to trace.**
Keep the composition shallow (2-3 levels). If wrapping is the only mechanism, consider whether a Protocol-based approach or simple function composition would be cleaner than a chain of decorator objects.

**The rule of three says not to abstract yet, but the duplication is causing bugs when one copy is updated but not the other.**
Duplication that diverges in dangerous ways should be abstracted sooner. The rule of three is a heuristic, not a law. If the copies are already diverging incorrectly, extract immediately and add a test that exercises the shared behavior.

**A service layer is importing from the API layer, breaking the dependency direction.**
This is a layering violation. The service layer must not import from handlers. Introduce a shared types/models layer that both can import from, keeping the dependency arrow pointing downward (API → Service → Repository).

## Related Skills

- python-testing-patterns — Test each layer in isolation using the dependency injection structure established here
- python-project-setup — Set up project structure and tooling that enforces layer boundaries from the start
