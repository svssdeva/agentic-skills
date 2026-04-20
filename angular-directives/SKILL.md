<!-- Source: https://skills.sh/analogjs/angular-skills/angular-directives -->
<!-- Install: npx skills add https://github.com/analogjs/angular-skills --skill angular-directives -->

# Angular Directives

Create custom directives for reusable DOM behavior in Angular v20+.

## Attribute Directives

Add behavior to existing elements:

```typescript
import { Directive, ElementRef, inject, input, effect } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
})
export class Highlight {
  private el = inject(ElementRef);

  // Signal input
  color = input('yellow');

  constructor() {
    effect(() => {
      this.el.nativeElement.style.backgroundColor = this.color();
    });
  }
}
```

Usage:

```html
<p appHighlight>Highlighted!</p>
<p appHighlight color="lightblue">Custom color</p>
<p [appHighlight] [color]="dynamicColor()">Dynamic</p>
```

## Host Bindings

Use `host` object instead of decorators:

```typescript
@Directive({
  selector: '[appTooltip]',
  host: {
    // Event listeners
    '(mouseenter)': 'show()',
    '(mouseleave)': 'hide()',
    '(focus)': 'show()',
    '(blur)': 'hide()',

    // Dynamic bindings
    '[class.has-tooltip]': 'hasTooltip()',
    '[attr.aria-describedby]': 'tooltipId()',
    '[style.--tooltip-delay.ms]': 'delay()',
  },
})
export class Tooltip {
  text = input.required<string>();
  delay = input(200);

  hasTooltip = computed(() => !!this.text());
  tooltipId = computed(() => `tooltip-${this.id}`);

  private id = Math.random().toString(36);

  show() {
    // Show tooltip logic
  }

  hide() {
    // Hide tooltip logic
  }
}
```

## Structural Directives

Manipulate DOM structure with `TemplateRef` and `ViewContainerRef`:

```typescript
import { Directive, TemplateRef, ViewContainerRef, input, effect, inject } from '@angular/core';

@Directive({
  selector: '[appIfAuthenticated]',
})
export class IfAuthenticated {
  private templateRef = inject(TemplateRef<unknown>);
  private viewContainer = inject(ViewContainerRef);
  private authService = inject(Auth);

  // Optional fallback template
  elseTemplate = input<TemplateRef<unknown> | null>(null, {
    alias: 'appIfAuthenticatedElse',
  });

  constructor() {
    effect(() => {
      this.viewContainer.clear();

      if (this.authService.isAuthenticated()) {
        this.viewContainer.createEmbeddedView(this.templateRef);
      } else if (this.elseTemplate()) {
        this.viewContainer.createEmbeddedView(this.elseTemplate()!);
      }
    });
  }
}
```

Usage:

```html
<div *appIfAuthenticated="; else loginPrompt">
  Welcome back!
</div>

<ng-template #loginPrompt>
  <a routerLink="/login">Please log in</a>
</ng-template>
```

## Host Directives (Composition)

Compose behavior from multiple directives:

```typescript
@Directive({
  selector: '[appInteractive]',
  hostDirectives: [
    Focusable,
    Hoverable,
    {
      directive: Trackable,
      inputs: ['eventName: trackEvent'],
    },
  ],
})
export class Interactive {
  // Inherits behaviors from all host directives
}
```

### Example: Accessibility Host Directive

```typescript
@Directive({
  selector: '[appFocusable]',
  host: {
    'tabindex': '0',
    '[attr.role]': 'role()',
    '[class.focused]': 'isFocused()',
    '(focus)': 'isFocused.set(true)',
    '(blur)': 'isFocused.set(false)',
  },
})
export class Focusable {
  role = input('button');
  isFocused = signal(false);
}

@Component({
  selector: 'app-card',
  hostDirectives: [
    {
      directive: Focusable,
      inputs: ['role'],
    },
  ],
  template: `...`,
})
export class Card {
  // Card is now focusable
}
```

## Directive Communication

### Parent-to-Directive via Inputs

```typescript
@Directive({
  selector: '[appValidator]',
})
export class Validator {
  rules = input.required<ValidationRule[]>();
  value = input.required<string>();

  isValid = computed(() => {
    const val = this.value();
    return this.rules().every(rule => rule.validate(val));
  });
}
```

### Directive-to-Parent via Outputs

```typescript
@Directive({
  selector: '[appSwipe]',
  host: {
    '(touchstart)': 'onTouchStart($event)',
    '(touchend)': 'onTouchEnd($event)',
  },
})
export class Swipe {
  threshold = input(50);
  swiped = output<'left' | 'right' | 'up' | 'down'>();

  private startX = 0;
  private startY = 0;

  onTouchStart(e: TouchEvent) {
    this.startX = e.touches[0].clientX;
    this.startY = e.touches[0].clientY;
  }

  onTouchEnd(e: TouchEvent) {
    const deltaX = e.changedTouches[0].clientX - this.startX;
    const deltaY = e.changedTouches[0].clientY - this.startY;

    if (Math.abs(deltaX) > this.threshold()) {
      this.swiped.emit(deltaX > 0 ? 'right' : 'left');
    } else if (Math.abs(deltaY) > this.threshold()) {
      this.swiped.emit(deltaY > 0 ? 'down' : 'up');
    }
  }
}
```

Usage:

```html
<div appSwipe (swiped)="handleSwipe($event)">
  Swipe me
</div>
```

## Dependency Injection in Directives

```typescript
@Directive({
  selector: '[appAutoFocus]',
})
export class AutoFocus {
  private el = inject(ElementRef<HTMLElement>);

  // Inject other directives from same element
  private parent = inject(NgForm, { optional: true });

  // Inject from host element
  private tooltip = inject(Tooltip, { host: true, optional: true });

  delay = input(0);

  constructor() {
    afterNextRender(() => {
      setTimeout(() => this.el.nativeElement.focus(), this.delay());
    });
  }
}
```

## Directive with State

```typescript
@Directive({
  selector: '[appDraggable]',
  host: {
    '[class.dragging]': 'isDragging()',
    '[style.cursor]': 'isDragging() ? "grabbing" : "grab"',
    '(mousedown)': 'startDrag($event)',
    '(document:mousemove)': 'onDrag($event)',
    '(document:mouseup)': 'endDrag()',
  },
})
export class Draggable {
  isDragging = signal(false);
  position = signal({ x: 0, y: 0 });

  dragStart = output<DragEvent>();
  dragMove = output<{ x: number; y: number }>();
  dragEnd = output<void>();

  private offset = { x: 0, y: 0 };

  startDrag(e: MouseEvent) {
    this.isDragging.set(true);
    this.offset = {
      x: e.clientX - this.position().x,
      y: e.clientY - this.position().y,
    };
    this.dragStart.emit(new DragEvent('start'));
  }

  onDrag(e: MouseEvent) {
    if (!this.isDragging()) return;

    const newPos = {
      x: e.clientX - this.offset.x,
      y: e.clientY - this.offset.y,
    };
    this.position.set(newPos);
    this.dragMove.emit(newPos);
  }

  endDrag() {
    if (this.isDragging()) {
      this.isDragging.set(false);
      this.dragEnd.emit();
    }
  }
}
```

## Common Use Cases

### Click Outside Directive

```typescript
@Directive({
  selector: '[appClickOutside]',
})
export class ClickOutside {
  private el = inject(ElementRef);

  clickOutside = output<MouseEvent>();

  constructor() {
    fromEvent<MouseEvent>(document, 'click')
      .pipe(takeUntilDestroyed())
      .subscribe(event => {
        const target = event.target as Node;
        if (!this.el.nativeElement.contains(target)) {
          this.clickOutside.emit(event);
        }
      });
  }
}
```

### Intersection Observer

```typescript
@Directive({
  selector: '[appLazyLoad]',
})
export class LazyLoad {
  private el = inject(ElementRef<HTMLElement>);

  src = input.required<string>();
  rootMargin = input('50px');

  private observer?: IntersectionObserver;

  constructor() {
    afterNextRender(() => {
      this.observer = new IntersectionObserver(
        entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              this.loadImage();
              this.observer?.disconnect();
            }
          });
        },
        { rootMargin: this.rootMargin() }
      );

      this.observer.observe(this.el.nativeElement);
    });

    inject(DestroyRef).onDestroy(() => {
      this.observer?.disconnect();
    });
  }

  private loadImage() {
    const img = this.el.nativeElement as HTMLImageElement;
    img.src = this.src();
  }
}
```

For advanced directive patterns, see references/directive-patterns.md.
