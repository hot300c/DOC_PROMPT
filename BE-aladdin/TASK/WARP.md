# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Aladdin is an ASP.NET Core REST API service that acts as a backend for the Genie frontend application. It provides a modern replacement for SQL Server stored procedures by implementing business logic as C# handlers, offering better maintainability, testability, and performance.

**Architecture Flow:**
```
Genie (Frontend) → JSON → Aladdin (API) → SQL → SQL Server → DataSet → JSON → Genie
```

**Key Technologies:**
- ASP.NET Core 8.0 
- LINQ to DB for database operations
- xUnit.net for testing
- Docker for containerization

## Common Development Commands

### Building and Running

```powershell
# Build the entire solution
dotnet build

# Run the main web service
dotnet run --project WebService

# Run with specific configuration
dotnet run --project WebService --environment Development
```

### Testing

```powershell
# Run all tests
dotnet test

# Run specific test project
dotnet test WebService.Handlers.Tests
dotnet test Services.Tests  
dotnet test Utilities.Tests

# Run tests for a specific handler (example)
dotnet test --filter "ws_API_ThongTinBienLaiShop"

# Run tests with verbose output for debugging
dotnet test --logger "console;verbosity=detailed"
```

### Docker Operations

```powershell
# Build Docker image
docker build -t aladdin:latest --target runtime .

# Run with Docker Compose (includes database)
docker-compose up -d

# Run standalone container
docker run -p 8080:8080 -e ASPNETCORE_ENVIRONMENT=Development -e "ConnectionStrings__Default=Data Source=localhost,1433;User ID=username;Password=password;Trust Server Certificate=True" aladdin:latest
```

### Database Setup for Testing

```powershell
# Start test database container
docker run --rm -p 1433:1433 registry.vnvc.info/vnvc-qas/qas-db-dev:0.4-nodata

# Start database with sample data
docker run --rm -p 1433:1433 registry.vnvc.info/vnvc-qas/qas-db-dev:latest
```

## Project Architecture

### Solution Structure

The solution follows a clean architecture pattern with clear separation of concerns:

- **WebService**: Main API project, controllers, and ASP.NET Core configuration
- **WebService.Handlers**: Business logic handlers that replace stored procedures
- **Entities**: Database entities and data connection classes (using LINQ to DB)
- **Services**: Shared business services and utilities
- **Utilities**: Common utilities and extension methods
- **TestHelpers**: Shared testing utilities and base classes

### Handler Architecture

Handlers are the core business logic components that replace SQL Server stored procedures:

**Handler Organization:**
- Each handler corresponds to one stored procedure
- Handlers are organized in folders by database name (e.g., `QAHosGenericDB`, `Application`, `Security`)
- Handler class names match the stored procedure names exactly

**Handler Implementation Patterns:**

1. **Direct IHandler implementation:**
```csharp
public class MyHandler(AladdinDataConnection db) : IHandler
{
    public DataSet Handle(Dictionary<string, object?> parameters)
    {
        // Implementation
    }
}
```

2. **Generic Handler (preferred for type safety):**
```csharp
public class MyHandler(AladdinDataConnection db) : GenericHandler<MyHandler.Parameters>
{
    public class Parameters
    {
        public string? SomeParam { get; set; }
        [DefaultValue("")] public string RequiredParam { get; set; }
    }

    public override DataSet Handle(Parameters @params)
    {
        // Implementation with strongly-typed parameters
    }
}
```

### Database Architecture

**Data Access Pattern:**
- Uses LINQ to DB for type-safe database operations  
- `AladdinDataConnection` provides access to multiple database contexts
- Database contexts are organized by schema (e.g., `QAHosGenericDB`, `Application`, `Security`)

**Key Database Contexts:**
- `QAHosGenericDB`: Primary business database
- `Application`: Application configuration
- `Security`: Authentication and authorization
- `Reports`: Reporting data
- `History`: Audit trail and history

### Testing Architecture

**Test Organization:**
- Handler tests in `WebService.Handlers.Tests` mirror the handler structure
- Test cases defined in YAML files under `TestCases/<database>/<handler>/`
- Tests inherit from `BaseHandlerTest` which extends `DatabaseTest`

**Test Structure:**
```csharp
public class HandlerName_Test : BaseHandlerTest
{
    private readonly HandlerName _handler;

    public HandlerName_Test()
    {
        _handler = new HandlerName(DbConnection);
    }

    [Theory]
    [MemberData(nameof(TestData), "QAHosGenericDB", "HandlerName")]
    public void Handle_ShouldReturnExpected(string testCasePath)
    {
        RunTestCase(_handler, testCasePath);
    }
}
```

## Development Guidelines

### Configuration Setup

1. **Local Development:**
   - Create `WebService/appsettings.Development.json` from sample file
   - Configure database connection string with local SQL Server credentials

2. **Testing:**
   - Tests use `appsettings.Test.json` 
   - Override locally with `appsettings.Local.json` (not committed)

### Handler Development Best Practices

1. **Database Queries:**
   - Use `WITH (NOLOCK)` hint: `.With(SqlServerHints.Table.NoLock)`
   - Use parameterized queries with `WhereIn()` for list operations
   - Prefer `AsEnumerable()` over `ToList()` when possible for memory efficiency

2. **Type Conversions:**
   - Use `AsVarChar()` for VARCHAR columns to ensure proper index usage
   - Handle nullable types carefully with `FirstOrDefault()`

3. **Performance:**
   - Use custom SQL expressions from `SqlExpr` class for complex operations
   - Implement efficient joins with proper hints
   - Consider query batching for large datasets using `Bucketize()` extension

### Authentication Flow

The API uses session-based authentication:
1. POST to `/Login` with username/password hash
2. Receive `sessionId` in response
3. Include `sessionId` in cookie `s` for subsequent requests
4. Access Swagger UI at `http://localhost:5272/swagger/index.html`

### Key Extension Methods and Utilities

- **SqlExpr**: Custom SQL functions and expressions
- **WhereIn**: Parameterized IN queries to avoid query plan proliferation  
- **Bucketize**: Split large collections into manageable chunks
- **DictionaryExtensions**: Parameter extraction utilities
- **AutoMapper integration**: For entity-to-DTO projections

## Important Files

- `HANDLERS.md`: Comprehensive handler development guide
- `.editorconfig`: Code formatting rules (enable in IDE)
- `WebService/appsettings.*.json`: Environment-specific configurations
- `TestCases/`: YAML test case definitions
- `Services/SqlExpr.cs`: Custom SQL expressions and utilities
- `WebService.Handlers.Tests/prompt.md`: AI assistant prompt for generating test cases

The project emphasizes type safety, comprehensive testing, and performance optimization while maintaining clean separation between business logic and data access layers.
