<!-- Source: https://skills.sh/analogjs/angular-skills/angular-testing -->
<!-- Install: npx skills add https://github.com/analogjs/angular-skills --skill angular-testing -->

# Angular Testing

Write unit and integration tests for Angular v20+ components, services, and directives using Vitest and Angular Testing Library.

## Test Setup

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import angular from '@analogjs/vite-plugin-angular';

export default defineConfig({
  plugins: [angular()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['src/test-setup.ts'],
  },
});
```

```typescript
// src/test-setup.ts
import '@analogjs/vitest-angular/setup-zoneless';
```

## Component Testing

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';
import { Counter } from './counter';

describe('Counter', () => {
  it('should increment count on button click', async () => {
    const user = userEvent.setup();

    await render(Counter);

    expect(screen.getByText('Count: 0')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### Testing with Inputs

```typescript
import { render, screen } from '@testing-library/angular';
import { UserCard } from './user-card';

describe('UserCard', () => {
  it('should display user information', async () => {
    await render(UserCard, {
      inputs: {
        name: 'Alice',
        email: 'alice@example.com',
        isActive: true,
      },
    });

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    expect(screen.getByRole('article')).toHaveClass('active');
  });

  it('should update when inputs change', async () => {
    const { rerender } = await render(UserCard, {
      inputs: { name: 'Alice' },
    });

    expect(screen.getByText('Alice')).toBeInTheDocument();

    await rerender({ inputs: { name: 'Bob' } });

    expect(screen.getByText('Bob')).toBeInTheDocument();
  });
});
```

### Testing Outputs

```typescript
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { Button } from './button';

describe('Button', () => {
  it('should emit clicked event', async () => {
    const user = userEvent.setup();
    const clickedSpy = vi.fn();

    await render(Button, {
      inputs: { label: 'Click me' },
      on: {
        clicked: clickedSpy,
      },
    });

    await user.click(screen.getByRole('button', { name: /click me/i }));

    expect(clickedSpy).toHaveBeenCalledOnce();
  });
});
```

### Testing with Providers

```typescript
import { render, screen } from '@testing-library/angular';
import { UserProfile } from './user-profile';
import { Auth } from './auth.service';

describe('UserProfile', () => {
  it('should display user name from auth service', async () => {
    const mockAuth = {
      user: signal({ id: '1', name: 'Alice', email: 'alice@test.com' }),
      isAuthenticated: computed(() => true),
    };

    await render(UserProfile, {
      providers: [
        { provide: Auth, useValue: mockAuth },
      ],
    });

    expect(screen.getByText('Welcome, Alice')).toBeInTheDocument();
  });

  it('should show login prompt when not authenticated', async () => {
    const mockAuth = {
      user: signal(null),
      isAuthenticated: computed(() => false),
    };

    await render(UserProfile, {
      providers: [
        { provide: Auth, useValue: mockAuth },
      ],
    });

    expect(screen.getByText(/please log in/i)).toBeInTheDocument();
  });
});
```

## Service Testing

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { User } from './user.service';

describe('User', () => {
  let service: User;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        User,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(User);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch users', async () => {
    const mockUsers = [
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ];

    const promise = service.loadUsers();

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);

    await promise;
    expect(service.users()).toEqual(mockUsers);
  });

  it('should handle errors', async () => {
    const promise = service.loadUsers();

    const req = httpMock.expectOne('/api/users');
    req.flush('Error', { status: 500, statusText: 'Server Error' });

    await expect(promise).rejects.toThrow();
  });
});
```

## Signal Testing

```typescript
import { TestBed } from '@angular/core/testing';
import { signal, computed } from '@angular/core';

describe('Signal computations', () => {
  it('should update computed when signal changes', () => {
    const count = signal(0);
    const doubled = computed(() => count() * 2);

    expect(doubled()).toBe(0);

    count.set(5);
    expect(doubled()).toBe(10);

    count.update(c => c + 1);
    expect(doubled()).toBe(12);
  });
});

describe('Counter service', () => {
  let counter: Counter;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [Counter],
    });
    counter = TestBed.inject(Counter);
  });

  it('should increment count', () => {
    expect(counter.count()).toBe(0);

    counter.increment();
    expect(counter.count()).toBe(1);

    counter.increment();
    expect(counter.count()).toBe(2);
  });
});
```

## Form Testing

### Testing Signal Forms

```typescript
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './login-form';

describe('LoginForm', () => {
  it('should validate required fields', async () => {
    const user = userEvent.setup();

    await render(LoginForm);

    const submitBtn = screen.getByRole('button', { name: /login/i });
    expect(submitBtn).toBeDisabled();

    // Fill email only
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    expect(submitBtn).toBeDisabled();

    // Fill password
    await user.type(screen.getByLabelText(/password/i), 'password123');
    expect(submitBtn).toBeEnabled();
  });

  it('should show validation errors', async () => {
    const user = userEvent.setup();

    await render(LoginForm);

    const emailInput = screen.getByLabelText(/email/i);

    // Enter invalid email
    await user.type(emailInput, 'invalid');
    await user.tab(); // Blur field

    expect(screen.getByText(/valid email/i)).toBeInTheDocument();

    // Fix email
    await user.clear(emailInput);
    await user.type(emailInput, 'valid@example.com');

    expect(screen.queryByText(/valid email/i)).not.toBeInTheDocument();
  });

  it('should submit form with valid data', async () => {
    const user = userEvent.setup();
    const submitSpy = vi.fn();

    await render(LoginForm, {
      on: { submit: submitSpy },
    });

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(submitSpy).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});
```

## HTTP Resource Testing

```typescript
import { render, screen, waitFor } from '@testing-library/angular';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { UserProfile } from './user-profile';

describe('UserProfile with httpResource', () => {
  it('should load and display user', async () => {
    await render(UserProfile, {
      inputs: { userId: '123' },
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    const httpMock = TestBed.inject(HttpTestingController);

    // Check loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Respond to request
    const req = httpMock.expectOne('/api/users/123');
    req.flush({
      id: '123',
      name: 'Alice',
      email: 'alice@test.com',
    });

    // Wait for data to render
    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
    });

    expect(screen.getByText('alice@test.com')).toBeInTheDocument();
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();

    httpMock.verify();
  });
});
```

## Testing Patterns

### User-Event Best Practices

```typescript
// Always use userEvent over fireEvent
const user = userEvent.setup();

// Click
await user.click(button);
await user.dblClick(element);

// Typing
await user.type(input, 'Hello');
await user.clear(input);
await user.type(input, 'New value');

// Keyboard
await user.keyboard('{Enter}');
await user.keyboard('{Control>}a{/Control}'); // Select all

// Select options
await user.selectOptions(dropdown, 'option1');

// Upload files
const file = new File(['content'], 'test.txt');
await user.upload(fileInput, file);
```

### Async Testing

```typescript
import { waitFor } from '@testing-library/angular';

// Wait for element to appear
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// Wait for element to disappear
await waitFor(() => {
  expect(screen.queryByText('Loading')).not.toBeInTheDocument();
});

// Custom timeout
await waitFor(
  () => expect(screen.getByText('Slow')).toBeInTheDocument(),
  { timeout: 5000 }
);
```

### Accessible Queries

Prefer these in order:

1. `getByRole` - Best, mirrors assistive tech
2. `getByLabelText` - Forms
3. `getByPlaceholderText` - Fallback for forms
4. `getByText` - Non-interactive elements
5. `getByDisplayValue` - Form values
6. `getByAltText` - Images
7. `getByTitle` - Last resort
8. `getByTestId` - Only when nothing else works

```typescript
screen.getByRole('button', { name: /submit/i });
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('heading', { level: 2 });
screen.getByRole('dialog');
screen.getByLabelText('Password');
screen.getByText(/welcome/i);
```

## Directive Testing

```typescript
import { Component } from '@angular/core';
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';
import { Tooltip } from './tooltip';

@Component({
  imports: [Tooltip],
  template: `<button appTooltip text="Help">Hover me</button>`,
})
class HostComponent {}

describe('Tooltip', () => {
  it('should show tooltip on hover', async () => {
    const user = userEvent.setup();

    await render(HostComponent);

    const button = screen.getByRole('button');

    expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();

    await user.hover(button);

    expect(screen.getByRole('tooltip')).toHaveTextContent('Help');
  });
});
```

For integration testing patterns, see references/testing-patterns.md.
