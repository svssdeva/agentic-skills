<!-- Source: https://skills.sh/analogjs/angular-skills/angular-tooling -->
<!-- Install: npx skills add https://github.com/analogjs/angular-skills --skill angular-tooling -->

# Angular Tooling

Essential commands and configuration for Angular v20+ development.

## Angular CLI Commands

### Project Creation

```bash
# Create new project
ng new my-app --routing --style=css

# With specific options
ng new my-app \
  --routing=true \
  --style=scss \
  --ssr=true \
  --skip-tests=false
```

### Generators

```bash
# Components (standalone by default in v20+)
ng generate component features/user-list
ng g c features/user-card
ng g c shared/button --skip-tests

# Services
ng generate service core/auth
ng g s features/user

# Directives
ng g d shared/highlight
ng g d features/tooltip

# Pipes
ng g pipe shared/capitalize
ng g p features/filter-by

# Interfaces & Types
ng g interface core/models/user
ng g i core/models/product

# Guards
ng g guard core/auth
ng g g core/admin --functional

# Resolvers
ng g resolver features/user

# Interceptors
ng g interceptor core/auth
ng g i core/error --functional
```

### Build & Serve

```bash
# Development server
ng serve
ng serve --port 4300 --open
ng serve --configuration=development

# Build
ng build
ng build --configuration=production
ng build --watch  # Rebuild on changes

# Specific configuration
ng build --base-href=/app/ --optimization=true
```

### Testing

```bash
# Run tests
ng test                    # Watch mode
ng test --watch=false      # Single run
ng test --code-coverage    # With coverage

# E2E tests
ng e2e
```

### Analysis

```bash
# Bundle analysis
ng build --stats-json
npx webpack-bundle-analyzer dist/my-app/stats.json

# Lint
ng lint
ng lint --fix
```

## Vite/esbuild Configuration

Angular v17+ uses Vite/esbuild by default via `@angular/build`:

### angular.json Build Config

```json
{
  "projects": {
    "my-app": {
      "architect": {
        "build": {
          "builder": "@angular/build:application",
          "options": {
            "outputPath": "dist/my-app",
            "index": "src/index.html",
            "browser": "src/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.app.json",
            "assets": [
              {
                "glob": "**/*",
                "input": "public"
              }
            ],
            "styles": ["src/styles.scss"],
            "scripts": []
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "500kB",
                  "maximumError": "1MB"
                }
              ],
              "outputHashing": "all",
              "sourceMap": false,
              "optimization": true
            },
            "development": {
              "optimization": false,
              "extractLicenses": false,
              "sourceMap": true,
              "namedChunks": true
            }
          }
        }
      }
    }
  }
}
```

## Zoneless Change Detection

Angular v20 supports zoneless mode for better performance:

```typescript
// app.config.ts
import { ApplicationConfig, provideExperimentalZonelessChangeDetection } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideExperimentalZonelessChangeDetection(),
    // Other providers...
  ],
};
```

### Remove Zone.js

```typescript
// main.ts - No zone.js import needed
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
```

### Remove from polyfills

```json
// angular.json - Remove zone.js from polyfills
{
  "polyfills": []  // Empty array for zoneless
}
```

## Environment Configuration

### Environment Files

```typescript
// src/environments/environment.ts (development)
export const environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api',
  features: {
    analytics: false,
    debugMode: true,
  },
};

// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.example.com',
  features: {
    analytics: true,
    debugMode: false,
  },
};
```

### File Replacements

```json
// angular.json
{
  "configurations": {
    "production": {
      "fileReplacements": [
        {
          "replace": "src/environments/environment.ts",
          "with": "src/environments/environment.prod.ts"
        }
      ]
    }
  }
}
```

### Usage

```typescript
import { environment } from '../environments/environment';

@Injectable({ providedIn: 'root' })
export class Api {
  private baseUrl = environment.apiUrl;

  getData() {
    if (environment.features.debugMode) {
      console.log('Fetching data...');
    }
    return this.http.get(`${this.baseUrl}/data`);
  }
}
```

## TypeScript Configuration

### tsconfig.json

```json
{
  "compileOnSave": false,
  "compilerOptions": {
    "outDir": "./dist/out-tsc",
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "sourceMap": true,
    "declaration": false,
    "experimentalDecorators": true,
    "moduleResolution": "bundler",
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022", "dom"],
    "useDefineForClassFields": false,
    "paths": {
      "@app/*": ["src/app/*"],
      "@shared/*": ["src/app/shared/*"],
      "@core/*": ["src/app/core/*"]
    }
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}
```

## Build Optimization

### Budgets

```json
{
  "budgets": [
    {
      "type": "initial",
      "maximumWarning": "500kB",
      "maximumError": "1MB"
    },
    {
      "type": "anyComponentStyle",
      "maximumWarning": "4kB",
      "maximumError": "8kB"
    },
    {
      "type": "bundle",
      "name": "vendor",
      "maximumWarning": "300kB"
    }
  ]
}
```

### Lazy Loading

```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./features/admin/admin.routes')
      .then(m => m.ADMIN_ROUTES),
  },
  {
    path: 'profile',
    loadComponent: () => import('./features/profile/profile')
      .then(m => m.Profile),
  },
];

// features/admin/admin.routes.ts
export const ADMIN_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./dashboard')
      .then(m => m.Dashboard),
  },
  {
    path: 'users',
    loadComponent: () => import('./users')
      .then(m => m.Users),
  },
];
```

### Preloading Strategies

```typescript
// app.config.ts
import { provideRouter, withPreloading, PreloadAllModules } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withPreloading(PreloadAllModules)
    ),
  ],
};

// Custom preloading
import { QuicklinkStrategy } from 'ngx-quicklink';
provideRouter(routes, withPreloading(QuicklinkStrategy));
```

## Development Tools

### Angular DevTools

Install: Chrome/Firefox extension "Angular DevTools"

Features:

* Component tree inspection
* Signal state viewer
* Profiler for change detection
* Route tree visualization

### ESLint Configuration

```json
// eslint.config.js
{
  "extends": [
    "eslint:recommended",
    "@angular-eslint/recommended",
    "@angular-eslint/template/recommended"
  ],
  "rules": {
    "@angular-eslint/prefer-standalone": "error",
    "@angular-eslint/prefer-signals": "warn",
    "@angular-eslint/no-input-rename": "error",
    "@angular-eslint/no-output-rename": "error",
    "@angular-eslint/use-lifecycle-interface": "error"
  }
}
```

### Prettier Configuration

```json
// .prettierrc
{
  "tabWidth": 2,
  "useTabs": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "overrides": [
    {
      "files": "*.html",
      "options": {
        "parser": "angular"
      }
    }
  ]
}
```

## Schematics

### Update Angular

```bash
ng update @angular/cli @angular/core

# Check for updates
ng update

# Update all packages
ng update --all

# Preview changes
ng update --dry-run
```

### Add Packages

```bash
# Official packages
ng add @angular/material
ng add @angular/pwa
ng add @angular/ssr

# Third-party
ng add @ngrx/store
ng add @analogjs/astro-angular
```

### Migration Schematics

```bash
# Migrate to standalone
ng generate @angular/core:standalone

# Migrate to signal inputs
ng generate @angular/core:signal-input-migration

# Migrate to signal queries
ng generate @angular/core:signal-queries-migration

# Migrate to self-closing tags
ng generate @angular/core:self-closing-tags-migration

# Migrate to control flow
ng generate @angular/core:control-flow

# Migrate to inject()
ng generate @angular/core:inject
```

## Performance Monitoring

### Bundle Analysis

```bash
# Generate stats
ng build --stats-json

# Analyze
npx webpack-bundle-analyzer dist/my-app/stats.json
```

### Source Maps

```json
// angular.json
{
  "configurations": {
    "production": {
      "sourceMap": {
        "scripts": true,
        "styles": true,
        "hidden": true,
        "vendor": true
      }
    }
  }
}
```

## Useful Dev Scripts

```json
// package.json
{
  "scripts": {
    "start": "ng serve",
    "build": "ng build --configuration=production",
    "test": "ng test",
    "test:watch": "ng test --watch",
    "test:coverage": "ng test --code-coverage",
    "lint": "ng lint",
    "lint:fix": "ng lint --fix",
    "format": "prettier --write \"src/**/*.{ts,html,css,scss}\"",
    "analyze": "ng build --stats-json && webpack-bundle-analyzer dist/my-app/stats.json"
  }
}
```

For advanced configuration patterns, see references/tooling-patterns.md.
