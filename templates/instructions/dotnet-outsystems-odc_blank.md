# Copilot Instructions

<!--
  Deploy to: .github/copilot-instructions.md
  Stack: C# / .NET — OutSystems ODC External Libraries
-->

## Project

[One sentence describing what this ODC External Library does.]

## Stack

- Language: C# / .NET 8
- SDK: `OutSystems.ExternalLibraries.SDK` (NuGet)
- Target: OutSystems Developer Cloud (ODC)
- Test: xUnit, Moq

## ODC External Library model

ODC extensions are **External Libraries** — not Integration Studio extensions. The model is attribute-based:

- Define a `public interface` decorated with `[OSInterface]` — this is what ODC Studio sees.
- Implement the interface in a `public class`.
- Expose actions with `[OSAction]` on interface methods.
- Expose input/output parameters with `[OSParameter]` on method parameters.
- Expose structures with `[OSStructure]` on classes.
- Deploy as a `.zip` of the compiled library to the ODC Portal.

```csharp
using OutSystems.ExternalLibraries.SDK;

[OSInterface(Description = "...")]
public interface IMyLibrary
{
    [OSAction(Description = "...")]
    string GetUserById(
        [OSParameter(Description = "User identifier")] string userId);
}

public class MyLibrary : IMyLibrary
{
    public string GetUserById(string userId)
    {
        // implementation
    }
}
```

## Project structure

```text
<LibraryName>/
├── <LibraryName>.csproj
├── I<LibraryName>.cs       ← OSInterface definition
├── <LibraryName>.cs        ← implementation
├── Models/                 ← OSStructure classes
│   └── *.cs
└── Tests/
    └── <LibraryName>Tests.cs
```

## Naming conventions

- Interface: `I<LibraryName>` with `[OSInterface]`.
- Implementation class: `<LibraryName>` (no prefix).
- Actions (interface methods): `PascalCase` verbs (e.g. `GetUserById`, `SendNotification`).
- Parameters: `camelCase` — ODC Studio displays them as-is.
- Structure classes: `PascalCase` nouns (e.g. `UserRecord`, `NotificationPayload`).
- Do not use `ss`/`Mss`/`Css` prefixes — those are O11 Integration Studio conventions and do not apply to ODC.

## Type mapping (ODC → C#)

| ODC type | C# type |
| --- | --- |
| Text | `string` |
| Integer | `int` |
| Long Integer | `long` |
| Decimal | `decimal` |
| Boolean | `bool` |
| Date Time | `DateTime` |
| Binary Data | `byte[]` |
| Structure | Class decorated with `[OSStructure]` |
| Structure List | `List<T>` where T is an `[OSStructure]` class |

## Async

ODC External Libraries support `async` — use it for I/O-bound operations:

```csharp
[OSAction(Description = "Fetches data from an external API")]
Task<string> FetchDataAsync(
    [OSParameter] string endpoint,
    CancellationToken cancellationToken = default);
```

## Error handling

Throw standard .NET exceptions — ODC surfaces the message to the flow.

```csharp
if (string.IsNullOrEmpty(userId))
    throw new ArgumentException("userId cannot be empty.", nameof(userId));
```

For expected business errors, prefer descriptive exception messages over custom exception types — ODC flows handle them via Exception Handlers.

## What not to do

- Do not use `[OSInterface]` on a class — it must be on an `interface`.
- Do not use O11 naming (`ss`, `Mss`, `Css`, `RC`, `RL`) — not applicable in ODC.
- Do not reference `OutSystems.HubEdition.RuntimePlatform` — that is the O11 assembly.
- Do not use `static` mutable state — External Libraries are instantiated per request in ODC.
- Do not hand-generate the `.zip` package manually — use `dotnet publish` and follow the ODC packaging guide.
